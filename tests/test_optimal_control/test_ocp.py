import unittest
import os
from typing import Any, Tuple

import numpy as np
from jax import jacobian, hessian
from numpy.testing import assert_array_equal
from parameterized import parameterized_class
from scipy.sparse import coo_matrix

from lumos.optimal_control.config import (
    BoundaryConditionConfig,
    ScaleConfig,
    BoundConfig,
    ScaleConfig,
)
from lumos.optimal_control.nlp import BaseObjective
from lumos.models.composition import ModelMaker
from lumos.models.drone_model import DroneModel
from lumos.optimal_control.fixed_mesh_ocp import FixedMeshOCP
from lumos.optimal_control.scaled_mesh_ocp import ScaledMeshOCP
from lumos.simulations.drone_simulation import DroneSimulation

_todo = unittest.skip("To be implemented")


class TestOCP(unittest.TestCase):
    """Test the methods of OCP without any solve."""

    def setUp(self):
        self.scales_dict = {
            "x": ScaleConfig("states", "x", 10.0),
            "omega": ScaleConfig("inputs", "omega", 4.0),
            "sin_theta": ScaleConfig("con_outputs", "sin_theta", 2.0),
            "mesh_scale": ScaleConfig("global", "mesh_scale", 1.5),
        }

        self.sim_config = DroneSimulation.get_sim_config(
            num_intervals=10,
            transcription="Trapezoidal",
            scales=tuple(self.scales_dict.values()),
        )

        self.ocp = DroneSimulation(sim_config=self.sim_config)

    def _get_state_scales_from_continuity_con(self, name):
        op = self.ocp.dec_var_operator
        idx_state = op.get_var_index_in_group("states", name)
        num_states = op.get_stage_var_size("states")
        return self.ocp._constraints["continuity"]._con_scales[idx_state::num_states]

    def _get_var_scales_from_model_algebra_con(self, group, name):

        op = self.ocp.dec_var_operator
        idx_var = op.get_var_index_in_group(group, name)
        num_con_per_stage = (
            self.ocp.model.num_states
            + self.ocp.model.num_con_outputs
            + self.ocp.model.num_residuals
        )
        # FIXME: the indexing of model_algebra relies on the hard-coded order of states,
        # con_outputs, residuals
        if group == "states":
            offset = 0
        elif group == "con_outputs":
            offset = self.ocp.model.num_states
        return self.ocp._constraints["model_algebra"]._con_scales[
            offset + idx_var :: num_con_per_stage
        ]

    def _check_constraints_scales_are_correctly_set(self, scales_dict):
        """Helper function to test scales are correctly passed to the constraints.

        We don't test if the constraints actually output the correclty scaleds outputs.
        That is left to test_constraints.py.

        NOTE: only valid with scales_dict with hard-coded structure as in setUp!

        TODO: this test is only valid for un-condensed problem for now. The condesned
        problem doesnt' have continuity constriants, and have different constarint order
        in "model_algebra", which contains the condensed continuity.
        """
        # State scales in continuity constraints
        x_scales = self._get_state_scales_from_continuity_con("x")
        np.testing.assert_array_almost_equal(x_scales, scales_dict["x"].value)

        # Scales in model algebra constraints
        x_scales = self._get_var_scales_from_model_algebra_con("states", "x")
        np.testing.assert_array_almost_equal(x_scales, scales_dict["x"].value)

        sin_theta_scales = self._get_var_scales_from_model_algebra_con(
            "con_outputs", "sin_theta"
        )
        np.testing.assert_array_almost_equal(
            sin_theta_scales, scales_dict["sin_theta"].value
        )

    def _check_dec_var_scales_are_correctly_set(self, scales_dict):
        """Helper function to test scales are correctly passed to _dec_var_scales

        NOTE: only valid with scales_dict with hard-coded structure as in setUp!
        """
        op = self.ocp.dec_var_operator
        x_scales = self.ocp._dec_var_scales[op.get_var_index_in_dec("states", "x")]
        np.testing.assert_array_almost_equal(x_scales, scales_dict["x"].value)

        omega_scales = self.ocp._dec_var_scales[
            op.get_var_index_in_dec("inputs", "omega")
        ]
        np.testing.assert_array_almost_equal(omega_scales, scales_dict["omega"].value)

        sin_theta_scales = self.ocp._dec_var_scales[
            op.get_var_index_in_dec("con_outputs", "sin_theta")
        ]
        np.testing.assert_array_almost_equal(
            sin_theta_scales, scales_dict["sin_theta"].value
        )

        mesh_scale_scales = self.ocp._dec_var_scales[
            op.get_var_index_in_dec("global", "mesh_scale")
        ]
        self.assertAlmostEqual(mesh_scale_scales, scales_dict["mesh_scale"].value)

    def test_correct_scales_are_set_from_sim_config(self):
        """Test scales are correclty set from sim_config"""

        # check constraint scales
        self._check_constraints_scales_are_correctly_set(self.scales_dict)
        # check dec var scales
        self._check_dec_var_scales_are_correctly_set(self.scales_dict)

    def test_correct_scales_are_set_after_ocp_construction(self):
        """Test setting scales after ocp construction"""

        # Test on global variable scale
        scales_dict = {
            "x": ScaleConfig("states", "x", 3.0),
            "omega": ScaleConfig("inputs", "omega", 1.5),
            "sin_theta": ScaleConfig("con_outputs", "sin_theta", 7.1),
            "mesh_scale": ScaleConfig("global", "mesh_scale", 0.3),
        }
        self.ocp.set_scales(tuple(scales_dict.values()))

        # check constraint scales
        self._check_constraints_scales_are_correctly_set(scales_dict)
        # check dec var scales
        self._check_dec_var_scales_are_correctly_set(scales_dict)

    def test_update_bounds(self):
        """Test corretly updating bounds or otherwise throwing error"""

        def _udpate_and_assert(group: str, name: str, bound_vals: Tuple[Any]):
            old_lb = self.ocp.lb
            old_ub = self.ocp.ub

            new_bounds = (BoundConfig(group, name, bound_vals),)
            self.ocp.update_bounds(new_bounds)

            op = self.ocp.dec_var_operator
            for g in ["states", "inputs", "states_dot", "con_outputs"]:
                for n in self.ocp.model.get_group_names(group):
                    # Ensure bounds that need to change are changed.
                    if g == group and n == name:
                        # NOTE: here the multiply is broadcasted for scalar case, and
                        # element-wise for array case (which makes no difference), but
                        # both are correct
                        assert_array_equal(
                            self.ocp.get_lb(group=group, name=name),
                            bound_vals[0] * np.ones(self.ocp.num_stages),
                        )

                        assert_array_equal(
                            self.ocp.get_ub(group=group, name=name),
                            bound_vals[1] * np.ones(self.ocp.num_stages),
                        )
                    else:
                        # Ensure that other bounds are unmodified
                        assert_array_equal(
                            self.ocp.get_lb(group=group, name=name),
                            op.get_var(old_lb, group=group, name=name),
                        )

                        assert_array_equal(
                            self.ocp.get_ub(group=group, name=name),
                            op.get_var(old_ub, group=group, name=name),
                        )

        # Setting bounds with scalars
        _udpate_and_assert(group="inputs", name="f", bound_vals=(-100, 100))

        # infeasible bound should throw an error
        with self.assertRaises(AssertionError):
            _udpate_and_assert(group="outputs", name="sin_theta", bound_vals=(0.6, 0.5))

        # Setting bounds with vectors
        _ones = np.ones(self.ocp.num_stages)
        _udpate_and_assert(
            group="inputs", name="omega", bound_vals=(-100 * _ones, 100 * _ones)
        )

        # Infeasible bound should throw an error
        with self.assertRaises(AssertionError):
            ub = 200 * _ones
            lb = np.copy(ub)
            lb[10] += 1
            _udpate_and_assert(group="states", name="z", bound_vals=(lb, ub))

        # Incorrect size should also throw an error
        with self.assertRaises(AssertionError):
            _wrong_ones = np.ones(self.ocp.num_stages + 1)
            _udpate_and_assert(
                group="states", name="z", bound_vals=(-100 * _ones, 100 * _wrong_ones)
            )

        # Setting bounds with mixed scalar and vectors shoudl raise an error
        with self.assertRaises(TypeError):
            _udpate_and_assert(group="states", name="x", bound_vals=(-200, 200 * _ones))

        # TODO: Test set global var

    def test_update_bounds_do_not_overwrite_bc(self):
        """Ensure updating bounds after boundary conditions are set do not overwrite."""

        expected_value = 0.0
        bc_configs = (BoundaryConditionConfig(0, "states", "x", expected_value),)
        self.ocp.update_boundary_conditions(bc_configs)

        bound_configs = (BoundConfig("states", "x", (-1.0, 1.0)),)
        self.ocp.update_bounds(bound_configs)

        # After updating the general bounds, it shouldn't overwrite and relax the
        # boundary conditions we set at stage 0!
        actual_lb = self.ocp.get_lb("states", "x")[0]
        self.assertAlmostEqual(actual_lb, expected_value)

        actual_ub = self.ocp.get_ub("states", "x")[0]
        self.assertAlmostEqual(actual_ub, expected_value)

    @unittest.skip(
        "After making ocp independent of Jax, does it really make sense to test the derivatives here?"
    )
    def test_jacobian(self):
        random_vector = np.abs(np.random.randn(self.ocp.num_dec))
        jac_vals = self.ocp.jacobian(random_vector)
        jac_rows, jac_cols = self.ocp.jacobianstructure()

        ours = coo_matrix(
            (jac_vals, (jac_rows, jac_cols)), shape=(self.ocp.num_con, self.ocp.num_dec)
        ).toarray()

        theirs = np.array(jacobian(self.ocp.constraints)(random_vector))

        np.testing.assert_allclose(ours, theirs, rtol=1e-6)

    @unittest.skip(
        "After making ocp independent of Jax, does it really make sense to test the derivatives here?"
    )
    def test_hessian(self):
        random_vector = np.abs(np.random.randn(self.ocp.num_dec))
        random_lagrange = np.random.randn(self.ocp.num_con)
        obj_factor = 1.0

        hessian_vals = self.ocp.hessian(random_vector, random_lagrange, obj_factor)
        hessian_rows, hessian_cols = self.ocp.hessianstructure()

        ours = coo_matrix(
            (hessian_vals, (hessian_rows, hessian_cols)),
            shape=(self.ocp.num_dec, self.ocp.num_dec),
        ).toarray()

        # We use upper triangular form by default
        theirs = np.triu(
            np.array(
                hessian(self.ocp.lagrangian)(random_vector, random_lagrange, obj_factor)
            )
        )
        np.testing.assert_allclose(ours, theirs, rtol=1e-6)

    def test_profile(self):
        """Test profiling info are returned correctly"""

        x0 = self.ocp.get_init_guess()

        # profile without hessian
        results = self.ocp.profile(x0, repeat=10, hessian=False)
        self.assertIn("model_algebra.constraints", results)
        self.assertIn("model_algebra.jacobian", results)
        self.assertNotIn("model_algebra.hessian", results)
        self.assertIn("nlp.constraints", results)
        self.assertIn("nlp.jacobian", results)
        self.assertNotIn("nlp.hessian", results)

        # Time should be positive
        for k, v in results.items():
            self.assertGreater(v, 0.0)

        # profile with hessian
        results = self.ocp.profile(x0, repeat=10, hessian=True)
        self.assertIn("model_algebra.constraints", results)
        self.assertIn("model_algebra.jacobian", results)
        self.assertIn("model_algebra.hessian", results)
        self.assertIn("nlp.constraints", results)
        self.assertIn("nlp.jacobian", results)
        self.assertIn("nlp.hessian", results)

        # Time should be positive
        for k, v in results.items():
            self.assertGreater(v, 0.0)


