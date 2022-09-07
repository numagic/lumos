import logging
import re
from abc import ABC
from functools import partial
from os.path import exists
from timeit import default_timer as timer
from typing import Any, Callable, Dict, List, Optional, Tuple

import cyipopt
import jax.numpy as jnp
import numpy as np
import jax
from scipy.sparse import csc_matrix

import lumos.numpy as lnp
from lumos.numpy import cmap, lmap

logger = logging.getLogger(__name__)

# NOTE: here a bug was once intorduced due to errors in varaible ordering. This is
# very error prune!
def _make_lagrangian(constraints: Callable) -> Callable:
    """Create a lagrangian function from given objective and constraints

    Args:
        constraints (Callable): constraint function: g(x)

    Returns:
        Callable: lagrangian function:
        L(x, lambda, obj_factor) = obj_factor*f(x) + dot(lagrange, constraints(x))

        Note here the obj_factor is not in the canonical lagrangian definition but is an
        implementation requirement from IPOPT
    """

    # TODO: the input signaure is not very generic, especially with the mesh inputs.
    def _lagrangian(*args):
        """Lagrangian is just a helper function, we never use it directly

        It is only used to get the hessian of the lagrangian via autodiff
        """

        # Split the arguments
        # FIXME: hard-coded order for lagrangian!
        x, lagrange, *args_to_func = args
        return jnp.dot(lagrange, constraints(x, *args_to_func))

    return _lagrangian


class BaseConstraints:
    def __init__(
        self,
        num_in: int,
        num_con: int,
        constraints: Callable,
        jacobian: Callable,
        hessian: Callable,
        jacobian_structure: Optional[Tuple[np.ndarray, np.ndarray]] = None,
        hessian_structure: Optional[Tuple[np.ndarray, np.ndarray]] = None,
    ):

        # NOTE: cyipopt checks the problem size against int, which would return
        # false for numpy.int types! eg, isinstance(np.sum([1, 2, 3]), int) would return
        # False!
        # see: https://github.com/mechmotum/cyipopt/blob/d6841beacb46a340b4c88465159dab9724ee156e/cyipopt/cython/ipopt_wrapper.pyx#L282
        assert isinstance(
            num_in, int
        ), f"num_in must have type int, but got {type(num_in)}"

        assert isinstance(
            num_con, int
        ), f"num_in must have type int, but got {type(num_con)}"

        # NOTE: we use a lot of monkey patch, is it controversial?
        self.num_in = num_in
        self.num_con = num_con
        self._constraints = constraints
        self._jacobian = jacobian
        self._hessian = hessian

        # Additional sparsity inside each block
        if jacobian_structure is None:
            self.has_jacobian_sparsity = False
            self._jacobian_structure = np.nonzero(np.ones((num_con, num_in)))
        else:
            # If it has special jacobian structure, we store the jacobian structure.
            # Note that the jacobian structure does NOT have to be a flat array, as long
            # as the flattened 'view' of the underlying data is consistent with the
            # jacobian values
            self.has_jacobian_sparsity = True
            self._jacobian_structure = jacobian_structure

        if hessian_structure is None:
            self.has_hessian_sparsity = False
            self._hessian_structure = np.nonzero(np.ones((num_in, num_in)))
        else:
            self.has_hessian_sparsity = True
            self._hessian_structure = hessian_structure

        # Set the default scales
        self._input_scales = np.ones(self.num_in)
        self._con_scales = np.ones(self.num_con)
        self.update_jac_scales()
        self.update_hess_scales()

    def constraints(self, x, *args, **kwargs):
        return (
            self._constraints(x * self._input_scales, *args, **kwargs)
            / self._con_scales
        )

    def jacobian(self, x, *args, **kwargs):
        return (
            self._jacobian(x * self._input_scales, *args, **kwargs) / self._jac_scales
        )

    def hessian(self, x, lagrange, *args, **kwargs):
        # Scaling the contribution of the constraints to the hessian is equivalent to
        # scaling the lagrangian multipliers corresponding to the constraints

        return (
            self._hessian(
                x * self._input_scales, lagrange / self._con_scales, *args, **kwargs
            )
            / self._hess_scales
        )

    def jacobianstructure(self):
        return self._jacobian_structure

    def hessianstructure(self):
        return self._hessian_structure

    def get_csc_jacobian(self, x):
        """Helper function to return the csc matrix using the sparse entries"""
        vals = self.jacobian(x)
        rows, cols = self.jacobianstructure()
        return csc_matrix(
            (vals.ravel(), (rows.ravel(), cols.ravel())), shape=self.jac_shape
        )

    def get_csc_hessian(self, x, lagrange):
        """Helper function to return the csc matrix using the sparse entries"""
        vals = self.hessian(x, lagrange)
        rows, cols = self.hessianstructure()
        return csc_matrix(
            (vals.ravel(), (rows.ravel(), cols.ravel())), shape=self.hess_shape
        )

    def set_input_scales(self, scales: np.ndarray):
        self._input_scales = scales
        self.update_jac_scales()
        self.update_hess_scales()

    def set_con_scales(self, scales: np.ndarray):
        self._con_scales = scales
        self.update_jac_scales()

    def update_jac_scales(self):
        """Update the jacobian scale.

        The jacobian is represented in a sparse format, so we only needs an array to
        scale the jac values. This needs to be called when the input and con are scaled.

        f:          y=f(x)
        f_scaled:   y_scaled = f(x_scaled*input_scale)/con_scale
        df_scaled/dx_scaled = df/dx / jac_scales

        where jac_scales for the entry of (row, col) has value (con_scale/input_scale)
        """
        # update jacobian value scales.
        rows, cols = self.jacobianstructure()
        self._jac_scales = self._con_scales[rows] / self._input_scales[cols]

    def update_hess_scales(self):
        rows, cols = self.hessianstructure()
        self._hess_scales = 1 / (self._input_scales[rows] * self._input_scales[cols])

    @property
    def jac_shape(self):
        return (self.num_con, self.num_in)

    @property
    def hess_shape(self):
        return (self.num_in, self.num_in)


