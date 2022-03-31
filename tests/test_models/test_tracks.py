import numpy as np
from unittest import TestCase

from parameterized import parameterized, parameterized_class

from lumos.models.tracks import (
    RaceTrack,
    cartesian_to_curvilinear,
    curvilinear_to_cartesian,
)


def generate_circle(curvature: float, num_points: int = 1000):

    radius = 1 / curvature
    curvature = np.ones(num_points) * curvature
    s = np.pi * 2 * np.abs(radius) * np.linspace(0, 1, num_points)

    # polar angle
    theta = curvature * s

    # circle starts at 3 o'lock position
    heading = theta + np.pi / 2
    x = np.cos(theta) * radius
    y = np.sin(theta) * radius

    assert heading[-1] - heading[0] == np.pi * 2 * (np.sign(radius))

    return {"x": x, "y": y, "s": s, "curvature": curvature, "heading": heading}


class TestTrackUtils(TestCase):
    @parameterized.expand([(1e-3,), (-1e-3,)])
    def test_cartesian_to_curvilinear(self, expected_curvature):
        """Test cartesian_to_curvilinear utility against a tractable track: a circle"""

        expected_results = generate_circle(curvature=expected_curvature)

        s, curvature, heading = cartesian_to_curvilinear(
            x=expected_results["x"], y=expected_results["y"]
        )

        # NOTE: the accuracy is affected by how many points we have on the circle
        np.testing.assert_allclose(s, expected_results["s"], rtol=1e-3, atol=1e-3)
        # first and last couple of elements of curvature would be off due to finite
        # difference, so we ignore them.
        np.testing.assert_allclose(
            curvature[2:-2],
            expected_results["curvature"][2:-2],
            rtol=1e-3,
            atol=1e-4,
        )
        np.testing.assert_allclose(
            heading, expected_results["heading"], rtol=1e-2, atol=1e-2
        )

    @parameterized.expand([(1e-3,), (-1e-3,)])
    def test_curvilinear_to_cartesian(self, expected_curvature):
        """Test curvilinear_to_cartesian utility against a tractable track: a circle"""
        expected_results = generate_circle(curvature=expected_curvature)

        x, y, heading = curvilinear_to_cartesian(
            s=expected_results["s"],
            curvature=expected_results["curvature"],
            x0=expected_results["x"][0],
            y0=expected_results["y"][0],
            heading0=expected_results["heading"][0],
        )

        # NOTE: the accuracy is affected by how many points we have on the circle
        np.testing.assert_allclose(x, expected_results["x"], rtol=1e-2, atol=1e-2)
        np.testing.assert_allclose(y, expected_results["y"], rtol=1e-2, atol=1e-2)
        np.testing.assert_allclose(
            heading, expected_results["heading"], rtol=1e-2, atol=1e-2
        )


@parameterized_class(
    [
        {"expected_curvature": 1e-3},
        {"expected_curvature": -1e-3},
    ]
)
class TestTrack(TestCase):
    expected_curvature = 1e-3

    def _test_against_expected(self, track):
        # first and last couple of elements of curvature would be off due to finite
        # difference, so we ignore them.
        np.testing.assert_allclose(
            track.curvature_at(self.expected_results["s"][2:-2]),
            self.expected_results["curvature"][2:-2],
            rtol=1e-3,
            atol=1e-4,
        )
        np.testing.assert_allclose(
            track.heading_at(self.expected_results["s"]),
            self.expected_results["heading"],
            rtol=1e-2,
            atol=1e-2,
        )

    def setUp(self):
        self.expected_results = generate_circle(curvature=self.expected_curvature)

    def test_from_cartesian(self):
        track = RaceTrack.from_cartesian(
            x=self.expected_results["x"], y=self.expected_results["y"]
        )

        self._test_against_expected(track)

    def test_from_curvilinear(self):
        track = RaceTrack.from_curvilinear(
            s=self.expected_results["s"],
            curvature=self.expected_results["curvature"],
            heading0=self.expected_results["heading"][0],
        )

        self._test_against_expected(track)
