import logging
import unittest
from typing import Any, Tuple

import numpy as np
from jax import jacobian, hessian
from numpy.testing import assert_array_equal
from parameterized import parameterized_class
from scipy.sparse import coo_matrix

from lumos.optimal_control.config import StageVarBoundConfig
from lumos.simulations.drone_simulation import DroneSimulation

_todo = unittest.skip("To be implemented")


class TestOCP(unittest.TestCase):
    """Test the methods of OCP without any solve."""

    @classmethod
    def setUpClass(cls):
        cls.sim_config = DroneSimulation.get_sim_config(
            num_intervals=10, transcription="Trapezoidal",
        )

        cls.ocp = DroneSimulation(sim_config=cls.sim_config)

    def test_update_bounds(self):
        """Test corretly updating bounds or otherwise throwing error"""

        def _udpate_and_assert(group: str, name: str, bound_vals: Tuple[Any]):
            old_lb = self.ocp.lb
            old_ub = self.ocp.ub

            new_bounds = (StageVarBoundConfig(group, name, bound_vals),)
            self.ocp.update_bounds(new_bounds)

            op = self.ocp.dec_var_operator
            for g in self.ocp.stage_var_groups:
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