class MappedConstraints(BaseConstraints):
    map_func: Callable = staticmethod(lmap)
    map_args: Dict[str, Dict[str, Any]] = {
        "constraints": {"in_axes": [0, 0, None]},
        "jacobian": {"in_axes": [0, 0, None]},
        "hessian": {"in_axes": [0, 0, 0, None]},
    }

    def __init__(
        self,
        num_in: int,
        num_con: int,
        constraints: Callable,
        jacobian: Callable,
        hessian: Callable,
        jacobian_structure: Optional[Tuple[np.ndarray, np.ndarray]] = None,
        hessian_structure: Optional[Tuple[np.ndarray, np.ndarray]] = None,
    ):
        super().__init__(
            num_in,
            num_con,
            constraints,
            jacobian,
            hessian,
            jacobian_structure,
            hessian_structure,
        )

        # HACK: the input signature is actually prety clear (var, mesh, params), should we
        # make them explicitly clear and rule out other useages? (which we could support
        # but we make it clear we don't suppor them now)

        # Create mapped functions
        self.mapped_constraints = self.map_func(
            self._constraints, **self.map_args["constraints"]
        )
        self.mapped_jacobian = self.map_func(
            self._jacobian, **self.map_args["jacobian"]
        )
        # HACK: in_axes args are different for hessian. And potentially should align with
        # the functions? (num of arguments, and order)
        # For the model func, as soon as the unit func are decided, the in_axes are also
        # decided. So these are decided inside model.base
        self.mapped_hessian = self.map_func(self._hessian, **self.map_args["hessian"])


