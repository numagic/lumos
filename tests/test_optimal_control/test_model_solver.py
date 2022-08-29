import unittest
from typing import Any, List, Tuple, Union
from enum import IntEnum


import numpy as np
from numpy.testing import assert_array_equal
from parameterized import parameterized_class
from lumos.models.base import Model

from lumos.optimal_control.config import (
    BoundaryConditionConfig,
    ScaleConfig,
    BoundConfig,
    ScaleConfig,
)

from lumos.models.composition import ModelMaker
from lumos.optimal_control.nlp import BaseConstraints, BaseObjective, CompositeProblem


class ModelSolver(CompositeProblem):
    _input_groups: Tuple[str, ...] = ("states", "inputs", "states_dot", "con_outputs")

    def __init__(self, model: Model, backend: str, con_outputs: List[str] = []):
        """ModelSolver solves algebraic constraints on models.
        
        TODO: currently only works on StateSpaceModel, but we should make it work
        on any standard models.
        """

        # set constraint outputs
        # TODO: now we have two places using constraint outputs, so maybe this should be
        # a model property?
        # TODO: this is also used in scaled_mesh_ocp
        model.names = model.names._replace(con_outputs=con_outputs)

        # TODO: can/should we get away with not storing the model?
        self._model = model

        # Create the model algebra constraints
        # TODO: should we try to move this `set_flat_implicit_inputs` to the model?
        # The model algebra needs it anyway, so the model should set this, not the OCP
        model.set_flat_implicit_inputs(self._input_groups)
        super().__init__(num_in=model.num_implicit_var)

        # Construct variable enum for easier indexing
        self._input_enum = IntEnum("InputEnum", self.input_names, start=0)

        implicit_functions = model.make_model_algebra_cons(backend=backend)

        # TODO: move these somewhere else
        def _jacobian(*args):
            return np.array(implicit_functions["jacobian"](*args).nonzeros())

        def _hessian(*args):
            return np.array(implicit_functions["_hessian"](*args).nonzeros())

        # TODO: model algebra scales, maybe this should be unified with
        # scaled_mesh_ocp.set_scales, and move to higher level?
        # TODO: currently hard-coded all scales to 1
        model.model_algebra.set_con_scales(np.ones(model.num_implicit_res))

        # FIXME: need to wrap model_algebra to remove mesh and params
        # FIXME: we create CasMappedConstraints (839 in base.py), but it actually is NOT
        # a Constriant that can be executed with its .constraints method, as it requires
        # extra inputs ! (mesh, params)
        # FIXME: mapped constraints are really only called on their mapped methods!
        # So is there any point that they inherit from base_constraints?
        flat_params, unravel = model.get_recursive_params().tree_ravel()
        x0 = np.ones(model.model_algebra.num_in)

        # breakpoint()
        # jac = model.model_algebra.mapped_jacobian(x0, 0.0, flat_params)
        # jac = model.model_algebra.jacobian(x0, 0.0, flat_params)
        # breakpoint()
        model_algebra_con = BaseConstraints(
            num_in=model.model_algebra.num_in,
            num_con=model.model_algebra.num_con,
            constraints=lambda x: model.model_algebra.constraints(x, 0.0, flat_params),
            jacobian=lambda x: _jacobian(x, 0.0, flat_params),
            hessian=lambda x, lagrange: _hessian(x, lagrange, 0.0, flat_params),
            jacobian_structure=model.model_algebra.jacobianstructure(),
            hessian_structure=model.model_algebra.hessianstructure(),
        )

        # Add model algebra constraints
        self.add_constraints("model_algebra", model_algebra_con)

        # Add a constant objective function of 0 (by default, only solving for
        # feasibility)
        # TODO: maybe this should jsut exist in composite problem by default?
        const_obj = BaseObjective(
            num_in=model.num_implicit_var,
            objective=lambda x: 0,
            gradient=lambda x: np.zeros(model.num_implicit_var),
            hessian=lambda x: [],
            hessian_structure=([], []),
        )
        self.add_objective("const_obj", const_obj)

        # Set all constarint values (here all to 0, for equality, or 0 residual)
        self.set_cons()

    def _construct_name(self, group, name):
        return group + "." + name

    @property
    def input_names(self):
        """TODO: this shares a lot with utils.DecVarOperator"""
        var_names = []
        for group in self._input_groups:
            var_names += [
                self._construct_name(group, n)
                for n in getattr(self._model.names, group)
            ]
        return var_names

    def get_var_idx(self, group, name):
        return self._input_enum[self._construct_name(group, name)]

    def set_cons(self):
        # TODO: this ought to be set in CompositeProblem as well
        # Set all constriants to equality
        self.cl = np.zeros(self.num_con)
        self.cu = np.zeros(self.num_con)

    def set_bounds(
        self, group: str, name: str, bounds: Union[float, Tuple[float, float]]
    ):
        idx = self.get_var_idx(group, name)

        if isinstance(bounds, tuple):
            lb, ub = bounds
        else:
            lb = ub = bounds

        assert (
            lb <= ub
        ), f"lower bounds must be smaller than upper bounds, but got ({lb}, {ub}) for {group}.{name}"

        self.lb[idx] = lb
        self.ub[idx] = ub

    def get_bounds(self, group, name):
        idx = self.get_var_idx(group, name)

        return self.lb[idx], self.ub[idx]

    def get_var(self, x, group, name):
        idx = self.get_var_idx(group, name)
        return x[idx]

    def print_result(self, x):

        for idx, name in enumerate(self.input_names):
            print(f"{name}: {x[idx]}")