# TODO: many combinations to test:
# 1) hessian approximation
# 2) transcription method
# 3) problem size
@parameterized_class(
    ("hessian_approximation",), [("exact",), ("limited-memory",),],
)
class TesteOCPSolve(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sim_config = DroneSimulation.get_sim_config(
            num_intervals=99,
            hessian_approximation=cls.hessian_approximation,
            transcription="Trapezoidal",
        )

        cls.ocp = DroneSimulation(sim_config=cls.sim_config)
        cls.solution, cls.info = cls.ocp.solve(
            init_guess=cls.ocp.get_init_guess(), max_iter=500
        )

    def test_objective(self):
        """Final time should be 1.300 sec for this problem"""
        # TODO: watch out, in the future the objective could be scaled.
        self.assertAlmostEqual(self.info["obj_val"], 1.3, delta=1e-3)

    def test_optimal(self):
        """Solution flag should be optimal."""
        self.assertEqual(self.info["status"], 0)

    @_todo
    def test_continuity(self):
        """Solution satisfy continuity equations."""
        raise NotImplementedError

    def test_boundary_conditions(self):
        """Test required boundary conditions are met."""
        for bc in self.sim_config.boundary_conditions:
            self.assertAlmostEqual(
                self.ocp.dec_var_operator.get_var(
                    self.solution, group=bc.group, name=bc.name, stage=bc.stage
                ),
                bc.value,
                delta=1e-3,
            )


def _get_default_boundary_conditions():
    return (
        BoundaryConditionConfig(0, "states", "x", 0.0),
        BoundaryConditionConfig(0, "states", "x_dot", 0.0),
        BoundaryConditionConfig(0, "states", "z", 0.0),
        BoundaryConditionConfig(0, "states", "z_dot", 0.0),
        BoundaryConditionConfig(0, "states", "theta", 0.0),
        BoundaryConditionConfig(-1, "states", "x_dot", 0.0),
        BoundaryConditionConfig(-1, "states", "z", 0.0),
        BoundaryConditionConfig(-1, "states", "z_dot", 0.0),
        BoundaryConditionConfig(-1, "states", "theta", 2 * np.pi),
    )


def _get_default_bounds():
    return (
        BoundConfig(group="states", name="x", values=(-50, 50)),
        BoundConfig(group="states", name="x_dot", values=(-50, 50)),
        BoundConfig(group="states", name="z", values=(-50, 50)),
        BoundConfig(group="states", name="z_dot", values=(-50, 50)),
        BoundConfig(group="states", name="theta", values=(-10 * np.pi, 10 * np.pi)),
        BoundConfig(group="inputs", name="f", values=(1, 20)),
        BoundConfig(group="inputs", name="omega", values=(-10, 10)),
    )


def _make_nonuniform_intervals(num_intervals: int):
    first_half = int(num_intervals / 2)
    second_half = num_intervals - first_half
    first_half_end = 0.2  # make this not doo different to old one to make interpolation
    # easier with coarse grid, but different enough to trigger errors.
    interval_points = np.hstack(
        [
            np.linspace(0, first_half_end, first_half),
            np.linspace(first_half_end + 0.01, 1.0, second_half + 1),
        ]
    )

    return interval_points


class TestOCPWithCustomMesh(unittest.TestCase):
    def test_create_mesh(self):
        num_intervals = 99
        model = DroneModel()
        sim_config = ScaledMeshOCP.get_sim_config(
            num_intervals=num_intervals, transcription="LGR",
        )
        ocp = ScaledMeshOCP(model=model, sim_config=sim_config)

        # Error if not finish at 1.0
        with self.assertRaises(ValueError):
            interval_points = np.linspace(0, 1.1, num_intervals + 1)
            ocp.set_normalized_mesh(interval_points)

        # Error if not start at 0.0
        with self.assertRaises(ValueError):
            interval_points = np.linspace(0.1, 1.0, num_intervals + 1)
            ocp.set_normalized_mesh(interval_points)

        # Error if not corrrect number of points
        with self.assertRaises(ValueError):
            interval_points = np.linspace(0.0, 1.0, num_intervals)
            ocp.set_normalized_mesh(interval_points)

        # Error if not monotonically increasing
        with self.assertRaises(ValueError):
            interval_points = np.linspace(0.0, 1.0, num_intervals + 1)
            interval_points[1] = 0.3
            ocp.set_normalized_mesh(interval_points)

        # Do it correctly
        interval_points = _make_nonuniform_intervals(num_intervals)
        ocp.set_normalized_mesh(interval_points)

        # Using a scale of 1, the mesh would be normalized.
        normalized_mesh_points = ocp.get_mesh_from_scale(1)
        actual_interval_points = normalized_mesh_points[
            :: ocp.dec_var_operator.num_stages_per_interval - 1
        ]

        np.testing.assert_allclose(actual_interval_points, interval_points)

        # Check mesh are set correctly

    def test_nonuniform_on_fixed_mesh(self):
        """Test changing mesh after problem creation still yields the correct results."""
        num_intervals = 99

        model = DroneModel()
        ocp = FixedMeshOCP(
            model=model,
            sim_config=FixedMeshOCP.get_sim_config(
                num_intervals=num_intervals,
                transcription="LGR",
                backend="jax",
                boundary_conditions=_get_default_boundary_conditions(),
                bounds=_get_default_bounds(),
            ),
            mesh_scale=1.0,  # work over a fixed 1.0sec span
        )

        # Remove the default time objective
        # TODO: the time objective shouldn't be there by default in the first place
        ocp.delete_objective("time")

        # Create new objective, say minimize x-distance travelled (so move to the left)
        def _objective(x):
            idx_end = ocp.dec_var_operator.get_var_index_in_dec(
                group="states", name="x", stage=-1
            )

            idx_start = ocp.dec_var_operator.get_var_index_in_dec(
                group="states", name="x", stage=0
            )
            return x[idx_end] - x[idx_start]

        def _gradient(x):
            idx_end = ocp.dec_var_operator.get_var_index_in_dec(
                group="states", name="x", stage=-1
            )

            idx_start = ocp.dec_var_operator.get_var_index_in_dec(
                group="states", name="x", stage=0
            )
            grad = np.zeros_like(x)
            grad[idx_end] = 1
            grad[idx_start] = -1
            return grad

        obj = BaseObjective(
            num_in=ocp.num_dec,
            objective=lambda x: _objective(x),
            gradient=lambda x: _gradient(x),
            hessian=lambda x: np.array([]),
            hessian_structure=(
                np.array([], dtype=np.int32),
                np.array([], dtype=np.int32),
            ),
        )
        ocp.add_objective("x", obj)

        # Use some very poor, but deterministic initial guess!
        x0 = np.ones(ocp.num_dec)
        sol, info = ocp.solve(x0, max_iter=500)

        mesh = ocp.get_mesh_from_dec_var(sol)
        final_x = ocp.dec_var_operator.get_var(sol, "states", "x", -1)

        # Create some non-uniform interval length
        interval_points = _make_nonuniform_intervals(num_intervals)
        ocp.set_normalized_mesh(interval_points)

        new_sol, new_info = ocp.solve(x0, max_iter=500)
        new_mesh = ocp.get_mesh_from_dec_var(new_sol)
        new_final_x = ocp.dec_var_operator.get_var(new_sol, "states", "x", -1)

        # Check if results are the same
        self.assertAlmostEqual(final_x, new_final_x, places=1)

        # Check if the results on the same index point (eg, stage 33) are NOT the same
        for stage in [10, 30, ocp.num_stages - 20]:
            old_val = ocp.dec_var_operator.get_var(sol, "states", "x_dot", stage)
            new_val = ocp.dec_var_operator.get_var(new_sol, "states", "x_dot", stage)

            self.assertNotAlmostEqual(old_val, new_val, places=1)

        # Check if the results on the same mesh are the same
        for stage in [10, 30, ocp.num_stages - 20]:
            old_val = ocp.dec_var_operator.get_var(sol, "states", "x_dot", stage)
            # Get the value of the results on new mesh by interpolating them to old mesh
            # point
            new_val = np.interp(
                mesh[stage],
                new_mesh,
                ocp.dec_var_operator.get_var(new_sol, "states", "x_dot"),
            )

            self.assertAlmostEqual(old_val, new_val, places=1)

    def test_nonuniform_on_scaled_mesh(self):
        """Test changing mesh after problem creation still yields the correct results."""
        num_intervals = 99

        ocp = DroneSimulation(
            sim_config=DroneSimulation.get_sim_config(
                num_intervals=num_intervals, transcription="LGR", backend="jax"
            )
        )

        x0 = np.ones(ocp.num_dec)
        sol, info = ocp.solve(x0, max_iter=500)

        mesh = ocp.get_mesh_from_dec_var(sol)
        time = mesh[-1] - mesh[0]

        # Create some non-uniform interval length
        interval_points = _make_nonuniform_intervals(num_intervals)
        ocp.set_normalized_mesh(interval_points)

        new_sol, new_info = ocp.solve(x0, max_iter=500)
        new_mesh = ocp.get_mesh_from_dec_var(new_sol)
        new_time = new_mesh[-1] - new_mesh[0]

        # Check if results are the same
        self.assertAlmostEqual(time, new_time, places=1)

        # Check if the results on the same index point (eg, stage 33) are NOT the same
        for stage in [10, 30, ocp.num_stages - 20]:
            old_val = ocp.dec_var_operator.get_var(sol, "states", "x_dot", stage)
            new_val = ocp.dec_var_operator.get_var(new_sol, "states", "x_dot", stage)

            self.assertNotAlmostEqual(old_val, new_val, places=1)

        # Check if the results on the same mesh are the same
        for stage in [10, 30, ocp.num_stages - 20]:
            old_val = ocp.dec_var_operator.get_var(sol, "states", "x_dot", stage)
            # Get the value of the results on new mesh by interpolating them to old mesh
            # point
            new_val = np.interp(
                mesh[stage],
                new_mesh,
                ocp.dec_var_operator.get_var(new_sol, "states", "x_dot"),
            )

            self.assertAlmostEqual(old_val, new_val, places=1)


def test_timing_extraction():
    """Test that we can correctly extract ipopt timing when available"""
    sim_config = DroneSimulation.get_sim_config(
        num_intervals=99, hessian_approximation="exact", transcription="Trapezoidal",
    )

    ocp = DroneSimulation(sim_config=sim_config)

    # with print level >= 4, we should get timing metrics
    _, info = ocp.solve(
        init_guess=ocp.get_init_guess(),
        print_level=4,
        print_timing_statistics="yes",
        max_iter=500,
    )

    assert "nlp_time" in info
    assert info["nlp_time"] > 0.0
    assert "ipopt_time" in info
    assert info["ipopt_time"] > 0.0

    # if custom output file is defined, we should still get it
    _, info = ocp.solve(
        init_guess=ocp.get_init_guess(), output_file="myoutput.out", max_iter=500
    )

    assert "nlp_time" in info
    assert info["nlp_time"] > 0.0
    assert "ipopt_time" in info
    assert info["ipopt_time"] > 0.0

    # if print_timing_statistics == "no" -> no timing metrics
    _, info = ocp.solve(
        init_guess=ocp.get_init_guess(), print_timing_statistics="no", max_iter=500
    )
    assert "nlp_time" not in info
    assert "ipopt_time" not in info
