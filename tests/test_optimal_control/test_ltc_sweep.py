import unittest

import numpy as np
from parameterized import parameterized_class

from lumos.optimal_control.config import BoundaryConditionConfig
from lumos.simulations.laptime_simulation import LaptimeSimulation
from lumos.models.simple_vehicle_on_track import SimpleVehicleOnTrack


@parameterized_class([{"backend": "casadi"}, {"backend": "jax"}])
class TestLTCSweep(unittest.TestCase):
    """Sweep mass parameter and solve

    This test mainly tests two things:
    1) the laptime converges to a reasonable optimum, that it monotonically increases
    with mass (robustness and accuracy)
    2) the parameter changing mechanism is working as expected

    TODO:
    Arguably the 2nd point can be made into a smaller unit test which only calls the nlp
    functions without doing the solve
    """

    @classmethod
    def setUpClass(cls) -> None:
        """Construct an LTC problem"""
        model_config = SimpleVehicleOnTrack.get_recursive_default_model_config()
        model = SimpleVehicleOnTrack(model_config=model_config)
        params = model.get_recursive_default_params()

        sim_config = LaptimeSimulation.get_sim_config(
            track="data/tracks/Catalunya.csv",
            num_intervals=100,
            hessian_approximation="exact",
            is_cyclic=True,
            backend=cls.backend,
            transcription="LGR",
            boundary_conditions=(BoundaryConditionConfig(0, "states", "time", 0.0),),
        )

        cls.ocp = LaptimeSimulation(
            sim_config=sim_config, model_params=params, model_config=model_config
        )

    def _set_param_and_solve(self, path, value):
        self.ocp.modify_model_param(path, value)

        solution, info = self.ocp.solve(
            init_guess=self.ocp.get_init_guess(),
            print_level=5,
            max_iter=500,
            dual_inf_tol=1e-3,
            constr_viol_tol=1e-3,
        )

        total_time = self.ocp.dec_var_operator.get_var(
            solution, group="states", name="time", stage=-1
        )
        return total_time, info["status"]

    def test_mass_sweep(self):
        path = "vehicle.vehicle_mass"
        values = np.linspace(1600, 2400, 5)

        laptimes = []
        for v in values:
            t, status = self._set_param_and_solve(path, v)
            self.assertEqual(status, 0, msg="solve status not optimal for mass={v:.1f}")
            laptimes.append(t)

        print(laptimes)

        self.assertTrue(
            np.all(np.diff(laptimes) > 0.01),
            msg="laptime not monotonically increasing with mass",
        )
