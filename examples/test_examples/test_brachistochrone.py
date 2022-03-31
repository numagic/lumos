from unittest import TestCase

from parameterized import parameterized

from examples.brachistochrone import solve_brachistochrone


class TestBrachistochrone(TestCase):
    """Test Brachistochrone example runs and returns correct answer.

    Correct answer taken from: https://scipython.com/blog/the-brachistochrone-problem/
    """

    def test_distance_domain(self):
        """Test distance based formulation with fixed grid.

        This is harder to converge, and then to be less robust.
        """
        t = solve_brachistochrone(1.0, -0.65, time_domain=False)
        self.assertAlmostEqual(t, 0.566, places=3)

    @parameterized.expand(["jax", "casadi", "custom"])
    def test_time_domain(self, backend: str):
        """Test time based formulation, with scaled grid."""
        t = solve_brachistochrone(1.0, -0.65, backend=backend)
        self.assertAlmostEqual(t, 0.566, places=3)