class JaxMappedConstraints(MappedConstraints):
    map_func: Callable = staticmethod(jax.vmap)

    def __init__(
        self,
        num_in: int,
        num_con: int,
        constraints: Callable,
        jacobian_structure: Optional[Tuple[np.ndarray, np.ndarray]] = None,
        hessian_structure: Optional[Tuple[np.ndarray, np.ndarray]] = None,
    ):

        # Apply additional sparsity structure as jax doesn't by default keep track of
        # the sparsity.
        def _wrap_extract_sparse_vals(fn, rows, cols):
            def _extract_sparse_vals(*args):
                return fn(*args)[rows, cols]

            return _extract_sparse_vals

        jacobian = jax.jacobian(constraints)
        hessian = jax.hessian(_make_lagrangian(constraints))

        if jacobian_structure is not None:
            rows, cols = jacobian_structure
            jacobian = _wrap_extract_sparse_vals(jacobian, rows, cols)

        if hessian_structure is not None:
            rows, cols = hessian_structure
            hessian = _wrap_extract_sparse_vals(hessian, rows, cols)

        super().__init__(
            num_in,
            num_con,
            constraints,
            jacobian,
            hessian,
            jacobian_structure,
            hessian_structure,
        )

        # Enforce backend and jit
        self.mapped_constraints = lnp.use_backend("jax")(
            jax.jit(self.mapped_constraints)
        )
        self.mapped_jacobian = lnp.use_backend("jax")(jax.jit(self.mapped_jacobian))
        self.mapped_hessian = lnp.use_backend("jax")(jax.jit(self.mapped_hessian))


class CasMappedConstraints(MappedConstraints):
    map_func: Callable = staticmethod(cmap)
    map_args: Dict[str, Dict[str, Any]] = {
        "constraints": {"in_axes": [0, 0, None], "sparse": False, "num_workers": 32},
        "jacobian": {"in_axes": [0, 0, None], "sparse": True, "num_workers": 32},
        "hessian": {"in_axes": [0, 0, 0, None], "sparse": True, "num_workers": 32},
    }


class LinearConstraints(BaseConstraints):
    def __init__(
        self,
        num_in: int,
        num_con: int,
        constraints: Callable,
        jacobian: Callable,
        jacobian_structure: Tuple[np.ndarray, np.ndarray],
        cache_jacobian: bool = True,
    ):
        """A simplified IO for linear constraints.

        - no hessian is needed (default to empty)
        - jacobian is constant, so we get the option to cache it (default: True).
        """

        # Linear, so no hessian.
        hessian = lambda x, lagrange: np.array([])
        hessian_structure = (np.array([], dtype=int), np.array([], dtype=int))

        # And jacobian is constant
        if cache_jacobian:
            # Linear constriants allow us to compute the jacobian once and then cache it.
            jac_val = jacobian(np.ones(num_in))
            jacobian_to_use = lambda x: jac_val
        else:
            jacobian_to_use = jacobian

        super().__init__(
            num_in,
            num_con,
            constraints,
            jacobian_to_use,
            hessian,
            jacobian_structure,
            hessian_structure,
        )