class TestModelSolver(unittest.TestCase):
    def setUp(self) -> None:
        self.model = ModelMaker.make_model_from_name("SimpleVehicle")

    def test_solve_coasting(self):
        # Create the problem, only needs a model, bounds, and configs

        # Maybe also need custom objective and constraints?
        ms = ModelSolver(
            model=self.model,
            backend="casadi",
            con_outputs=[
                "Fz_tire_fl",
                "Fz_tire_fr",
                "Fz_tire_rl",
                "Fz_tire_rr",
                "slip_ratio_fl",
                "slip_ratio_fr",
                "slip_ratio_rl",
                "slip_ratio_rr",
                "slip_angle_fl",
                "slip_angle_fr",
                "slip_angle_rl",
                "slip_angle_rr",
            ],
        )

        # Add a dummy object
        def _make_obj(group, name, direction):
            """direction = 1 for maximize"""
            idx = ms.get_var_idx(group, name)

            assert direction in [-1, 1]

            def obj(x):
                return -direction * x[idx]

            def gradient(x):
                grad = np.zeros(ms.num_dec)
                grad[idx] = -direction
                return grad

            def hessian(x):
                return []

            return obj, gradient, hessian, ([], [])

        obj, gradient, hessian, hessian_structure = _make_obj("inputs", "ay", 1.0)

        objective = BaseObjective(
            num_in=ms.num_dec,
            objective=obj,
            gradient=gradient,
            hessian=hessian,
            hessian_structure=hessian_structure,
        )

        ms.add_objective("custom_obj", objective)

        ms.set_bounds("states", "vx", 50.0)
        ms.set_bounds("states", "vy", (-5, 5))
        ms.set_bounds("states", "yaw_rate", (-np.pi * 2, np.pi * 2))

        ms.set_bounds("inputs", "throttle", (0, 1))
        ms.set_bounds("inputs", "brake", (0, 1))
        ms.set_bounds("inputs", "steer", (-1, 1))
        ms.set_bounds("con_outputs", "Fz_tire_fl", (1, np.inf))
        ms.set_bounds("con_outputs", "Fz_tire_fr", (1, np.inf))
        ms.set_bounds("con_outputs", "Fz_tire_rl", (1, np.inf))
        ms.set_bounds("con_outputs", "Fz_tire_rr", (1, np.inf))
        ms.set_bounds("states", "wheel_speed_fl", (0.1, 300))
        ms.set_bounds("states", "wheel_speed_fr", (0.1, 300))
        ms.set_bounds("states", "wheel_speed_rl", (0.1, 300))
        ms.set_bounds("states", "wheel_speed_rr", (0.1, 300))

        for name in [
            "slip_ratio_fl",
            "slip_ratio_fr",
            "slip_ratio_rl",
            "slip_ratio_rr",
            "slip_angle_fl",
            "slip_angle_fr",
            "slip_angle_rl",
            "slip_angle_rr",
        ]:
            ms.set_bounds("con_outputs", name, (-0.1, 0.1))

        # Important to leave some states out of QS!
        qs_states = [n for n in self.model.names.states if n not in ["vx", "vy"]]

        for name in qs_states:
            ms.set_bounds("states_dot", name, 0.0)

        # Set some bounds

        x0 = np.ones(ms.num_dec)
        sol, info = ms.solve(x0)

        # Check all steady-states are satisfied
        for name in qs_states:
            self.assertAlmostEqual(ms.get_var(sol, "states_dot", name), 0.0, places=6)

        ms.print_result(sol)

