from unittest import TestCase

from examples.drone_example import main as drone_main


class TestDroneExample(TestCase):
    def test_drone_simulation(self):
        """Simple smoke test for drone simulation example"""
        drone_main()
