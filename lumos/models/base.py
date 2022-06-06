import logging
import hashlib
import subprocess
from abc import abstractmethod
from collections import namedtuple
from typing import Any, Dict, NamedTuple, Optional, Tuple
from os.path import exists, getsize

import casadi as cas
import numpy as np
from jax import jit, vmap

import lumos.numpy as lnp
from lumos.models.composition import CompositeModel

logger = logging.getLogger(__name__)


# Convert from names and arrays to dictionary
def _array_to_dict(names, values):
    # We could do dict(zip(names, values)), but unfortunately this does NOT work
    # for casadi as casadi matrices are designed to be non-iterable
    # see: https://github.com/casadi/casadi/issues/2278
    return {name: values[idx] for idx, name in enumerate(names)}


# We use namedtuple to make the io names immutable after generation. They will be used
# for two types of names:
# the direct names: which are fully defined by the model itself
# the 'names': which is the eventual IO taking into consideration submodels and etc.
ModelIO = namedtuple("BaseIO", ("inputs", "outputs", "residuals"))
StateSpaceIO = namedtuple(
    "StateSpaceIO",
    ("states", "states_dot", "inputs", "outputs", "con_outputs", "residuals"),
)


def model_io(
    inputs: Tuple[str] = (), outputs: Tuple[str] = (), residuals: Tuple[str] = (),
):
    """Decorator to set the input and output names of a stateless model."""

    def wrapper(cls):
        cls._direct_names = ModelIO(inputs=inputs, outputs=outputs, residuals=residuals)
        return cls

    return wrapper


def state_space_io(
    states: Tuple[str] = (),
    inputs: Tuple[str] = (),
    outputs: Tuple[str] = (),
    con_outputs: Tuple[str] = (),
    residuals: Tuple[str] = (),
):
    """Decorator to set the input and output names of a StateSpaceModel"""

    def wrapper(cls):

        # TODO: an issue with using a decorator instead of directly in the class is that
        # the decorator is executed during import time, which might be harder to debug.
        if not issubclass(cls, StateSpaceModel):
            raise RuntimeError(
                "state_space_io can only be used for setting the io for "
                "StateSpaceModel. Use model_io for other models"
            )

        cls._direct_names = StateSpaceIO(
            states=states,
            states_dot=states,  # use the same name as states for the states_dot
            inputs=inputs,
            outputs=outputs,
            con_outputs=con_outputs,
            residuals=residuals,
        )

        return cls

    return wrapper


class ModelReturn(NamedTuple):
    """Return data structure for a static model."""

    outputs: Dict = {}
    residuals: Dict = {}


class StateSpaceModelReturn(NamedTuple):
    """Return data structure for state space model."""

    states_dot: Dict = {}
    outputs: Dict = {}
    con_outputs: Dict = {}
    residuals: Dict = {}


class ArrayModelReturn(NamedTuple):
    """Return data structure for a static model in array forms."""

    outputs: lnp.ndarray = np.array([])
    residuals: lnp.ndarray = np.array([])


class ArrayStateSpaceModelReturn(NamedTuple):
    """Return data structure for state space model in array forms."""

    # NOTE: we use np empty array instead of lnp.array([]) here because the type is
    # not really affected by user backend choice as it's determined already during the
    # import time as the default values.
    states_dot: lnp.ndarray = np.array([])
    outputs: lnp.ndarray = np.array([])
    con_outputs: lnp.ndarray = np.array([])
    residuals: lnp.ndarray = np.array([])


