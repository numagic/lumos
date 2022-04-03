import unittest

import numpy as np
from parameterized import parameterized_class
from scipy.sparse import csc_matrix

from lumos.models.drone_model import DroneModel
from lumos.optimal_control.fixed_mesh_ocp import FixedMeshOCP
from lumos.optimal_control.utils import batch_conv1d
from lumos.optimal_control.config import BoundaryConditionConfig
from lumos.simulations.laptime_simulation import LaptimeSimulation
from lumos.optimal_control.nlp import LinearConstraints


# TODO: we should probably move these to some common utilities
def _fd_jacobian(fn, x0, delta=1e-6):
    num_in = len(x0)
    jac = []
    for idx in range(num_in):
        # central difference is needed as for our case fwd difference was not
        # good enough for 2nd order derivatives.
        x_up = np.copy(x0)
        x_up[idx] += delta / 2
        x_down = np.copy(x0)
        x_down[idx] -= delta / 2
        jac.append((fn(x_up) - fn(x_down)) / delta)

    return np.stack(jac).T


def _fd_hessian(fn, x0, delta=1e-6):
    def grad_fn(xx):
        return np.squeeze(_fd_jacobian(fn, xx, delta=delta))

    return _fd_jacobian(grad_fn, x0, delta)


class TestFixedDistanceCondensed(unittest.TestCase):
    """Test the condensed constraints and its derivatives."""

    @classmethod
    def setUpClass(cls):
        cls.ocp = FixedMeshOCP(
            model=DroneModel(),
            sim_config=FixedMeshOCP.get_sim_config(
                num_intervals=3,
                hessian_approximation="exact",
                is_condensed=True,
                backend="casadi",
                transcription="LGR",
                scales={
                    "states": {"x": 10},
                },  # Sometimes things only work with scales =1, we need to catch it
            ),
        )

        # FIXME: if we do the derivative tests with vehicle models, then we need to
        # use a reasonable x0, otherwise the test fails. Is it because the vehicle model
        # has a 'sensitive' valid input range? Otherwise the model behaves odd and make
        # the finite difference or the AD part blow up?
        cls.x0 = np.random.randn(cls.ocp.num_dec)

    def test_condensed_constraints(self):
        """Condensed constraints should agree with manually constructed ones."""
        cons = self.ocp._condensed_constraints(self.x0)
        op = self.ocp.dec_var_operator

        vars = op.unflatten_var(self.x0)
        distance = self.ocp._flat_normalized_mesh * self.ocp._get_mesh_scale(self.x0)
        model_return = self.ocp.model.batched_forward(
            vars.states, vars.inputs, distance, self.ocp._params
        )

        width = op.num_stages_per_interval
        stride = width - 1
        states = batch_conv1d(vars.states, width=width, stride=stride)
        states_dot = batch_conv1d(model_return.states_dot, width=width, stride=stride)
        distance = batch_conv1d(distance, width=width, stride=stride)

        # Check continuity part
        interval_length = distance[:, -1] - distance[:, 0]
        A, B = self.ocp.transcription.get_continuity_matrices()
        # Use loop to follow different code as actual implementation
        # NOTE: here we also need to manually implement the scaling.
        continuity_cons = []
        for interval in range(self.ocp.num_intervals):
            continuity_cons.append(
                self.ocp.transcription.continuity_con(
                    states[interval], states_dot[interval], interval_length[interval]
                )
                / self.ocp.model.get_group_scales("states")
            )
        continuity_cons = np.stack(continuity_cons).ravel()

        num_continuity_cons = (
            self.ocp.num_intervals
            * (op.num_stages_per_interval - 1)
            * self.ocp.model.num_states
        )

        np.testing.assert_allclose(
            cons[:num_continuity_cons],
            continuity_cons,
            err_msg="continuity part of the condensed constraints are incorrect",
            atol=1e-4,
            rtol=1e-3,
        )

        # Check algebraic part
        # NOTE: need to be careful here with stacking because some models have empty
        # con_outputs or residuals
        expected_algebraic_cons = []
        if not (model_return.con_outputs.size == 0):
            expected_algebraic_cons.append(model_return.con_outputs - vars.con_outputs)
        if not (model_return.residuals.size == 0):
            expected_algebraic_cons.append(model_return.residuals)
        expected_algebraic_cons = np.hstack(expected_algebraic_cons).ravel()
        np.testing.assert_allclose(
            cons[num_continuity_cons:],
            expected_algebraic_cons,
            err_msg="algebraic part of the condensed constraints are incorrect",
            atol=1e-4,
            rtol=1e-3,
        )

        pass

    def test_condensed_jacobian(self):
        """Condensed jacobian should agree with finite difference jacobian"""
        # NOTE: we could do tests just on the non-sparse entries, but that would miss
        # bugs when the sparsity returned is too optimistic (we miss non-sparse
        # elements in our derivatives)
        actual = (
            self.ocp._constraints["model_algebra"].get_csc_jacobian(self.x0).toarray()
        )
        desired = _fd_jacobian(self.ocp._condensed_constraints, self.x0)
        np.testing.assert_allclose(actual, desired, atol=1e-4, rtol=1e-3)

    def test_condensed_hessian(self):
        """Condensed hessian should agree with finite difference hessian

        NOTE: this is a slow test. (>1m)
        """
        lagrange = np.abs(
            np.random.randn(self.ocp._constraints["model_algebra"].num_con)
        )
        vals = self.ocp._condensed_hessian(self.x0, lagrange)
        rows, cols = self.ocp._condensed_hessianstructure()
        shape = (self.ocp.num_dec, self.ocp.num_dec)
        actual = csc_matrix(
            (vals.ravel(), (rows.ravel(), cols.ravel())), shape=shape
        ).toarray()

        def lagrangian(xx):
            return np.dot(lagrange, self.ocp._condensed_constraints(xx))

        desired = _fd_hessian(lagrangian, self.x0, delta=1e-3)
        np.testing.assert_allclose(actual, desired, atol=1e-4, rtol=1e-3)


