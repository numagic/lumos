import unittest
from typing import List

import numpy as np

from lumos.models import ModelMaker
from lumos.models.drone_model import DroneModel
from lumos.optimal_control.nlp import BaseObjective
from lumos.optimal_control.model_solver import ModelSolver


def _set_base_vehicle_bounds(ms, qs_states: List[str]):
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

    for name in qs_states:
        ms.set_bounds("states_dot", name, 0.0)

    # set some scales
    ms.set_var_scale("states", "wheel_speed_fl", 10)
    ms.set_var_scale("states", "wheel_speed_fr", 10)
    ms.set_var_scale("states", "wheel_speed_rl", 10)
    ms.set_var_scale("states", "wheel_speed_rr", 10)
    ms.set_var_scale("states", "vx", 10)
    ms.set_var_scale("con_outputs", "Fz_tire_fl", 100)
    ms.set_var_scale("con_outputs", "Fz_tire_fr", 100)
    ms.set_var_scale("con_outputs", "Fz_tire_rl", 100)
    ms.set_var_scale("con_outputs", "Fz_tire_rr", 100)


class TestModelSolver(unittest.TestCase):
    """Test basic functionality of ModelSolver on drone model"""

    def setUp(self) -> None:
        self.model = DroneModel()

        self.ms = ModelSolver(
            model=self.model, backend="casadi", con_outputs=["f_omega"],
        )

    def test_set_scales(self):

        # Check if the default scales are all correct (unscaled)
        ms = self.ms
        for g in ms._model.implicit_inputs:
            for n in getattr(self.model.names, g):
                self.assertAlmostEqual(ms._var_scales[g][n], 1.0)

        # Set a scale that doesn't exist
        with self.assertRaises(KeyError):
            ms.set_var_scale("WrongGroup", "x", 1.0)

        with self.assertRaises(KeyError):
            ms.set_var_scale("states", "WrongName", 1.0)

        # Set some correct scales
        ms.set_var_scale("states", "x", 10.0)
        self.assertAlmostEqual(ms._var_scales["states"]["x"], 10.0)

        pass


class TestSolveVehicleModel(unittest.TestCase):
    """Test advanced solve use-cases on vehicle model."""

    def setUp(self) -> None:
        self.model = ModelMaker.make_model_from_name("SimpleVehicle")

        self.ms = ModelSolver(
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

    def test_feasibility_solve(self):
        # Create the problem, only needs a model, bounds, and configs

        # Maybe also need custom objective and constraints?
        ms = self.ms

        # Set the required quasi-static states: some states should not be set as QS!
        qs_states = [n for n in self.model.names.states if n not in ["vx", "vy"]]

        _set_base_vehicle_bounds(ms, qs_states)

        x0 = np.ones(ms.num_dec)
        sol, info = ms.solve(x0)

        # Check all steady-states are satisfied
        for name in qs_states:
            self.assertAlmostEqual(ms.get_var(sol, "states_dot", name), 0.0, places=6)

        ms.print_result(sol)

    def test_solve_coasting(self):
        # Create the problem, only needs a model, bounds, and configs

        # Maybe also need custom objective and constraints?
        ms = self.ms

        # Set the required quasi-static states: some states should not be set as QS!
        qs_states = [n for n in self.model.names.states if n not in ["vx", "vy"]]

        _set_base_vehicle_bounds(ms, qs_states)

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

        x0 = np.ones(ms.num_dec)
        sol, info = ms.solve(x0)

        # Check all steady-states are satisfied
        for name in qs_states:
            self.assertAlmostEqual(ms.get_var(sol, "states_dot", name), 0.0, places=6)

        ms.print_result(sol)

