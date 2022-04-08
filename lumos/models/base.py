import hashlib
import logging
import subprocess
from abc import abstractmethod
from collections import namedtuple
from os.path import exists, getsize
from typing import Any, Dict, NamedTuple, Optional, Tuple

import casadi as cas
import numpy as np
from jax import jit, vmap

import lumos.numpy as lnp
from lumos.optimal_control.nlp import MappedConstraints, JaxConstraints, CasConstraints
from lumos.models.composition import CompositeModel
from lumos.optimal_control.nlp import CasConstraints, JaxConstraints

logger = logging.getLogger(__name__)


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
        cls.names = ModelIO(inputs=inputs, outputs=outputs, residuals=residuals)
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

        states_dot = tuple([n + "_dot" for n in states])
        cls.names = StateSpaceIO(
            states=states,
            states_dot=states_dot,
            inputs=inputs,
            outputs=outputs,
            con_outputs=con_outputs,
            residuals=residuals,
        )

        return cls

    return wrapper


class ModelReturn(NamedTuple):
    """Return data structure for a static model."""

    outputs: lnp.ndarray = np.array([])
    residuals: lnp.ndarray = np.array([])


class StateSpaceModelReturn(NamedTuple):
    """Return data structure for state space model."""

    # NOTE: we use np empty array instead of lnp.array([]) here because the type is
    # not really affected by user backend choice as it's determined already during the
    # import time as the default values.
    states_dot: lnp.ndarray = np.array([])
    outputs: lnp.ndarray = np.array([])
    con_outputs: lnp.ndarray = np.array([])
    residuals: lnp.ndarray = np.array([])


class Model(CompositeModel):
    """Abstract class for mathematical models of the simplest form."""

    # Names of variables in each group.
    names: Dict[str, Tuple[str, ...]]

    # parameters of the model.
    # TODO: need to constrain this more.
    _params: Dict[str, Any]

    # TODO: not designed yet
    model_config: Dict[str, Any]

    def __init__(
        self, model_config: Dict[str, Any] = {}, params: Dict[str, Any] = {},
    ):
        super().__init__(model_config=model_config, params=params)

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

    @classmethod
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

    def make_vector(self, group: str, **kwargs) -> lnp.ndarray:
        """Create a state vector from kwargs. All values must be provided."""

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

        return lnp.array(list(kwargs[name] for name in self.get_group_names(group)))

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
            kwargs["con_outputs"] = self._extract_con_outputs(outputs)

        if residuals is not None:
            kwargs["residuals"] = residuals
        return StateSpaceModelReturn(**kwargs)

    def _check_names(self):
        # Ensure con_outputs all exist
        for c in self.get_group_names("con_outputs"):
            if c not in self.get_group_names("outputs"):
                raise ValueError(f"constraint outputs {c} not found in outputs")

    def _extract_con_outputs(self, outputs: lnp.ndarray) -> lnp.ndarray:
        con_outputs_dict = {
            c: self.get_output(outputs, c) for c in self.get_group_names("con_outputs")
        }
        return self.make_vector(group="con_outputs", **con_outputs_dict)

    @property
    def num_implicit_res(self):
        return self.num_states + self.num_con_outputs + self.num_residuals

    @property
    def num_implicit_var(self):
        return sum([self.get_num_vars(g) for g in self._implicit_inputs])

    @property
    def num_states(self):
        return self.get_num_vars(group="states")

    def get_state(self, states: lnp.ndarray, name: str) -> float:
        return states[self.get_var_index(group="states", name=name)]

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

        model_return = self.forward(states, inputs, mesh)

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
        split_indices = list(
            np.cumsum([self.get_num_vars(g) for g in self._implicit_inputs])[:-1]
        )
        list_vars = lnp.vector_split(flat_vars, split_indices)

        return dict(zip(self._implicit_inputs, list_vars))

    def _apply_and_flat_implicit(
        self, flat_vars: lnp.ndarray, mesh: float, params,
    ) -> lnp.ndarray:
        self.set_recursive_params(params)
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
        """
        if backend == "casadi":
            self._make_casadi_model_algebra_cons()
        elif backend == "jax":
            self._make_jax_model_algebra_cons()
        elif backend == "custom":
            self._make_custom_model_algebra_cons()
        else:
            raise ValueError(
                f"{backend} is not supported. Only 'jax', 'casadi' and 'custom' backends are supported."
            )

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
        # stage. See JaxConstraints
        implicit_functions = {
            "constraints": self._apply_and_flat_implicit,
        }

        # TODO: _stage_hessianstructure not yet implemented
        self.model_algebra = JaxConstraints(
            num_in=self.num_implicit_var,
            num_con=self.num_implicit_res,
            **implicit_functions,
            jacobian_structure=self._model_algebra_jacobianstructure(),
            hessian_structure=self._model_algebra_hessianstructure(),
        )

        # FIXME: handle batched_forward better
        self._batched_forward = lnp.use_backend("jax")(
            jit(vmap(self.apply_and_forward, in_axes=[0, 0, 0, None]))
        )

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
            model_return = self.apply_and_forward(states, inputs, mesh, cas_dict_params)
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
                [stage_vars, mesh, cas_flat_params, mult],
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
        def cas_batched_forward(_states, _inputs, _mesh, _params):
            _flat_params, _ = _params.tree_ravel()

            # FIXME: fixed thread number
            out = lnp.cmap(
                cas.external("forward", library_path),
                num_workers=32,
                in_axes=[0, 0, 0, None],
            )(_states, _inputs, _mesh, _flat_params)

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

        self.model_algebra = CasConstraints(
            num_in=self.num_implicit_var,
            num_con=self.num_implicit_res,
            **implicit_functions,
        )