class Model(CompositeModel):
    """Abstract class for mathematical models of the simplest form."""

    # parameters of the model.
    # TODO: need to constrain this more.
    _params: Dict[str, Any]

    # TODO: not designed yet
    model_config: Dict[str, Any]

    def __init__(
        self, model_config: Dict[str, Any] = {}, params: Dict[str, Any] = {},
    ):
        super().__init__(model_config=model_config, params=params)

        # Build instance specific name attributes
        self._construct_io_names()

    @abstractmethod
    def forward(self, *args, **kwargs):
        """Abstract method for calling the model.

        We name the method to 'forward' to emphasis it's the forward execution of a
        model.h
        """
        pass

    def apply_and_forward(self, inputs, params):
        self.set_recursive_params(params)
        return self.forward(inputs)

    def apply_and_forward_with_arrays(self, inputs, params, con_outputs):
        self.set_recursive_params(params)
        return self.forward_with_array(inputs, con_outputs)

    def _construct_io_names(self):
        """Create model io names while also taking into account submodels compositoin"""

        self.names = ModelIO(
            inputs=self._direct_names.inputs,
            residuals=self._direct_names.residuals,
            outputs=self._direct_names.outputs
            + tuple(self._collect_children_outputs()),
        )

    def _collect_children_outputs(self):
        """Collect all children outputs and prefix them with submodel_name
        
        
        eg: the 'power' output of the 'engine' submodel becomes 'engine.power'
        """
        children_outputs = []
        if not self.is_leaf():
            for submodel_name, model in self._submodels.items():
                children_outputs += [
                    submodel_name + "." + n for n in model.names.outputs
                ]
        return children_outputs

    def combine_submodel_outputs(self, **kwargs):
        """combine the outputs from submodels into large dictionary
        
        kwargs: {name_of_submodel: vector_of_outputs}
        """
        combined_dict = {}
        for submodel_name, submodel_outputs in kwargs.items():
            # TODO: maybe we could convert the following to a helper method?
            combined_dict.update(
                {submodel_name + "." + n: v for n, v in submodel_outputs.items()}
            )

        return combined_dict

    @classmethod
    def get_direct_group_names(cls, group: str) -> Tuple[str, ...]:
        """Return the direct names of variables inside an IO group."""

        return getattr(cls._direct_names, group)

    def get_group_names(self, group: str) -> Tuple[str, ...]:
        """Return the names of variables inside an IO group."""

        return getattr(self.names, group)

    def get_var_index(self, group: str, name: str) -> int:
        if name not in self.get_group_names(group):
            raise KeyError(
                f"{name} doesnot exist in group: {group}. Valid names are {self.get_group_names(group)} "
            )
        return self.get_group_names(group).index(name)

    def get_var_index_in_flat(self, group: str, name: str) -> int:
        """Return variable index in the flat input"""

        # offset before the group
        offsets = np.cumsum([self.get_num_vars(g) for g in self._implicit_inputs])[:-1]
        offsets = dict(zip(self._implicit_inputs, np.insert(offsets, 0, 0)))

        return self.get_var_index(group=group, name=name) + offsets[group]

    def get_group_indices_in_flat(self, group: str) -> np.ndarray:
        """Return the indices for a group of varialbes in the flat input."""
        return np.array(
            [self.get_var_index_in_flat(group, n) for n in self.get_group_names(group)],
            dtype=np.int32,
        )

    def get_num_vars(self, group: str) -> int:
        return len(self.get_group_names(group))

    # TODO: these are convenience methods. Can we dynamically generate them?
    def get_input(self, inputs: lnp.ndarray, name: str) -> float:
        return inputs[self.get_var_index(group="inputs", name=name)]

    def get_output(self, outputs: lnp.ndarray, name: str) -> float:
        return outputs[self.get_var_index(group="outputs", name=name)]

    def forward_with_arrays(self, inputs):
        inputs = _array_to_dict(self.names.inputs, inputs)
        model_return = self.forward(inputs)

        # Convert from dictionary to arrays for the outputs
        kwargs = {
            g: self.make_vector(g, **getattr(model_return, g))
            for g in model_return._fields
        }

        return ArrayModelReturn(**kwargs)

    @property
    def num_inputs(self):
        return self.get_num_vars(group="inputs")

    @property
    def num_outputs(self):
        return self.get_num_vars(group="outputs")

    @property
    def num_residuals(self):
        return self.get_num_vars(group="residuals")

    @property
    def num_con_outputs(self):
        return self.get_num_vars(group="con_outputs")

    def make_const_vector(self, group: str, val: float = 0.0):
        """Create an array of constant value representing a group."""

        return np.ones(self.get_num_vars(group=group)) * val

    def make_random_vector(self, group: str):
        """Create a random vector representing a group

        We make all the values positive for now.
        """
        return np.abs(np.random.randn(self.get_num_vars(group=group)))

    def _check_keys(self, group, kwargs):
        # check missing names
        input_set = set(kwargs.keys())
        expected_set = set(self.get_group_names(group))
        if not input_set == expected_set:
            if expected_set.issubset(input_set):
                logger.warning(
                    f"{input_set - expected_set} are not valid {group} names."
                    " These values are ignored."
                )
            else:
                raise ValueError(
                    f"Missing {group} values for {expected_set - input_set}"
                )

    def make_vector(self, group: str, **kwargs) -> lnp.ndarray:
        """Create a state vector from kwargs. All values must be provided."""
        self._check_keys(group, kwargs)
        return lnp.array(list(kwargs[name] for name in self.get_group_names(group)))

    def make_dict(self, group: str, **kwargs) -> Dict[str, Any]:
        """Create a dictionary from kwargs. All values must be provided.
        
        This is actually just a thing wrapper on the standard dictionary construction,
        but it additionally checks if all the necessary keys exist
        """
        self._check_keys(group, kwargs)
        return kwargs

    def make_const_dict(self, group, value: float) -> Dict[str, Any]:
        """Create a dictionary for a group filled with constant values."""
        return {n: value for n in self.get_group_names(group)}

    def plot(self, *args, **kwargs):
        raise NotImplementedError


