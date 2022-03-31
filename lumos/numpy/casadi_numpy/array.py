import numpy as _onp
import casadi as _cas
from typing import List, Tuple, Union
from lumos.numpy.casadi_numpy.determine_type import is_casadi_type


def array(array_like, dtype=None):
    """
    Initializes a new array. Creates a NumPy array if possible; if not, creates a CasADi array.

    See syntax here: https://numpy.org/doc/stable/reference/generated/numpy.array.html
    """
    if is_casadi_type(
        array_like, recursive=False
    ):  # If you were literally given a CasADi array, just return it
        # Handles inputs like cas.DM([1, 2, 3])
        return array_like

    elif not is_casadi_type(
        array_like, recursive=True
    ):  # If you were given a list of iterables that don't have CasADi types:
        # Handles inputs like [[1, 2, 3], [4, 5, 6]]
        return _onp.array(array_like, dtype=dtype)

    else:
        # Handles inputs like [[opti_var_1, opti_var_2], [opti_var_3, opti_var_4]]
        def make_row(contents: List):
            try:
                return _cas.horzcat(*contents)
            except (TypeError, Exception):
                return contents

        return _cas.vertcat(*[make_row(row) for row in array_like])


def concatenate(arrays: Tuple, axis: int = 0):
    """
    Join a sequence of arrays along an existing axis. Returns a NumPy array if possible; if not, returns a CasADi array.

    See syntax here: https://numpy.org/doc/stable/reference/generated/numpy.concatenate.html
    """

    if not is_casadi_type(arrays, recursive=True):
        return _onp.concatenate(arrays, axis=axis)

    else:
        if axis == 0:
            return _cas.vertcat(*arrays)
        elif axis == 1:
            return _cas.horzcat(*arrays)
        else:
            raise ValueError(
                "CasADi-backend arrays can only be 1D or 2D, so `axis` must be 0 or 1."
            )


def stack(arrays: Tuple, axis: int = 0):
    """
    Join a sequence of arrays along a new axis. Returns a NumPy array if possible; if not, returns a CasADi array.

    See syntax here: https://numpy.org/doc/stable/reference/generated/numpy.stack.html
    """
    if not is_casadi_type(arrays, recursive=True):
        return _onp.stack(arrays, axis=axis)

    else:
        ### Validate stackability
        for array in arrays:
            if is_casadi_type(array, recursive=False):
                if not array.shape[1] == 1:
                    raise ValueError("Can only stack Nx1 CasADi arrays!")
            else:
                if not len(array.shape) == 1:
                    raise ValueError(
                        "Can only stack 1D NumPy ndarrays alongside CasADi arrays!"
                    )

        if axis == 0 or axis == -2:
            return _cas.transpose(_cas.horzcat(*arrays))
        elif axis == 1 or axis == -1:
            return _cas.horzcat(*arrays)
        else:
            raise ValueError(
                "CasADi-backend arrays can only be 1D or 2D, so `axis` must be 0 or 1."
            )


def hstack(arrays):
    # FIXME: add size and type checks
    return _cas.horzcat(*arrays)


def vstack(arrays):
    # FIXME: add size and type checks
    return _cas.vertcat(*arrays)


def _check_1d_arrays(arrays):
    """Check if all arrays in an list of arrays are 1d casadi array of shape (n, 1)"""
    for a in arrays:
        if not (a.shape[1] == 1):
            return False

    return True


def column_stack(arrays):
    """Stack 1-D arrays as columns into a 2-D array.

    Since casadi by default uses 2-d array to represetn a vector (column vector),
    we need to be very explicit when we're working with 2d or 1d arrays
    """

    if not (_check_1d_arrays(arrays)):
        raise ValueError("To use column_stack, all arrays must be 1d casadi arrays.")

    return _cas.horzcat(*arrays)


def row_stack(arrays):
    """Stack 1-D arrays as rows into a 2-D array.

    see: https://numpy.org/devdocs/reference/generated/numpy.row_stack.html

    Since casadi by default uses 2-d array to represent a vector (column vector),
    we need to be very explicit when we're working with 2d or 1d arrays
    """

    if not (_check_1d_arrays(arrays)):
        raise ValueError("To use row_stack, all arrays must be 1d casadi arrays.")
    return _cas.horzcat(*arrays).T


