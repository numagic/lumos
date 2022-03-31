import itertools
import unittest

import numpy as np
from numpy.testing import assert_allclose
from parameterized import parameterized

from lumos.optimal_control.collocation import (
    build_lagrange_differential_matrix,
    CollocationEnum,
    build_lagrange_integration_matrix,
    get_collocation_points,
)


class LG:
    """Hand-coded helper Lengendre polynomials.

    see: https://en.wikipedia.org/wiki/Legendre_polynomials
    """

    def p8(x):
        return (
            1
            / 128
            * (6435 * x ** 9 - 12012 * x ** 6 + 6930 * x ** 4 - 1260 * x ** 2 + 35)
        )

    def p9(x):
        return (
            1
            / 128
            * (
                12155 * x ** 9
                - 25740 * x ** 7
                + 18018 * x ** 5
                - 4620 * x ** 3
                + 315 * x
            )
        )

    def p9_dot(x):
        return (
            1
            / 128
            * (
                9 * 12155 * x ** 8
                - 7 * 25740 * x ** 6
                + 5 * 18018 * x ** 4
                - 3 * 4620 * x ** 2
                + 315
            )
        )

    def p10(x):
        return (
            1
            / 256
            * (
                46189 * x ** 10
                - 109395 * x ** 8
                + 90090 * x ** 6
                - 30030 * x ** 4
                + 3465 * x ** 2
                - 63
            )
        )

    def p10_dot(x):
        return (
            1
            / 256
            * (
                10 * 46189 * x ** 9
                - 8 * 109395 * x ** 7
                + 6 * 90090 * x ** 5
                - 4 * 30030 * x ** 3
                + 2 * 3465 * x
            )
        )


class TestCollocation(unittest.TestCase):
    @parameterized.expand(tuple(itertools.product(CollocationEnum, [2, 10])))
    def test_get_collocation_points(self, collocation_method, num_collocation_points):
        """Test collocation points by:
        - check against known roots of charateerization polynomials
        - comparing to hard-coded ground truth.
        """
        collocation_points = get_collocation_points(
            num_collocation_points, collocation_method
        )

        # Check correct size and correctly ordered
        assert len(set(collocation_points)) == num_collocation_points
        assert np.all(collocation_points == sorted(collocation_points))

        if collocation_method == CollocationEnum.LGR:
            if num_collocation_points == 2:
                # This characteristic polynomial is a quadratic, we could solve by hand.
                # Q = 3/2*x^2 + x - 0.5 = 0 ==> x = -1 or 1/3
                # then flip to -1/3 and 1
                assert_allclose(collocation_points, [-1 / 3, 1])
            elif num_collocation_points == 10:
                residuals = [LG.p10(-x) + LG.p9(-x) for x in collocation_points]
                assert_allclose(residuals, np.zeros_like(residuals), atol=1e-9)
        elif collocation_method == CollocationEnum.LG:
            # Q = 3/2*x^2 - 0.5 = 0 ==> solve by hand
            if num_collocation_points == 2:
                sol = np.sqrt(4 * 0.5 * 3 / 2) / 3
                assert_allclose(collocation_points, [-sol, sol])
            elif num_collocation_points == 10:
                residuals = [LG.p10(x) for x in collocation_points]
                assert_allclose(residuals, np.zeros_like(residuals), atol=1e-9)
        elif collocation_method == CollocationEnum.LGL:
            if num_collocation_points == 2:
                assert_allclose(collocation_points, [-1, 1])
            elif num_collocation_points == 10:
                # First and last points are included in LGL
                self.assertAlmostEqual(collocation_points[0], -1)
                self.assertAlmostEqual(collocation_points[-1], 1)

                residuals = [LG.p9_dot(x) for x in collocation_points[1:-1]]
                assert_allclose(residuals, np.zeros_like(residuals), atol=1e-9)
        else:
            raise NotImplementedError(collocation_method)

    @unittest.skip("To be implemented")
    def test_lagrange_interpolation(self):
        "Test if the interpolation goes through the points exactly."

        # TODO: to be implemented
        raise NotImplementedError

    def test_build_lagrange_differential_matrix(self):
        """Test differential matrix against manually derived ground truth."""

        support = np.array([0.0, 2.0, 5])
        evaluation_points = np.array([2.0, 5])
        differential_matrix = build_lagrange_differential_matrix(
            support, evaluation_points
        )

        # Manually derived derivatives
        derivatives = [
            lambda x: -7 / 10 + 1 / 5 * x,
            lambda x: 5 / 6 - 1 / 3 * x,
            lambda x: -2 / 15 + 2 / 15 * x,
        ]

        expected = np.array([[f(x) for f in derivatives] for x in evaluation_points])
        assert_allclose(differential_matrix, expected)

    def test_build_lagrange_build_lagrange_integration_matrix(self):
        """Test integration matrix against manually derived ground truth."""

        support = np.array([0.0, 2.0, 5])
        evaluation_points = np.array([2.0, 5])
        integration_matrix = build_lagrange_integration_matrix(
            support, evaluation_points
        )

        # Manually derived integrals
        integrals = [
            lambda x: x - 7 / 20 * x ** 2 + 1 / 30 * x ** 3,
            lambda x: 5 / 12 * x ** 2 - 1 / 18 * x ** 3,
            lambda x: -1 / 15 * x ** 2 + 1 / 45 * x ** 3,
        ]

        expected = np.array([[f(x) for f in integrals] for x in evaluation_points])
        assert_allclose(integration_matrix, expected)