class StateSpaceModel(Model):
    """Compare to a standard model, now we have states."""

    # We name the inputs to the system simply "inputs" instead of "controls" in control
    # literature. This is so that StateSpaceModel can be naturally seen as a child of
    # the standard Model, where the only difference is the addition of states.

    # TODO: maybe we need a better name for this as this is now only used for the
    # flat input calls which is then used in ocp
    # Maybe explicit_inputs, and implicit_inputs? But for explicit formulation, we also
    # need the outputs defined, so it's not just 'inputs'
    _implicit_inputs: Tuple[str, str, str, str] = (
        "states",
        "inputs",
        "states_dot",
        "con_outputs",
    )

    def __init__(
        self, params: Dict[str, Any] = {}, model_config: Dict[str, Any] = {},
    ):
        super().__init__(model_config=model_config, params=params)
        self._check_names()

    @abstractmethod
    def forward(
        self, states: lnp.ndarray, inputs: lnp.ndarray, mesh: float
    ) -> StateSpaceModelReturn:
        """The canonical form.

        x_dot = f(x, u, t, p)
        y     = g(x, u, t, p)
        """
        pass

    def apply_and_forward(self, states, inputs, mesh, params):
        self.set_recursive_params(params)
        return self.forward(states, inputs, mesh)

    def apply_and_forward_with_arrays(self, states, inputs, mesh, params, con_outputs):
        self.set_recursive_params(params)
        return self.forward_with_arrays(states, inputs, mesh, con_outputs=con_outputs)

    def make_state_space_model_return(
        self,
        states_dot: lnp.ndarray,
        outputs: lnp.ndarray = None,
        residuals: lnp.ndarray = None,
    ) -> StateSpaceModelReturn:
        """Thin wrapper for StateSpaceModelReturn to handle con_outputs automatically."""
        kwargs = {"states_dot": states_dot}
        if outputs is not None:
            kwargs["outputs"] = outputs

        if residuals is not None:
            kwargs["residuals"] = residuals

        return StateSpaceModelReturn(**kwargs)

    def _construct_io_names(self):
        """Create model io names while also taking into account submodels compositoin.
        
        Similar to Model._construct_io_names, but now needs to operate on more groups
        for state space model.
        """

        self.names = StateSpaceIO(
            inputs=self._direct_names.inputs,
            states=self._direct_names.states,
            states_dot=self._direct_names.states_dot,
            con_outputs=self._direct_names.con_outputs,
            residuals=self._direct_names.residuals,
            outputs=self._direct_names.outputs
            + tuple(self._collect_children_outputs()),
        )

    def _check_names(self):
        # Ensure con_outputs all exist
        for c in self.get_group_names("con_outputs"):
            if c not in self.get_group_names("outputs"):
                raise ValueError(f"constraint outputs {c} not found in outputs")

    def _extract_con_outputs(self, outputs: Dict[str, Any]) -> Dict[str, Any]:
        return {c: outputs[c] for c in self.get_group_names("con_outputs")}

    # HACK: need num_implicit_var to
    # 1) create casadi variable size
    # 2) create sparsity structure
    # -- this is really decided by the ocp formulation
    @property
    def num_implicit_var(self):
        return sum([self.get_num_vars(g) for g in self._implicit_inputs])

    @property
    def num_states(self):
        return self.get_num_vars(group="states")

    def get_state(self, states: lnp.ndarray, name: str) -> float:
        return states[self.get_var_index(group="states", name=name)]

    def forward_with_arrays(self, states, inputs, mesh, con_outputs):

        states = _array_to_dict(self.names.states, states)
        inputs = _array_to_dict(self.names.inputs, inputs)
        model_return = self.forward(states, inputs, mesh)

        # Convert from dictionary to arrays for the outputs
        kwargs = {
            g: self.make_vector(g, **getattr(model_return, g))
            for g in model_return._fields
            if g != "con_outputs"
        }

        # HACK: we could unify this a bit with self.make_vector
        kwargs["con_outputs"] = lnp.array(
            [model_return.outputs[c] for c in con_outputs]
        )

        return ArrayStateSpaceModelReturn(**kwargs)

    def implicit(
        self,
        states: lnp.ndarray,
        inputs: lnp.ndarray,
        states_dot: lnp.ndarray,
        con_outputs: lnp.ndarray,
        mesh: float,
        con_output_names: Tuple[str],
    ) -> lnp.ndarray:
        """Implicit form: f(x, u, t, x_dot, y, p) = 0

        This is the base class method for models with a forward method to be turned into
        an implicit model.

        For models that are really implicit, the user should implement the implicit form
        directly.

        the order of the outputs should be: [states_dot, con_outputs, residuals]. This
        is a hard-coded limitation of the current design. -> FIXME
        """

        model_return = self.forward_with_arrays(
            states, inputs, mesh, con_outputs=con_output_names
        )

        # TODO: here we return an array, but maybe we should at least always check
        # (especially for user-defined ones) that the residual size is correct.

        res = lnp.vector_concat(
            [
                model_return.states_dot - states_dot,
                model_return.con_outputs - con_outputs,
                model_return.residuals,
            ]
        )
        return res

    def _split_flat_vars(self, flat_vars: lnp.ndarray):
        split_indices = list(
            np.cumsum([self.get_num_vars(g) for g in self._implicit_inputs])[:-1]
        )
        list_vars = lnp.vector_split(flat_vars, split_indices)

        return dict(zip(self._implicit_inputs, list_vars))

    def _apply_and_flat_implicit(
        self, flat_vars: lnp.ndarray, mesh: float, params, con_outputs
    ) -> lnp.ndarray:
        self.set_recursive_params(params)
        dict_vars = self._split_flat_vars(flat_vars)

        return self.implicit(**dict_vars, mesh=mesh, con_output_names=con_outputs)

    def _implicit_jac(self, flat_vars, mesh, params):
        raise NotImplementedError(
            "_implicit_jac and _implicit_jacobianstructure needs to be implemented to "
            "use custom jacobians"
        )

    def _implicit_jacobianstructure(self):
        raise NotImplementedError(
            "_implicit_jac and _implicit_jacobianstructure needs to be implemented to "
            "use custom jacobians"
        )

    def _implicit_hess(self, flat_vars, mesh, params, mult):
        raise NotImplementedError(
            "_implicit_hess and _implicit_hessianstructure needs to be implemented to "
            "use custom hessian"
        )

    def _implicit_hessianstructure(self):
        raise NotImplementedError(
            "_implicit_hess and _implicit_hessianstructure needs to be implemented to "
            "use custom hessian"
        )

    def _make_batched_forward(
        self, backend: str, con_outputs: Tuple[str], CasType: type = cas.MX
    ):
        def wrapped_fn(states, inputs, mesh, params):
            return self.apply_and_forward_with_arrays(
                states, inputs, mesh, params, con_outputs=con_outputs
            )

        if backend == "jax":
            self._batched_forward = lnp.use_backend("jax")(
                jit(vmap(wrapped_fn, in_axes=[0, 0, 0, None]))
            )
        elif backend == "casadi":
            # HACK: lots of duplicate code, factorize
            params = self.get_recursive_params()
            flat_params, unravel = params.tree_ravel()

            cas_flat_params = CasType.sym("params", len(flat_params))
            cas_dict_params = unravel(cas_flat_params)

            mesh = CasType.sym("distance")
            states = CasType.sym("states", self.num_states)
            inputs = CasType.sym("inputs", self.num_inputs)

            # Only the model calls need to go inside the context manager.
            with lnp.use_backend("casadi"):
                model_return = self.apply_and_forward_with_arrays(
                    states, inputs, mesh, cas_dict_params, con_outputs=con_outputs
                )

            # Generate code
            filename = "batched_forward"
            cfile = filename + ".c"
            # FIXME: path management, currently local directory only
            codegen = cas.CodeGenerator(cfile)

            codegen.add(
                cas.Function(
                    "forward", [states, inputs, mesh, cas_flat_params], [*model_return]
                )
            )
            codegen.generate()

            logger.info(f"Generated c-code with {getsize(cfile)} lines: ")
            # Call compiler if no library exists already
            with open(cfile, "rb") as f:
                file_hash = hashlib.md5()
                for chunk in iter(lambda: f.read(8192), b""):
                    file_hash.update(chunk)

            library_name = file_hash.hexdigest()
            library_path = "./" + library_name + ".so"

            if exists(library_path):
                logger.info(f"{library_path} already exists, no compliation is needed.")
            else:
                logger.info(f"Compiling casadi library {library_path}")
                cmd = ["gcc", "-fPIC", "-o2", "-shared", cfile, "-o", library_path]
                p = subprocess.Popen(cmd)
                p.wait()

            # Wrap the functions to take in dict params
            # FIXME: fixed thread number
            _mapped_forward = lnp.cmap(
                cas.external("forward", library_path),
                num_workers=32,
                in_axes=[0, 0, 0, None],
            )

            def cas_batched_forward(_states, _inputs, _mesh, _params):
                _flat_params, _ = _params.tree_ravel()
                out = _mapped_forward(_states, _inputs, _mesh, _flat_params)
                return StateSpaceModelReturn(*out)

            self._batched_forward = cas_batched_forward

            # FIXME: again, we need to set the parameters back to the type they were
            self.set_recursive_params(params)

        elif backend == "custom":

            def custom_batched_forward(_states, _inputs, _mesh, _params):
                self.set_recursive_params(_params)
                out = lnp.lmap(self.forward)(_states, _inputs, _mesh)
                return StateSpaceModelReturn(*out)

            self._batched_forward = custom_batched_forward

    def batched_forward(
        self,
        states: lnp.ndarray,
        inputs: lnp.ndarray,
        mesh: float,
        params: Optional[Dict[str, Any]] = None,
    ) -> StateSpaceModelReturn:
        return self._batched_forward(states, inputs, mesh, params)

    def export_c_mex(self, cfile: str, CasType: type = cas.MX):
        """Export a state space model into c-code that is ready for mex.

        The exported function has the following API:

        states_dot, outputs, con_outputs, residuals = function(states, inputs, mesh, params)
        where each I/O is an array of the corresponding size.

        Args:
            cfile (str): path of the c-file for export, includg .c extension. Limited to
                current working directory only.
            CasType (type, optional): casadi type to use, SX or MX. Defaults to MX.

        """
        # FIXME: path management, currently local directory only, which is a limitation
        # that comes from casadi
        params = self.get_recursive_params()
        flat_params, unravel = params.tree_ravel()

        cas_flat_params = CasType.sym("params", len(flat_params))
        cas_dict_params = unravel(cas_flat_params)

        mesh = CasType.sym("distance")
        states = CasType.sym("states", self.num_states)
        inputs = CasType.sym("inputs", self.num_inputs)

        # Only the model calls need to go inside the context manager.
        with lnp.use_backend("casadi"):
            model_return = self.apply_and_forward_with_arrays(
                states, inputs, mesh, cas_dict_params
            )

        # Generate code
        codegen = cas.CodeGenerator(cfile, dict(mex=True, main=True))

        codegen.add(
            cas.Function(
                "forward", [states, inputs, mesh, cas_flat_params], [*model_return]
            )
        )

        codegen.generate()

        # Need to set the parameters back to the original params, as they were replaced
        # with casadi variables during the apply_and_forward_with_arrays
        # TODO: the same also happens to other casadi export and also jax tracing right?
        # Can we generalize this problem?
        self.set_recursive_params(params)