class BaseObjective:
    def __init__(
        self,
        num_in: int,
        objective: Callable,
        gradient: Callable,
        hessian: Callable,
        hessian_structure: Optional[Tuple[np.ndarray, np.ndarray]] = None,
    ):
        """Create an objective object that can be used by OCP.

        Args:
            num_in (int): number of inputs, or decision variables

            objective (Callable): an unscaled function f(x) that takes in the input x
            and returns a scalar objective value.

            gradient (Callable): an unscaled function g(x) that takes in the input x and
            returns an array that is the same size as x.

            hessian (Callable): an unscaled function h(x) that returns a 1d array of the
            non-zero elements in the hessian, that has the same length as the indicdes
            in hessian_structrue.

            hessian_structure (Optional[Tuple[np.ndarray, np.ndarray]], optional): a
            tuple of 2 equal-size arrays of (rows, cols) that gives the row and column
            indices of the non-sparse elements. If not given, then it is assumed the
            hessian is fully dense.
        """

        self.num_in = num_in
        self._objective = objective
        self._gradient = gradient
        self._hessian = hessian
        if hessian_structure is None:
            self._hessian_structure = np.nonzero(np.ones((num_in, num_in)))
            self._sparse_hess = False
        else:
            self._hessian_structure = hessian_structure
            self._sparse_hess = True

        # Set the default scales
        self._input_scales = np.ones(self.num_in)
        self.update_hess_scales()

    def set_input_scales(self, scales: np.ndarray):
        """Set the input scale to be used for the objective.

        Args:
            scales (np.ndarray): an array that is the same size as the decision variable
            and maps the scaled varialbes x_hat to the unscaled ones:
            x = scale * x_hat
        """

        self._input_scales = scales
        self.update_hess_scales()

    def update_hess_scales(self):
        rows, cols = self.hessianstructure()
        self._hess_scales = 1 / (self._input_scales[rows] * self._input_scales[cols])

    def objective(self, x: np.ndarray) -> float:
        """Call the objective function with a scaled inputs

        Args:
            x (np.ndarray): scaled inputs

        Returns:
            float: the objective value
        """
        return self._objective(x * self._input_scales)

    def gradient(self, x: np.ndarray) -> np.ndarray:
        """Call the gradient with scaled inputs

        Args:
            x (np.ndarray): scaled inputs

        Returns:
            np.ndarray: the gradient of the objective w.r.t. the scaled inputs.
        """
        return self._gradient(x * self._input_scales) * self._input_scales

    def hessianstructure(self) -> Tuple[np.ndarray, np.ndarray]:
        """Return the sparsity structure of the hessian

        Returns:
            Tuple[np.ndarray, np.ndarray]: a tuple of 2 equal-size arrays of
            (rows, cols) that gives the row and column indices of the non-sparse
            elements.
        """
        return self._hessian_structure

    def hessian(self, x: np.ndarray) -> np.ndarray:
        """Call the hessian with scaled inputs.

        Args:
            x (np.ndarray): scaled inputs.

        Returns:
            np.ndarray: the non-sparse elements of the hessian as an array. Must be the
            same size as the indicer from hessianstructure.
        """
        if self._sparse_hess:
            return self._hessian(x * self._input_scales) / self._hess_scales
        else:
            return self._hessian(x * self._input_scales) / self._hess_scales


