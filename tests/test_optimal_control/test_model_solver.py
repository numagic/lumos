import unittest
from typing import Any, List, Tuple

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

    @property
    def input_names(self):
        """TODO: this shares a lot with utils.DecVarOperator"""
        var_names = []
        for group in self._input_groups:
            var_names += [group + "." + n for n in getattr(self._model.names, group)]
        return var_names

    def set_cons(self):
        # TODO: this ought to be set in CompositeProblem as well
        # Set all constriants to equality
        self.cl = np.zeros(self.num_con)
        self.cu = np.zeros(self.num_con)


class TestModelSolver(unittest.TestCase):
    def setUp(self) -> None:
        self.model = ModelMaker.make_model_from_name("SimpleVehicle")

    def test_solve_coasting(self):

        # Create the problem, only needs a model, bounds, and configs

        # Maybe also need custom objective and constraints?
        model_solver = ModelSolver(
            model=self.model,
            backend="casadi",
            con_outputs=["Fz_tire_fl", "Fz_tire_fr", "Fz_tire_rl", "Fz_tire_rr",],
        )

        # Set some bounds

        x0 = np.ones(model_solver.num_dec)
        sol, info = model_solver.solve(x0)

        pass
