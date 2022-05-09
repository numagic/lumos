import logging
from contextlib import ContextDecorator
from typing import Any, List, Union

import casadi
import jax.numpy as jnp
import numpy as np

import lumos.numpy as lnp

logger = logging.getLogger(__name__)


class use_backend(ContextDecorator):
    def __init__(self, backend: str):
        self._original_backend = lnp.get_backend()
        self._target_backend = backend

    def __enter__(self):
        lnp.set_backend(self._target_backend)

    def __exit__(self, *exc):
        lnp.set_backend(self._original_backend)


def is_jax_array(x: Any) -> bool:
    """
    See https://github.com/google/jax/issues/2014#issuecomment-808977622
    """
    return isinstance(x, jnp.ndarray) and not isinstance(x, np.ndarray)


def assert_allclose(a, b, *args, **kwargs) -> bool:
    """Overwrite the numpy one because we need type conversion for casadi.

    The plain numpy.testing.assert_allclose works well for numpy and jax.numpy,
    but doesn't work for casadi.SX
    """

    # TODO: casadi represents vector as 2d array, but sometimes we do have 2d arrays that
    # just happens to have one dimension = 1, how do we differentiate between these cases?

    def patch_casadi(var):
        """Try to remove duplicate casadi dimension and convert type to assertable"""
        if isinstance(var, casadi.SX):
            # convert SX to DM, which can be used for comparison to numpy and jax.numpy array.
            var = np.array(casadi.DM(var))
            if 1 in var.shape:
                var = var.flatten()

        return var

    return np.testing.assert_allclose(patch_casadi(a), patch_casadi(b), *args, **kwargs)


def vector_concat(arrays):
    """Concatenate 1d vectors along the existing axis

    Need special handling because casadi arrays are 2d, eg (6, 1), while numpy and jax
    numpy are 1d, eg (6, ), which would mean one would need vstack, and the other hstack
    """

    if lnp.get_backend() == "casadi":
        return casadi.vertcat(*arrays)
    else:
        return lnp.hstack(arrays)


def vector_split(array, split_indices: List[int]):
    # FIXME:
    # 1) documentation
    # 2) test
    if lnp.get_backend() == "casadi":
        # casadi requires the split indices to start with 0 and finish with size
        split_indices = [0, *split_indices, array.size()[0]]
        return casadi.vertsplit(array, split_indices)
    else:
        return lnp.split(array, split_indices)


def vector_tile(vec, reps: int):
    """Turn a 1d vector into a 2d matrix by tiling on the leading dimension.

    Casadi represents vectors as D x 1 array, so needs to be treated differently.

    For casadi: [D x 1 ] vector -> [N x D] array
    For numpy/jax: [D, ] vector -> [N x D] array
    """

    if lnp.get_backend() == "casadi":
        return casadi.repmat(vec.T, reps, 1)
    else:
        return lnp.tile(vec, (reps, 1))


