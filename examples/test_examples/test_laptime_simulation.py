from unittest import TestCase

from examples.laptime_simulation_example import main as ltc_main


class TestLaptimeSimulationExample(TestCase):
    def test_laptime_simulation(self):
        """Simple smoke test for laptime simulation example"""
        ltc_main()
