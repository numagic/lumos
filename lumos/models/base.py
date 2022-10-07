import hashlib
import logging
import subprocess
from abc import abstractmethod
from collections import namedtuple
from os.path import exists, getsize
from typing import Any, Dict, List, NamedTuple, Optional, Tuple

import casadi as cas
import numpy as np
from jax import jit, vmap

import lumos.numpy as lnp
from lumos.optimal_control.nlp import (
    MappedConstraints,
    JaxMappedConstraints,
    CasMappedConstraints,
)
from lumos.models.composition import CompositeModel, ParameterTree
from lumos.optimal_control.nlp import CasMappedConstraints, JaxMappedConstraints

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

    def __init__(
        self, model_config: Dict[str, Any] = {}, params: Dict[str, Any] = {},
    ):
        super().__init__(model_config=model_config, params=params)

        # Build instance specific name attributes
        self._construct_io_names()

        # Construct a buffer for submodel returns. This is used for automatic outputs
        # collection, and cleared with a _combine_submodel_outputs call
        self._clear_submodel_return_buffer()

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

    def apply_and_forward_with_arrays(self, inputs, params):
        self.set_recursive_params(params)
        return self.forward_with_array(inputs)

    def _construct_io_names(self):
        """Create model io names while also taking into account submodels compositoin"""

        self.names = ModelIO(
            inputs=self._direct_names.inputs,
            residuals=self._direct_names.residuals
            + tuple(self._collect_children_residuals()),
            outputs=self._direct_names.outputs
            + tuple(self._collect_children_outputs()),
        )

    def _collect_children_residuals(self):
        """Collect all children residuals and prefix them with submodel_name

        eg: the 'net_moment' output of the 'body' submodel becomes 'body.net_moment'
        """
        children_residuals = []
        if not self.is_leaf():
            for submodel_name, model in self._submodels.items():
                children_residuals += [
                    submodel_name + "." + n for n in model.names.residuals
                ]
        return children_residuals

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

    def _clear_submodel_return_buffer(self):
        """Create a clear submodel return buffer.

        The buffer is used for saving submodel returns after 'call_submodel'. The saved
        submodel returns will then be used for automatic outputs collection.

        The buffer must be cleared (done in _combine_submodel_outputs) before a new
        round of submodel calls.
        """
        self._submodel_return_buffer = {n: None for n in self.get_submodel_names()}

    def call_submodel(self, submodel_name: str, **kwargs) -> ModelReturn:
        """Call a submodel with keyword arguments

        Args:
            submodel_name (str): name of the submodel

        Raises:
            RuntimeError: if the submodel has already been called and its results stored
                in the buffer. This can happen if the same submodel is called a second
                time before the buffer is cleared.

        Returns:
            ModelReturn: the return from the submodel.

        This is the intended way for the user to call the submodels, instead of getting
        the submodel and calling it, as it also handles automatic submodel output
        collections.
        """

        # We call this first because it also handles errors where we retire the wrong
        # submodel
        submodel = self.get_submodel(submodel_name)

        # Make sure the submodel_returns is not populated yet. As we want to make sure
        # we always clear it before we call the submodel again to avoid result
        # contamination
        if self._submodel_return_buffer[submodel_name] is not None:
            raise RuntimeError(
                f"submodel {submodel_name} is called again before the corresponding submodel "
                "return buffer is cleared. "
            )

        # Check the required inputs are provided to the submodel (this is also why we
        # only support kwargs here)
        groups_to_check = ["inputs"]
        if isinstance(submodel, StateSpaceModel):
            groups_to_check.append("states")

        for group in groups_to_check:
            submodel._check_keys(group, kwargs[group])

        submodel_return = submodel.forward(**kwargs)

        # Store result in buffer
        self._submodel_return_buffer[submodel_name] = submodel_return

        return submodel_return

    def _combine_submodel_outputs(self):
        """combine the outputs from submodels into large dictionary

        It also:
        - checks that all submodel returns are already populated in the buffer
        - clears the buffer after the results are collected (so that we are ready for
        the next round of 'forward' call)
        """

        combined_dict = {}
        for submodel_name, submodel_return in self._submodel_return_buffer.items():

            # Check if results already exist in the buffer
            if submodel_return is None:
                raise KeyError(
                    f"submodel_return for {submodel_name} does not exist "
                    "in the buffer. Did you call `call_submodel` on it?"
                )

            # TODO: maybe we could convert the following to a helper method?
            combined_dict.update(
                {submodel_name + "." + n: v for n, v in submodel_return.outputs.items()}
            )

        # Clear buffer
        self._clear_submodel_return_buffer()

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
                raise KeyError(f"Missing {group} values for {expected_set - input_set}")

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

    def make_outputs_dict(self, **kwargs) -> Dict[str, Any]:
        """As make_dict, but specific for outputs due to submodel outputs collection."""

        submodel_outputs = self._combine_submodel_outputs()

        # Create an outputs with the current model outputs in kwargs, and submodel_outputs
        return self.make_dict(group="outputs", **kwargs, **submodel_outputs)

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
    # The order of the implicit inputs
    _implicit_inputs: Tuple[str] = ("states", "inputs", "states_dot", "con_outputs")

    def __init__(
        self, params: Dict[str, Any] = {}, model_config: Dict[str, Any] = {},
    ):
        super().__init__(model_config=model_config, params=params)
        self._check_names()

    @abstractmethod
    def forward(
        self, states: Dict[str, float], inputs: Dict[str, float], mesh: float
    ) -> StateSpaceModelReturn:
        """The canonical form.

        x_dot = f(x, u, t, p)
        y     = g(x, u, t, p)
        """
        pass

    def apply_and_forward(self, states, inputs, mesh, params):
        self.set_recursive_params(params)
        return self.forward(states, inputs, mesh)

    def apply_and_forward_with_arrays(self, states, inputs, mesh, params):
        self.set_recursive_params(params)
        return self.forward_with_arrays(states, inputs, mesh)

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
            residuals=self._direct_names.residuals
            + tuple(self._collect_children_residuals()),
            outputs=self._direct_names.outputs
            + tuple(self._collect_children_outputs()),
        )

    def _check_names(self):
        # Ensure con_outputs all exist
        for c in self.get_group_names("con_outputs"):
            if c not in self.get_group_names("outputs"):
                raise ValueError(f"constraint outputs {c} not found in outputs")

        # Ensure residuals all exist
        for c in self.get_group_names("residuals"):
            if c not in self.get_group_names("outputs"):
                raise ValueError(f"residual {c} not found in outputs")

    def set_con_outputs(self, con_outputs: Tuple[str, ...]) -> None:
        """Set the con_outputs of the model."""
        # NOTE: names is a namedtuple, so it's immutable. Using the _replace method is
        # just a workaround to change a field.
        self.names = self.names._replace(con_outputs=con_outputs)

    def _extract_residuals(self, outputs: Dict[str, Any]) -> Dict[str, Any]:
        return {c: outputs[c] for c in self.get_group_names("residuals")}

    def _extract_con_outputs(self, outputs: Dict[str, Any]) -> Dict[str, Any]:
        return {c: outputs[c] for c in self.get_group_names("con_outputs")}

    @property
    def num_implicit_res(self):
        return self.num_states + self.num_con_outputs + self.num_residuals

    @property
    def num_implicit_var(self):
        return sum([self.get_num_vars(g) for g in self._implicit_inputs])

    @property
    def num_states(self):
        return self.get_num_vars(group="states")

    @property
    def implicit_inputs(self):
        """Light protection of hidden attributes of implicit inputs"""
        return self._implicit_inputs

    def get_state(self, states: lnp.ndarray, name: str) -> float:
        return states[self.get_var_index(group="states", name=name)]

    def forward_with_arrays(self, states, inputs, mesh):

        states = _array_to_dict(self.names.states, states)
        inputs = _array_to_dict(self.names.inputs, inputs)
        model_return = self.forward(states, inputs, mesh)

        # Convert from dictionary to arrays for the outputs
        kwargs = {
            g: self.make_vector(g, **getattr(model_return, g))
            for g in model_return._fields
            if g not in ["con_outputs", "residuals"]
        }

        # TODO: this is where we extract con_outputs, does this make sense?
        kwargs["con_outputs"] = self.make_vector(
            "con_outputs", **self._extract_con_outputs(model_return.outputs)
        )

        kwargs["residuals"] = self.make_vector(
            "residuals", **self._extract_residuals(model_return.outputs)
        )

        return ArrayStateSpaceModelReturn(**kwargs)

    def implicit(
        self,
        states: lnp.ndarray,
        inputs: lnp.ndarray,
        states_dot: lnp.ndarray,
        con_outputs: lnp.ndarray,
        mesh: float,
    ) -> lnp.ndarray:
        """Implicit form: f(x, u, t, x_dot, y, p) = 0

        This is the base class method for models with a forward method to be turned into
        an implicit model.

        For models that are really implicit, the user should implement the implicit form
        directly.

        the order of the outputs should be: [states_dot, con_outputs, residuals]. This
        is a hard-coded limitation of the current design.
        """

        model_return = self.forward_with_arrays(states, inputs, mesh)

        # TODO: here we return an array, but maybe we should at least always check
        # (especially for user-defined ones) that the residual size is correct.
        #
        # TODO: maybe we should also refer to constraints by name, just like what we did
        # for the decision variables.

        # Assemble scaled residuals. We could move scales outside of the residual
        # functions so the scales are no longer compiled into the residual calls. But
        # that would require manually scaling the jacobian and hessian as well -- Doable
        # but not necessary for now.

        res = lnp.vector_concat(
            [
                model_return.states_dot - states_dot,
                model_return.con_outputs - con_outputs,
                model_return.residuals,
            ]
        )
        return res

    def _split_flat_vars(self, flat_vars: lnp.ndarray):
        """Split the flat stage variables into dictionary of arrays."""
        split_indices = list(
            np.cumsum([self.get_num_vars(g) for g in self._implicit_inputs])[:-1]
        )
        list_vars = lnp.vector_split(flat_vars, split_indices)

        return dict(zip(self._implicit_inputs, list_vars))

    def _apply_and_flat_implicit(
        self, flat_vars: lnp.ndarray, mesh: float, params,
    ) -> lnp.ndarray:
        self.set_recursive_params(params)
        # TODO: split to dict of arrays -> call in implicit with forward_with_arrays
        # -> convert to dict again, call with dict, can we simplify?
        #
        # NOTE: that's ok for states and inputs, but implicit also requires states_dot
        # and con_outputs, which we will never use as dict, and it's easier to use them
        # as arrays!
        dict_vars = self._split_flat_vars(flat_vars)

        return self.implicit(**dict_vars, mesh=mesh)

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

    def batched_forward(
        self,
        states: lnp.ndarray,
        inputs: lnp.ndarray,
        mesh: float,
        params: Optional[Dict[str, Any]] = None,
    ) -> StateSpaceModelReturn:
        return self._batched_forward(states, inputs, mesh, params)

    def make_model_algebra_cons(self, backend: str):
        """Create the model_algebra constraints that are needed for the OCP.

        FIXME: currently we also require this function to formulate the _batched_forward
        function, which we should probaly consider moving somewhere else.

        FIXME: here we direclty return the MappedConstraints (either Cas or Jax), but
        there should be one step in between where we get a single stage model algebra
        """

        # store the original parameters (and also must make a copy)
        # TODO: create a param copy method
        params = ParameterTree.from_dict(self.get_recursive_params().to_dict())

        if backend == "casadi":
            implicit_functions = self._make_casadi_model_algebra_cons()
        elif backend == "jax":
            implicit_functions = self._make_jax_model_algebra_cons()
        elif backend == "custom":
            implicit_functions = self._make_custom_model_algebra_cons()
        else:
            raise ValueError(
                f"{backend} is not supported. Only 'jax', 'casadi' and 'custom' backends are supported."
            )

        # Restore the original params (some backends would replace model params with
        # objects such as their own symbolic types or tracers during tracing)
        self.set_recursive_params(params)

        return implicit_functions

    def _model_algebra_jacobianstructure(self):
        """A pessimistic estimate for the jacobian structure of model algebra.

        NOTE: Here we rely on a few dangerous assumptions:
        1) the implicit form is a explicit turned into implicit (see model.implicit),
        with states_dot and con_outputs only acting as linear variables.
        2) the ordering of constraints are assumed to be defined by self.implicit

        TODO: if we really want to, we could use casadi to get the symbolic jac struct
        and then apply it to jax functions (and potentially other backend).
        """
        # states and inputs are involved in all constraints
        # FIXME: this relies on the ordering of the constraints
        rows = np.stack(
            [np.arange(self.num_implicit_res)] * (self.num_states + self.num_inputs)
        ).T.ravel()
        cols = np.stack(
            [
                np.concatenate(
                    [
                        self.get_group_indices_in_flat("states"),
                        self.get_group_indices_in_flat("inputs"),
                    ]
                )
            ]
            * self.num_implicit_res
        ).ravel()

        # states_dot part
        # FIXME: this relies on both the ordering of the constraints and the variables
        states_dot_rows = np.arange(self.num_states)
        states_dot_cols = self.get_group_indices_in_flat("states_dot")

        # con_outputs part
        # FIXME: this relies on both the ordering of the constraints and the variables
        con_outputs_rows = self.num_states + np.arange(self.num_con_outputs)
        con_outputs_cols = self.get_group_indices_in_flat("con_outputs")

        rows = np.concatenate([rows, states_dot_rows, con_outputs_rows])
        cols = np.concatenate([cols, states_dot_cols, con_outputs_cols])

        return rows, cols

    def _model_algebra_hessianstructure(self):
        """A pessimistic estimate for the hessian structure of model algebra.

        NOTE: states_dot and con_outputs are only linear, so no hessian entries for
        them, but for truely implicit equations where states_dot or con_outputs are
        algebraic variables they could become nonlinear! But in those case, the
        condensed approach also won't work. (because it has no explicit ODE to work on)

        TODO: if we really want to, we could use casadi to get the symbolic jac struct
        and then apply it to jax functions (and potentially other backend).
        """

        rows, cols = np.nonzero(np.ones((self.num_implicit_var, self.num_implicit_var)))

        # remove those related to states_dot and con_outputs
        idx_remove = np.hstack(
            [
                self.get_group_indices_in_flat("states_dot"),
                self.get_group_indices_in_flat("con_outputs"),
            ]
        )

        keep_rows = np.array([r not in idx_remove for r in rows])
        keep_cols = np.array([c not in idx_remove for c in cols])
        keep = keep_rows & keep_cols

        return rows[keep], cols[keep]

    def _make_jax_model_algebra_cons(self):
        # For jax, we rely on jac and hessian to compute the constraints at a later
        # stage. See JaxMappedConstraints
        implicit_functions = {
            "constraints": self._apply_and_flat_implicit,
        }

        # TODO: _stage_hessianstructure not yet implemented
        self.model_algebra = JaxMappedConstraints(
            num_in=self.num_implicit_var,
            num_con=self.num_implicit_res,
            **implicit_functions,
            jacobian_structure=self._model_algebra_jacobianstructure(),
            hessian_structure=self._model_algebra_hessianstructure(),
        )

        # FIXME: handle batched_forward better
        self._batched_forward = lnp.use_backend("jax")(
            jit(vmap(self.apply_and_forward_with_arrays, in_axes=[0, 0, 0, None]))
        )

        # FIXME: here the implicit functions are incomplete
        return implicit_functions

    def _make_custom_model_algebra_cons(self):
        implicit_functions = {
            "constraints": self._apply_and_flat_implicit,
            "jacobian": self._implicit_jac,
            "jacobian_structure": self._implicit_jacobianstructure(),
            "hessian": self._implicit_hess,
            "hessian_structure": self._implicit_hessianstructure(),
        }

        self.model_algebra = MappedConstraints(
            num_in=self.num_implicit_var,
            num_con=self.num_implicit_res,
            **implicit_functions,
        )

        def custom_batched_forward(_states, _inputs, _mesh, _params):
            self.set_recursive_params(_params)
            out = lnp.lmap(self.forward)(_states, _inputs, _mesh)
            return StateSpaceModelReturn(*out)

        self._batched_forward = custom_batched_forward

        return implicit_functions

    def _make_casadi_model_algebra_cons(self, CasType: type = cas.MX):
        # NOTE: for large linear operations, like those in FC layers, MX is much faster
        # than SX both for compilation and executtion
        params = self.get_recursive_params()
        flat_params, unravel = params.tree_ravel()

        cas_flat_params = CasType.sym("params", len(flat_params))
        cas_dict_params = unravel(cas_flat_params)

        mesh = CasType.sym("distance")
        states = CasType.sym("states", self.num_states)
        inputs = CasType.sym("inputs", self.num_inputs)
        stage_vars = CasType.sym("stage_vars", self.num_implicit_var)
        mult = CasType.sym("mult", self.num_implicit_res)

        # Only the model calls need to go inside the context manager.
        with lnp.use_backend("casadi"):
            model_return = self.apply_and_forward_with_arrays(
                states, inputs, mesh, cas_dict_params
            )
            res = self._apply_and_flat_implicit(stage_vars, mesh, cas_dict_params)
            lagrange = lnp.dot(mult, res)

        jac = cas.jacobian(res, stage_vars)
        lagrange_hessian, lagrange_gradient = cas.hessian(lagrange, stage_vars)

        # Generate code
        filename = "nlpfunctions"
        cfile = filename + ".c"
        # FIXME: path management, currently local directory only
        codegen = cas.CodeGenerator(cfile)

        codegen.add(
            cas.Function(
                "forward", [states, inputs, mesh, cas_flat_params], [*model_return]
            )
        )
        codegen.add(
            cas.Function("implicit_con", [stage_vars, mesh, cas_flat_params], [res])
        )
        codegen.add(
            cas.Function("implicit_jac", [stage_vars, mesh, cas_flat_params], [jac])
        )
        codegen.add(
            cas.Function(
                "implicit_hess",
                [stage_vars, mult, mesh, cas_flat_params],
                [lagrange_hessian],
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

        # add sparsity structure
        # Can we not get this from the symbolic SX? eg, jac.sparsity(), but then what?
        # This get_triplet interface almost looks like a bug...
        # [*row_indices, [*col_indices]] is what is returned
        # see: http://casadi.sourceforge.net/api/html/d5/da8/classcasadi_1_1Sparsity.html#a1f3eed93488c3cf121f47bec4956927f
        *jac_rows, jac_cols = jac.sparsity().get_triplet()
        *hess_rows, hess_cols = lagrange_hessian.sparsity().get_triplet()

        implicit_functions = {
            "constraints": cas.external("implicit_con", library_path),
            "jacobian": cas.external("implicit_jac", library_path),
            "hessian": cas.external("implicit_hess", library_path),
            "jacobian_structure": (np.array(jac_rows), np.array(jac_cols)),
            "hessian_structure": (np.array(hess_rows), np.array(hess_cols)),
        }

        self.model_algebra = CasMappedConstraints(
            num_in=self.num_implicit_var,
            num_con=self.num_implicit_res,
            **implicit_functions,
        )
        return implicit_functions

    def export_c_code(
        self,
        cfile: str,
        CasType: type = cas.MX,
        options: Dict[str, Any] = None,
        includes: List[str] = None,
    ):
        """Export a state space model into c-code using the casadi backend.

        The exported function has the following API:

        states_dot, outputs, con_outputs, residuals = function(states, inputs, mesh, params)
        where each I/O is an array of the corresponding size.

        Args:
            cfile (str): path of the c-file for export, includg .c extension. Limited to
                current working directory only.
            CasType (type, optional): casadi type to use, SX or MX. Defaults to MX.
            options (Dict[str, Any], optional): code generator options for casadi. See:
            https://web.casadi.org/docs/#generating-c-code. Defaults to None.
            includes (List[str], optional): header files to include. Defaults to None.

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
        if options is None:
            options = {}
        codegen = cas.CodeGenerator(cfile, options)
        codegen.add(
            cas.Function(
                "forward", [states, inputs, mesh, cas_flat_params], [*model_return]
            )
        )

        if includes:
            for inc in includes:
                codegen.add_include(inc)

        codegen.generate()

        # Need to set the parameters back to the original params, as they were replaced
        # with casadi variables during the apply_and_forward_with_arrays
        # TODO: the same also happens to other casadi export and also jax tracing right?
        # Can we generalize this problem?
        self.set_recursive_params(params)