def cmap(
    fn,
    in_axes: Union[int, List[Union[int, None]]] = 0,
    num_workers: int = 32,
    sparse: bool = False,
):
    """Casadi map in a syntax similar to jax vmap

    The cmap uses casadi's native 'map' on Casadi Functions for multi-thread execution.

    sparse: for most cases we need to transpose because casadi by default maps to the
    row axis. But for sparse jacobian values, we don't need to transpose, because while
    casadi uses column major, the flattened order of the non-zero values are actually
    correct without transposing!

    # TODO:
    - for casadi, only 2d matrices are possible, so really the in_axes can only be 0 or 1
    we handle the case for 0 here, but for 1, we actually need to remove the double
    transpose
    - for jax, the vmap actually retains the container structure, but we don't do it for
    casadi, since casadi can only output tuples. So we need to handle the structure on
    an outer layer

    """

    def fmapped(*args):
        if isinstance(in_axes, list):
            assert len(in_axes) == len(args)
            full_in_axes = in_axes
        else:
            full_in_axes = [in_axes] * len(args)

        # First find an argument that needs to be mapped
        sample_arg = next(a for a in args if a is not None)
        batch = sample_arg.shape[0]

        # NOTE: Creating the mapped function costs quite a bit of overhead. Therefore we
        # make the decorator stateful and caches the mapped function. As long as the
        # batch size remains unchanged, we use the cached mapped function.
        if not hasattr(fmapped, "batch_size"):
            fmapped.batch_size = None

        if not hasattr(fmapped, "raw_mapped"):
            fmapped.raw_mapped = None

        if batch != fmapped.batch_size:
            logger.info(
                f"cached batch size {fmapped.batch_size}. Got batch {batch}. "
                "Updating mapped function"
            )
            # update batch_size and re-create raw-mapped
            fmapped.batch_size = batch
            fmapped.raw_mapped = fn.map(batch, "thread", num_workers)

        # Since Casadi must map all inputs, so
        # for inputs that we don't want to map (in_axes=None), we need to tile.
        # NOTE: for parameter input, which are usually tree type data or dicitonary
        # clearly tiling won't work. But this works here because casadi works on
        # flattened array as parameters
        args = [
            np.tile(a, (batch, 1)) if map_axis is None else a
            for (a, map_axis) in zip(args, full_in_axes)
        ]

        # Casadi by default uses column vector, and hence maps both the inputs and ouputs
        # in row dimension, so we need to transpose both
        args = [a.T for a in args]
        outputs = fmapped.raw_mapped(*args)

        # Since casadi only concatenates on existing axis (and also it is limited to 2d)
        # The outputs have the following shape:
        # jacobian: [num_con, num_var x batch] -> [num_con, num_var, batch] in casadi order
        # since casadi is column major, the underlyng data vector is equivalent to that
        # of [batch, num-var, num_con] in row-major numpy.

        # hessian: [num_var, num_var x batch]

        # Now transpose the outputs, take care of multiple outputs if there are
        if sparse:
            nnz = int(outputs.nnz() / batch)

            # NOTE: here we do NOT need to do the reshape, as all we need is the
            # underlying flat continguous array of the matrix (because we use sparse
            # representation). And since the original outputs.sparse().data already
            # satisfies the contiguous array requirement, we could directly pass it out
            # (reshape does not change the underlying contiguous array)
            #
            # The reshape is done to provide a more meaningful output to make splitting
            # the big jacobian into smaller chunks easier for postprocessing (eg: for
            # condensing).
            # NOTE: for the (batch, nnz) array, the size nnz row is a unit jacobian
            # flattened as column major! (casadi still outputs jacobian as (n_out, n_in),
            # but at the same time, casadi is column major). This column major is not
            # an issue as long as the indices we pass for each unit problem are also
            # flattened with column major. See StateSpaceModel._make_casadi_model_algebra_cons
            # check C++ API documentation here:
            # http://casadi.sourceforge.net/v3.4.4/api/html/dd/df2/singletoncasadi_1_1Matrix.html#details
            # NOTE: Both the nonzeros and the reshape calls cost some non-trivial
            # overhead. For the LTC example with 2500 intervals LGR3, they cost roughly
            # 0.1sec each
            # this is the python API for the cpp get_nonzeros()
            data = outputs.nonzeros()
            outputs = np.reshape(data, (batch, nnz))
        else:
            if isinstance(outputs, tuple):
                outputs = tuple(np.array(o).T for o in outputs)
            else:
                outputs = np.array(outputs).T

        return outputs

    return fmapped


def lmap(
    fn, in_axes: Union[int, List[Union[int, None]]] = 0,
):
    """Simple map in a syntax similar to jax vmap, using for loops

    FIXME: currently only works for array outputs
    """

    def fmapped(*args):
        if isinstance(in_axes, list):
            assert len(in_axes) == len(args)
            full_in_axes = in_axes
        else:
            full_in_axes = [in_axes] * len(args)

        # First find an argument that needs to be mapped
        sample_arg = next(a for a in args if a is not None)
        batch_size = sample_arg.shape[0]

        out_array = []
        for idx in range(batch_size):
            sample_args = [
                a if map_axis is None else a[idx]
                for (a, map_axis) in zip(args, full_in_axes)
            ]
            sample_out = fn(*sample_args)
            out_array.append(sample_out)

        if isinstance(out_array[0], tuple):
            # array of tuple, need to make it a tuple of arrays
            ContainerClass = type(out_array[0])
            num_tuple_elements = len(out_array[0])
            converted_array = [
                np.array([o[tuple_idx] for o in out_array])
                for tuple_idx in range(num_tuple_elements)
            ]
            if ContainerClass == tuple:
                return tuple(converted_array)
            else:
                return ContainerClass(*converted_array)
        else:
            return np.stack(out_array)

    return fmapped