class TestLaptimeSimulation(unittest.TestCase):
    # tests without solves
    @classmethod
    def setUpClass(cls):

        cls.sim_config = LaptimeSimulation.get_sim_config(
            track="data/tracks/Catalunya.csv",
            num_intervals=100,
            hessian_approximation="exact",
            is_cyclic=True,
            backend="jax",  # backend doesn't matter for the continuity constraints
            transcription="LGR",
        )

        cls.ocp = LaptimeSimulation(sim_config=cls.sim_config)

    def _test_linear_constraints(self, con: LinearConstraints):
        """Test a linear constraints is linear and with correct jacobian

        TODO: we could abstract this out, it's not really attached to any specific ocp.
        """

        x0 = np.random.randn(self.ocp.num_dec)

        # Test constraints
        c = con.constraints(x0)
        jac = con.jacobian(x0)

        for mult in np.random.randn(10):
            new_c = con.constraints(x0 * mult)
            np.testing.assert_allclose(
                c * mult,
                new_c,
                atol=1e-6,
                err_msg="Continuity constraints appear to be nonlinear!",
            )

            new_jac = con.jacobian(x0 * mult)
            np.testing.assert_allclose(
                new_jac,
                jac,
                atol=1e-6,
                err_msg="Continuity jacobian appear to be non-constant!",
            )

        # Check jacobian and structure is correct
        g = con.jacobian(x0)
        rows, cols = con.jacobianstructure()
        jac = csc_matrix((g, (rows, cols)), shape=(con.num_con, con.num_in))
        np.testing.assert_allclose(
            jac @ x0,
            c,
            atol=1e-6,
            err_msg="Continuity jacobian disagrees with linear constraints",
        )

    def test_continuity_constraints(self):
        """Test that continuity constraints is linear and with correct jacobian"""
        self._test_linear_constraints(self.ocp._constraints["continuity"])

        # Test the linear constraint for continuity is still valid after changing
        # mesh_scale - this is only true if we don't cache the jacobian. If we cache the
        # jacobian (in FixedMeshOCP._build_continuity_cons), then it would fail.
        original_mesh_scale = self.ocp._mesh_scale
        self.ocp.set_mesh_scale(original_mesh_scale * 2.0)
        self._test_linear_constraints(self.ocp._constraints["continuity"])
        self.ocp.set_mesh_scale(original_mesh_scale)

    def test_cyclic_constraints(self):
        """Test cyclic constraints is linear and really cyclic"""
        cyclic_con = self.ocp._constraints["cyclic"]
        self._test_linear_constraints(cyclic_con)

        x0 = np.ones(self.ocp.num_dec)
        op = self.ocp.dec_var_operator
        initial_idx = np.hstack(
            [
                op.get_group_indices_at_stage("states", 0),
                op.get_group_indices_at_stage("inputs", 0),
            ]
        )

        final_idx = np.hstack(
            [
                op.get_group_indices_at_stage("states", -1),
                op.get_group_indices_at_stage("inputs", -1),
            ]
        )

        vals = np.random.randn(initial_idx.size)
        x0[initial_idx] = vals
        x0[final_idx] = vals

        c = cyclic_con.constraints(x0)
        np.testing.assert_allclose(
            c,
            np.zeros_like(c),
            atol=1e-6,
            err_msg="Cyclic constraints returned non-zero values for cyclic inputs",
        )

    def test_modify_model_param(self):
        """WHEN a parameter is modified

        THEN the modified parameter is correctly updated
            the constraint function will output something different for the same input.
        """
        mass = 2301
        x0 = np.random.randn(self.ocp.num_dec)
        abs_con = np.mean(np.abs(self.ocp.constraints(x0)))

        self.ocp.modify_model_param("vehicle.vehicle_mass", mass)
        model_params = self.ocp.model.get_recursive_params()
        new_abs_con = np.mean(np.abs(self.ocp.constraints(x0)))

        self.assertAlmostEqual(self.ocp._params.get_param("vehicle.vehicle_mass"), mass)
        self.assertAlmostEqual(model_params.get_param("vehicle.vehicle_mass"), mass)

        # It's a little tricky setting 'how much they shouldn't be euqal'
        self.assertNotAlmostEqual(abs_con, new_abs_con, places=3)


