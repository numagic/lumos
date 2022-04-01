from unittest import TestCase

from lumos.models.composition import ModelMaker
from lumos.simulations.laptime_simulation import LTCConfig
from lumos.simulations.laptime_simulation import LaptimeSimulation


class TestLTCConfig(TestCase):
    def test_to_dict_and_back(self):
        """Test values remain the same when converting to dictionary and back"""
        config = LTCConfig(track="Barcelona")

        config_dict = config.to_dict()
        self.assertEqual(config, LTCConfig(**config_dict))
        self.assertDictEqual(config_dict, LTCConfig(**config_dict).to_dict())

    def test_set_track(self):
        """Should raise ValueError if no track is defined"""
        with self.assertRaises(ValueError):
            config = LTCConfig()

        expected_str = "/tracks/Barcelona"
        config = LTCConfig(track=expected_str)
        self.assertEqual(config.track, expected_str)

    def test_set_cyclic(self):
        """Ensure time and track heading are not made cyclic"""

        # If not specified, must also automtically add the reuqired non_cyclic_vars
        always_non_cyclic = ["states.time", "inputs.track_heading"]
        inputs_to_test = [["var1", "var2"], always_non_cyclic, ["states.time", "var2"]]
        for inputs in inputs_to_test:
            config = LTCConfig(track="Barcelona", non_cyclic_vars=inputs)
            for v in set(inputs + always_non_cyclic):
                self.assertIn(v, config.non_cyclic_vars)
                self.assertIn(v, config.non_cyclic_vars)


# TODO: currently test_optimal_control/test_fixed_grid.py already tests LTC. Maybe we
# should test that one with a dummy model, and test ltc solve here?
class TestLaptimeSimulationWithoutSolve(TestCase):
    def setUp(self):
        pass

    def test_set_track(self):
        ltc_config = LaptimeSimulation.get_sim_config(track="data/tracks/Catalunya.csv")
        model_config = ModelMaker.make_config("SimpleVehicleOnTrack")
        ltc = LaptimeSimulation(model_config=model_config, sim_config=ltc_config)
        pass

    def test_change_track(self):
        pass

    pass