def split(array, indices_or_sections: Union[List[int], int], axis: int):

    # FIXME, check for array sizes, etc. Currently assumes 2d array
    if axis == 0:
        split_func = _cas.vertsplit
    elif axis == 1 or axis == -1:
        split_func = _cas.horzsplit

    if isinstance(indices_or_sections, int):
        # integer, so split into N equal parts
        if not (array.shape[axis] % indices_or_sections == 0):
            raise ValueError(
                f"Cannot split an array of shape {array.shape} into {indices_or_sections} equal parts along axis {axis} "
            )
        else:
            # casadi requires the size of each split, instead of number of splits like numpy
            indices_or_sections = int(array.shape[axis] / indices_or_sections)
    elif isinstance(indices_or_sections, list):
        # casadi horzsplit/vertsplit works the same as numpy array indices, but need 0 and
        # size appended at the two ends
        indices_or_sections = [0, *indices_or_sections, array.shape[axis]]

    return split_func(array, indices_or_sections)


def hsplit(array, indices_or_sections):

    return split(array, indices_or_sections, axis=1)


def vsplit(array, indices_or_sections):
    return split(array, indices_or_sections, axis=0)


def dstack(arrays):
    if not is_casadi_type(arrays, recursive=True):
        return _onp.dstack(arrays)
    else:
        raise ValueError(
            "Use `np.stack()` or `np.concatenate()` instead of `np.dstack()` when dealing with mixed-backend arrays."
        )


def length(array) -> int:
    """
    Returns the length of an 1D-array-like object. An extension of len() with slightly different functionality.
    Args:
        array:

    Returns:

    """
    if not is_casadi_type(array):
        try:
            return len(array)
        except TypeError:
            return 1

    else:
        if array.shape[0] != 1:
            return array.shape[0]
        else:
            return array.shape[1]


def diag(v, k=0):
    """
    Extract a diagonal or construct a diagonal array.

    See syntax here: https://numpy.org/doc/stable/reference/generated/numpy.diag.html
    """
    if not is_casadi_type(v):
        return _onp.diag(v, k=k)

    else:
        if k != 0:
            raise NotImplementedError(
                "Should be super possible, just haven't had the need yet."
            )

        if 1 in v.shape:
            return _cas.diag(v)
        elif v.shape[0] == v.shape[1]:
            raise NotImplementedError(
                "Should be super possible, just haven't had the need yet."
            )
        else:
            raise ValueError("Cannot return the diagonal of a non-square matrix.")


def roll(a, shift, axis: int = None):
    """
    Roll array elements along a given axis.

    Elements that roll beyond the last position are re-introduced at the first.

    See syntax here: https://numpy.org/doc/stable/reference/generated/numpy.roll.html

    Parameters
    ----------
    a : array_like
        Input array.
    shift : int
        The number of places by which elements are shifted.

    Returns
    -------
    res : ndarray
        Output array, with the same shape as a.

    """
    if not is_casadi_type(a):
        return _onp.roll(a, shift, axis=axis)
    else:  # TODO add some checking to make sure shift < len(a), or shift is modulo'd down by len(a).
        # assert shift < a.shape[axis]
        if 1 in a.shape and axis == 0:
            return _cas.vertcat(a[-shift, :], a[:-shift, :])
        elif axis == 0:
            return _cas.vertcat(a.T[:, -shift], a.T[:, :-shift]).T
        elif axis == 1:
            return _cas.horzcat(a[:, -shift], a[:, :-shift])
        elif axis is None:
            return roll(a, shift=shift, axis=0)
        else:
            raise Exception(
                "CasADi types can only be up to 2D, so `axis` must be None, 0, or 1."
            )


def max(a):
    """
    Returns the maximum value of an array
    """

    try:
        return _onp.max(a)
    except TypeError:
        return _cas.mmax(a)


def min(a):
    """
    Returns the minimum value of an array
    """

    try:
        return _onp.min(a)
    except TypeError:
        return _cas.mmin(a)


def reshape(a, newshape):
    """Gives a new shape to an array without changing its data."""

    if not is_casadi_type(a):
        return _onp.reshape(a, newshape)
    else:
        return _cas.reshape(a, newshape)


def zeros(shape):
    return _cas.SX.zeros(shape)


def zeros_like(array):
    return _cas.SX.zeros(array.shape)


def eye(shape):
    return _cas.SX.eye(shape)


def ones(shape):
    return _cas.SX.ones(shape)