class NLPFunction(ABC):
    """Base class for nonlinear programming problem for IPOPT"""

    hessian_approximation: str = "limited-memory"  # "limited-memory" or "exact"

    # number of iterations used
    _num_iter: int = None
    # Decision variable used at last objective function callback
    _last_iter_dec_var: np.ndarray = None

    def __init__(self):

        pass

    def objective(self, x):
        # Store unscaled last iter decision variable, and then call the real objective
        # functions
        # NOTE: during initial tracing, the type of x would be a jax tracer object
        # but later it will be just numpy array.
        #
        # Ideally we would store this in the 'intermediate' callback, but that callback
        # API does not provide the last decision variable used
        self._last_iter_dec_var = x
        return self._compute_objective(x)

    def _compute_objective(self, x):
        """The objective function to be over-written

        This is seperated from self.objective because we want to add additional hooks to
        the objective other than the computation, such as to store the last iteration of
        decision variables used
        """
        pass

    # TODO: should we move the jax.jit somewhere else?
    @partial(jax.jit, static_argnums=(0,))
    def gradient(self, x):
        return jax.grad(self._compute_objective)(x)

    def constraints(self, x):
        pass

    @partial(jax.jit, static_argnums=(0,))
    def jacobian(self, x):
        return jax.jacobian(self.constraints)(x)

    def lagrangian(
        self, x: jnp.ndarray, lagrange: jnp.ndarray, obj_factor: float
    ) -> float:
        """Lagrangian as defined by IPOPT's usege.

        See: https://coin-or.github.io/Ipopt/INTERFACES.html
        """
        return obj_factor * self.objective(x) + jnp.dot(lagrange, self.constraints(x))

    @partial(jax.jit, static_argnums=(0,))
    def hessian(
        self, x: jnp.ndarray, lagrange: jnp.ndarray, obj_factor: float
    ) -> jnp.ndarray:
        """Autograd hessian of the lagrangian"""

        hessian_func = jax.hessian(self.lagrangian, argnums=0)
        hessian_matrix = hessian_func(x, lagrange, obj_factor)

        # Always return in sparse triplet form
        return hessian_matrix[self.hessianstructure()]

    def hessianstructure(self) -> Tuple[np.ndarray, np.ndarray]:
        """IPOPT callback for hessian structure. This is dense."""

        return np.triu_indices(self.num_dec)

    def _construct_ipopt_problem(
        self, ipopt_options: Dict[str, Any], dec_var_scales: Optional[np.ndarray] = None
    ):
        """Construct an ipopt problem object"""

        # TODO: Is this the best place to scale the lower and upper bounds?
        # Advantage:
        # 1) the user doesn't need to touch scaled variables ever (just unscaled ones
        # in their more understandable units)
        # 2) we still have .lb and .ub as unscaled versions, which the user can more
        # easily check and use
        # Disadvantage:
        # 1) the handling of scales are a little bit scattered, making future dev/debug
        # potentially more difficult
        nlp = cyipopt.Problem(
            n=self.num_dec,
            m=self.num_con,
            problem_obj=self,  # this is particularly concerning...
            lb=self.lb / self._dec_var_scales,
            ub=self.ub / self._dec_var_scales,
            cl=self.cl,
            cu=self.cu,
        )

        # TODO: check if options are valid
        for name, val in ipopt_options.items():
            try:
                nlp.add_option(name, val)
            except TypeError:
                logger.error(
                    f"There is a problem with setting options {name} to value {val}"
                )
                raise
        return nlp

    def _get_default_ipopt_options(self) -> Dict[str, Any]:
        default_options = {
            "mu_strategy": "adaptive",
            "tol": 1e-3,
            "linear_solver": "mumps",
            "print_level": 4,
            "nlp_scaling_method": "user-scaling",
            "max_iter": 100,
            "print_timing_statistics": "yes",
            "hessian_approximation": self.hessian_approximation,
            "fixed_variable_treatment": "make_parameter_nodual",
            "output_file": "ipopt.out",
        }

        # HACK: temporary hack for hsl library path
        import platform

        if platform.system() == "Darwin":
            hsllib = "hsl/libcoinhsl.dylib"
        elif platform.system() == "Linux":
            hsllib = "hsl/libcoinhsl.so"
        elif platform.system() == "Widows":
            hsllib = "hsl/libcoinhsl.dll"
        else:
            # what can it be?
            pass

        if exists(hsllib):
            hsl_args = {"hsllib": hsllib, "linear_solver": "ma27"}
            default_options.update(hsl_args)

        return default_options

    def solve(
        self,
        init_guess: Optional[lnp.ndarray] = None,
        lagrange=[],
        zl=[],
        zu=[],
        **user_options,
    ):
        # If the problem has no objectives defined (feasibility solve), define a
        # constatn objective
        if not self._objectives:
            const_obj = BaseObjective(
                num_in=self.num_dec,
                objective=lambda x: 0,
                gradient=lambda x: np.zeros(self.num_dec),
                hessian=lambda x: [],
                hessian_structure=([], []),
            )
            self.add_objective("const_obj", const_obj)

        ipopt_options = self._get_default_ipopt_options()
        ipopt_options.update(user_options)
        nlp = self._construct_ipopt_problem(ipopt_options)

        if init_guess is None:
            init_guess = self.get_init_guess()

        # scale initial guess
        scaled_init_guess = init_guess / self._dec_var_scales

        # Solve the scaled problem
        # TODO: we still need to handle the scaling of the lagrangian multipliers for
        # the constraints as well as for the bounds.
        scaled_sol, info = nlp.solve(scaled_init_guess, lagrange=lagrange, zl=zl, zu=zu)

        # Raise error if the optimization runs into an error
        # Some errors such as nan etc don't actually raise an error in cyipopt, but we
        # want them to
        # TODO: fill this in, or alternatively create acceptable status list
        ERROR_STATUS = [-13]
        if info["status"] in ERROR_STATUS:
            raise RuntimeError(
                f"Error in IPOPT execution, status {info['status']} with message: {info['status_msg']}"
            )

        info["num_iter"] = self._num_iter

        # If print level >=4, print_timing_statistics == yes, and there is an
        # outputfile defined, then read the ipopt time from the file
        if (
            ipopt_options["print_timing_statistics"] == "yes"
            and ipopt_options["print_level"] >= 4
            and ("output_file" in ipopt_options and ipopt_options["output_file"])
        ):
            patterns = {
                "nlp_time": "Total seconds in NLP function evaluations \s*=\s*(\d+.\d+)",
                "ipopt_time": "Total seconds in IPOPT \(w/o function evaluations\) \s*=\s*(\d+.\d+)",
            }
            with open(ipopt_options["output_file"]) as f:
                for name, pattern in patterns.items():
                    f.seek(0)
                    for line in f:
                        match = re.findall(pattern, line)
                        if match:
                            info[name] = float(match[0])

        # Unscale solution before return
        sol = scaled_sol * self._dec_var_scales
        return sol, info

    def intermediate(
        self,
        alg_mod,
        iter_count,
        obj_value,
        inf_pr,
        inf_du,
        mu,
        d_norm,
        regularization_size,
        alpha_du,
        alpha_pr,
        ls_trials,
    ):
        self._num_iter = iter_count


