import unittest
from typing import List

import numpy as np

from lumos.models import ModelMaker
from lumos.models.drone_model import DroneModel
from lumos.optimal_control.nlp import BaseObjective
from lumos.optimal_control.model_solver import ModelSolver


class TestModelSolver(unittest.TestCase):
    """Test basic functionality of ModelSolver on drone model"""

    def setUp(self) -> None:
        self.model = DroneModel()

        self.ms = ModelSolver(
            model=self.model, backend="casadi", con_outputs=["f_omega"],
        )

    def test_set_scales(self):
        """Setting custom scales lead to correct constraint and decision var scaling"""

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

        # Ensure decision variable sclaes are updated correctly
        self.assertAlmostEqual(ms._dec_var_scales[ms.get_var_idx("states", "x")], 10.0)

        # Ensure constraint scales are updated correctly
        # This test is a bit tricky as we rely on the hard-coded ordering of the
        # algebraic constraints
        x0 = np.ones(ms.num_dec)
        x0[ms.get_var_idx("states", "x_dot")] = 5.0
        x0[ms.get_var_idx("states_dot", "x")] = 4.0
        expected_scaled_con = (
            x0[ms.get_var_idx("states", "x_dot")]
            - x0[ms.get_var_idx("states_dot", "x")]
        ) / 10
        # We should expect the evaluation of the scaled constriants to come out as (5.0 - 4.0)/10 = 0.1
        con = ms._constraints["model_algebra"].constraints(x0)
        idx = self.model.get_var_index("states", "x")
        self.assertAlmostEqual(con[idx], expected_scaled_con)


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
        """Test a feasibility solve with no objectives. Check constraints are satisfied."""
        ms = self.ms

        # Set the required quasi-static states: some states should not be set as QS!
        qs_states = [n for n in self.model.names.states if n not in ["vx", "vy"]]
        _set_base_vehicle_bounds(ms, qs_states)

        x0 = np.ones(ms.num_dec)
        sol, info = ms.solve(x0)

        # Check all steady-states are satisfied
        for name in qs_states:
            self.assertAlmostEqual(ms.get_var(sol, "states_dot", name), 0.0, places=6)

    def test_add_obj_from_var(self):
        """Test solving with existing variables as objective."""
        ms = self.ms

        # Set the required quasi-static states: some states should not be set as QS!
        qs_states = [n for n in self.model.names.states if n not in ["vx", "vy"]]
        _set_base_vehicle_bounds(ms, qs_states)

        # Trivial initial guess
        x0 = np.ones(ms.num_dec)

        # minmize ay
        obj_name = ms.add_obj_from_var("inputs", "ay", weight=1.0)
        sol, info = ms.solve(x0)
        # Check ay is -ve enough
        self.assertLess(ms.get_var(sol, "inputs", "ay"), -3.0)

        # Check all steady-states are satisfied
        for name in qs_states:
            self.assertAlmostEqual(ms.get_var(sol, "states_dot", name), 0.0, places=6)

        # remove objective to clean up
        ms.delete_objective(obj_name)

        # maximize ay
        obj_name = ms.add_obj_from_var("inputs", "ay", weight=-1.0)
        sol, info = ms.solve(x0)
        # Check ay is +ve enough
        self.assertGreater(ms.get_var(sol, "inputs", "ay"), 3.0)

        # remove objective to clean up
        ms.delete_objective(obj_name)

        # Maximize some combined ax ay. Instead of defining a custom objective, we could
        # actually just add two obj from var
        obj_name_ay = ms.add_obj_from_var("inputs", "ay", weight=-1.0)
        obj_name_ax = ms.add_obj_from_var("inputs", "ax", weight=-1.0)

        sol, info = ms.solve(x0)
        opt_ax = ms.get_var(sol, "inputs", "ax")
        opt_ay = ms.get_var(sol, "inputs", "ay")

        # Check ax and ay are +ve enough
        self.assertGreater(opt_ax, 2.0)
        self.assertGreater(opt_ay, 2.0)

        # Ensure setting scale doesn't change result
        ms.set_var_scale("inputs", "ax", 100)

        sol, info = ms.solve(x0)
        self.assertAlmostEqual(ms.get_var(sol, "inputs", "ax"), opt_ax, places=3)
        self.assertAlmostEqual(ms.get_var(sol, "inputs", "ay"), opt_ay, places=3)

        # Check ax and ay are +ve enough
        self.assertGreater(opt_ax, 2.0)
        self.assertGreater(opt_ay, 2.0)

        # remove objective to clean up
        ms.delete_objective(obj_name_ay)
        ms.delete_objective(obj_name_ax)

    def test_custom_objective_solve(self):
        """Create a custom objective that is the same as obj_from_var, results should not change"""
        ms = self.ms

        # Set the required quasi-static states: some states should not be set as QS!
        qs_states = [n for n in self.model.names.states if n not in ["vx", "vy"]]
        _set_base_vehicle_bounds(ms, qs_states)

        # Add a dummy object
        def _make_obj(group, name, weight):
            """direction = 1 for maximize"""
            idx = ms.get_var_idx(group, name)

            def obj(x):
                return weight * x[idx]

            def gradient(x):
                grad = np.zeros(ms.num_dec)
                grad[idx] = weight
                return grad

            def hessian(x):
                return []

            return {
                "objective": obj,
                "gradient": gradient,
                "hessian": hessian,
                "hessian_structure": ([], []),
            }

        objective = BaseObjective(num_in=ms.num_dec, **_make_obj("inputs", "ay", -1.0))
        ms.add_objective("max_ay", objective)

        x0 = np.ones(ms.num_dec)
        sol, info = ms.solve(x0)

        # Check all steady-states are satisfied
        for name in qs_states:
            self.assertAlmostEqual(ms.get_var(sol, "states_dot", name), 0.0, places=6)

        ms.print_result(sol)

        # Check this agrees with our objective from var solve result
        ms.delete_objective("max_ay")
        ms.add_obj_from_var("inputs", "ay", weight=-1.0)
        new_sol, _ = ms.solve(x0)

        self.assertAlmostEqual(
            ms.get_var(sol, "inputs", "ay"),
            ms.get_var(new_sol, "inputs", "ay"),
            places=3,
        )