# NOTE: disabled "limited-memory" test for now because the convergence is really bad...
# (eg, 470iter while "exact" can converge in 20)
@parameterized_class(
    [
        {"backend": "casadi"},
        # {"backend": "casadi", "hessian_approximation": "limited-memory"},
        {"backend": "casadi", "is_cyclic": False},
        {},
        {"is_condensed": True},
        {"is_cyclic": False},
        # {"hessian_approximation": "limited-memory"},
    ]
)
class TestLaptimeSimulationSolve(unittest.TestCase):
    hessian_approximation = "exact"
    is_cyclic = True
    is_condensed = False
    backend = "jax"

    @classmethod
    def setUpClass(cls):
        if cls.is_cyclic:
            boundary_conditions = (BoundaryConditionConfig(0, "states", "time", 0.0),)

        else:
            boundary_conditions = (
                BoundaryConditionConfig(0, "states", "time", 0.0),
                BoundaryConditionConfig(0, "states", "n", 0.0),
                BoundaryConditionConfig(0, "states", "eta", 0.0),
                BoundaryConditionConfig(0, "states", "vx", 30.0),
                BoundaryConditionConfig(0, "states", "vy", 0.0),
                BoundaryConditionConfig(0, "states", "yaw_rate", 0.0),
                BoundaryConditionConfig(-1, "states", "n", 0.0),
                BoundaryConditionConfig(-1, "states", "eta", 0.0),
                BoundaryConditionConfig(-1, "con_outputs", "slip_ratio_fl", 0.0),
            )
        cls.sim_config = LaptimeSimulation.get_sim_config(
            track="data/tracks/Catalunya.csv",
            num_intervals=250,
            hessian_approximation=cls.hessian_approximation,
            is_cyclic=cls.is_cyclic,
            is_condensed=cls.is_condensed,
            backend=cls.backend,
            transcription="LGR",
            boundary_conditions=boundary_conditions,
        )

        cls.ocp = LaptimeSimulation(sim_config=cls.sim_config)
        cls.solution, cls.info = cls.ocp.solve(
            init_guess=cls.ocp.get_init_guess(),
            print_level=5,
            max_iter=500,
            dual_inf_tol=1e-3,
            constr_viol_tol=1e-3,
        )

    def test_optimal(self):
        """Solution flag should be optimal."""
        self.assertEqual(self.info["status"], 0)

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

    def test_cyclic(self):
        """Test if cyclic constraints are satisfied."""

        if self.is_cyclic:
            for group in ["states", "inputs"]:
                for name in self.ocp.model.get_group_names(group):
                    # Time and track_heading won't be cyclic.
                    if group == "states" and name == "time":
                        continue
                    elif group == "inputs" and name == "track_heading":
                        continue
                    else:
                        start_value = self.ocp.dec_var_operator.get_var(
                            self.solution, group=group, name=name, stage=0
                        )
                        end_value = self.ocp.dec_var_operator.get_var(
                            self.solution, group=group, name=name, stage=-1
                        )
                        self.assertAlmostEqual(
                            start_value, end_value, delta=1e-3,
                        )
        else:
            # we just test that velocities are different, as there is no guarantee that
            # the states should be 'sufficiently different'. But we make the initial
            # states such that we know quite safely this is the case.
            v_start = self.ocp.dec_var_operator.get_var(
                self.solution, group="states", name="vx", stage=0
            )

            v_end = self.ocp.dec_var_operator.get_var(
                self.solution, group="states", name="vx", stage=-1
            )

            self.assertGreater(np.abs(v_end - v_start), 1.0)