class CompositeProblem(NLPFunction):
    """Combine multiple functions that share the same inputs

    Combining functions g_1, g_2, ... g_n into a function g

    g(x) = concatenate([g_1(x), g_2(x), ..., g_n(x)]

    And does the same for the jacobian and hessians.

    """

    def __init__(self, num_in: int):

        self.num_dec = num_in

        # NOTE: These must be instance properties. If they are class properties, then
        # the CompositeProblem would behave like a singleton, so if you instantiate one
        # ocp after another, it would keep adding ConvProllem to it!
        self._constraints: Dict[str, List[BaseConstraints]] = {}
        self._objectives: Dict[str, List[BaseObjective]] = {}
        self._idx_triu: np.ndarray = (
            None  # index of upper triangular entries in the hessian.
        )

        # Set default varaible bounds and constraint bounds
        self.set_default_bounds()

        self.set_default_scales()

    @property
    def num_con(self):
        # NOTE: this must be an 'int', if it is numpy.int64, cyipopt will throw an
        # exception, see:
        # https://github.com/mechmotum/cyipopt/blob/d6841beacb46a340b4c88465159dab9724ee156e/cyipopt/cython/ipopt_wrapper.pyx#L306
        return sum(p.num_con for p in self._constraints.values())

    def add_constraints(self, name: str, c: BaseConstraints):
        if name in self._constraints:
            raise ValueError(
                f"{name} already exists in defined constraints. Please change to a new"
                f"name. Currently used names are {self._constraints.keys()}",
            )

        if not (c.num_in == self.num_dec):
            raise ValueError(
                f"Mismatch number of inputs: expected {self.num_dec} but "
                f" got a constraints {name} with {c.num_in}"
            )

        # Update the input scales using the nlp's dec_var_scales
        c.set_input_scales(self._dec_var_scales)
        self._constraints.update({name: c})

    def delete_constraints(self, name: str):
        # FIXME: add checks
        self._constraints.pop(name)

    def add_objective(self, name: str, o: BaseObjective):
        """Add an objecitve function to the problem.

        Args:
            name (str): name of the objective
            o (BaseObjective): the objective to use

        Raises:
            NameError: if the name of the objective already exists.
        """
        if name in self._objectives:
            raise NameError(
                f"{name} already exists in defined objectives. Please change to a new name.",
                f"Currently used names are {self._objectives.keys()}",
            )

        # Update the decision variable scale for the objective, using the current nlp's
        # decision variable scale
        o.set_input_scales(self._dec_var_scales)
        self._objectives.update({name: o})

    def delete_objective(self, name: str):
        self._objectives.pop(name)


    def _compute_objective(self, x):
        return np.sum(np.hstack([p.objective(x) for p in self._objectives.values()]))

    def gradient(self, x):
        return np.sum(
            np.vstack([p.gradient(x) for p in self._objectives.values()]), axis=0
        )

    def constraints(self, x):
        return np.hstack(
            [np.ravel(p.constraints(x)) for p in self._constraints.values()]
        )

    def jacobian(self, x):
        return np.hstack([np.ravel(p.jacobian(x)) for p in self._constraints.values()])

    def jacobianstructure(self) -> Tuple[np.ndarray, np.ndarray]:
        idx_rows, idx_cols = [], []

        # When we stack constraints together, the jacobian structure row indices need
        # to be offset by the number of constraints before it.
        row_offset = 0
        for p in self._constraints.values():
            new_rows, new_cols = p.jacobianstructure()
            idx_rows.append(np.ravel(new_rows) + row_offset)
            idx_cols.append(np.ravel(new_cols))
            row_offset += p.num_con

        return np.hstack(idx_rows), np.hstack(idx_cols)

    def hessian(self, x, lagrange, obj_factor):

        # if upper triangular indices don't exist yet, call the hessian structure once
        if self._idx_triu is None:
            _ = self.hessianstructure()

        vals = []

        lagrange = self.split_constraints(lagrange)
        for k, p in self._constraints.items():
            vals.append(np.ravel(p.hessian(x, lagrange[k])))

        for k, p in self._objectives.items():
            vals.append(np.ravel(p.hessian(x) * obj_factor))

        return np.hstack(vals)[self._idx_triu]

    def hessianstructure(self) -> Tuple[np.ndarray, np.ndarray]:
        idx_rows, idx_cols = [], []

        # NOTE: order must be the same as hessian composition!
        for p in list(self._constraints.values()) + list(self._objectives.values()):
            new_rows, new_cols = p.hessianstructure()
            idx_rows.append(np.ravel(new_rows))
            idx_cols.append(np.ravel(new_cols))

        idx_rows = np.hstack(idx_rows)
        idx_cols = np.hstack(idx_cols)

        self._idx_triu = idx_rows <= idx_cols

        return idx_rows[self._idx_triu], idx_cols[self._idx_triu]

    def split_constraints(self, c):
        indices = [p.num_con for p in self._constraints.values()]
        values = np.split(c, np.cumsum(indices[:-1]))
        return dict(zip(self._constraints.keys(), values))

    def profile(
        self, x0, repeat: int = 10, hessian: bool = False, call_once_before: bool = True
    ):
        logger.info("Time NLP execution")

        def time_function(f, name, repeat, *args):
            if call_once_before:
                # call once to remove any possible first call overhead (jitting, etc)
                _ = f(*args)

            start = timer()
            for _ in range(repeat):
                _ = f(*args)

            end = timer()
            time_per_call = (end - start) / repeat

            logger.info(f"{name}: {time_per_call:.6f}")
            return time_per_call

        results = {}

        # objective components
        for name, obj in self._objectives.items():
            for method in ["objective", "gradient", "hessian"]:
                key = ".".join([name, method])
                results[key] = time_function(getattr(obj, method), key, repeat, x0)

        # constraint components
        for name, con in self._constraints.items():
            for method in ["constraints", "jacobian"]:
                key = ".".join([name, method])
                results[key] = time_function(getattr(con, method), key, repeat, x0)

            if hessian:
                # Hessian needs a different signature
                lagrange = np.ones(con.num_con)
                key = ".".join([name, "hessian"])
                results[key] = time_function(con.hessian, key, repeat, x0, lagrange)

        # Test the aggregate separately, as this is likely to be slightly higher than
        # the sum of the components due to additional overhead in aggregating
        for method in ["objective", "gradient", "constraints", "jacobian"]:
            key = ".".join(["nlp", method])
            results[key] = time_function(getattr(self, method), key, repeat, x0)
        if hessian:
            # the problem hessian requires 'obj_factor' as well.
            lagrange = np.ones(self.num_con)
            obj_factor = 1.0
            key = ".".join(["nlp", "hessian"])
            results[key] = time_function(
                self.hessian, key, repeat, x0, lagrange, obj_factor
            )

        return results

    def set_default_bounds(self):
        """Set default bounds of decision variables without external configs.

        For the base class, the default is set to be unbounded.
        """

        # Create default (-inf, inf) bounds
        self.lb = -np.inf * np.ones(self.num_dec)
        self.ub = np.inf * np.ones(self.num_dec)

    def set_default_scales(self):
        # Default scales is unscaled
        self._dec_var_scales = np.ones(self.num_dec)
