import unittest

import numpy as np
from scipy.interpolate import lagrange

from lumos.optimal_control.transcription import (
    get_transcription_options,
    make_transcription,
    ForwardEuler,
    Trapezoidal,
    LGR,
    LGRIntegral,
)


class TestMakeTranscription(unittest.TestCase):
    def test_make_LGR(self):
        transcription = make_transcription("LGR", {"num_stages": 3})
        self.assertIsInstance(transcription, LGR)
        self.assertEqual(transcription.num_stages_per_interval, 3)

    def test_make_ForwardEuler(self):
        transcription = make_transcription("ForwardEuler")
        self.assertIsInstance(transcription, ForwardEuler)
        self.assertEqual(transcription.num_stages_per_interval, 2)

    def test_make_Trapezoidal(self):
        transcription = make_transcription("Trapezoidal")
        self.assertIsInstance(transcription, Trapezoidal)
        self.assertEqual(transcription.num_stages_per_interval, 2)

    def test_make_LGRIntegral(self):
        transcription = make_transcription("LGRIntegral", {"num_stages": 5})
        self.assertIsInstance(transcription, LGRIntegral)
        self.assertEqual(transcription.num_stages_per_interval, 5)

    def test_make_something_wrong(self):
        # Type not supported
        with self.assertRaises(RuntimeError):
            transcription = make_transcription("LGL")

        # Unwanted input arguments, the constructor should raise TypeError
        with self.assertRaises(TypeError):
            transcription = make_transcription("ForwardEuler", {"someargs": 1.0})

    def test_get_and_make_transcriptions(self):
        options = get_transcription_options()

        for name in options:
            transcription = make_transcription(name)
            self.assertEqual(transcription.__class__.__name__, name)


class TestTranscription(unittest.TestCase):
    def test_LGR_continuity(self):
        """Test LGR differentiation and residual computations are correct"""
        num_stages = 5
        lgr = make_transcription("LGR", {"num_stages": num_stages})
        A_diff, B_diff = lgr.get_continuity_matrices()
        x = np.random.randn(num_stages)
        s = lgr.interp_points
        poly = lagrange(s, x)

        # Test derivatives are correct.
        x_dot_expected = poly.deriv()(s[1:])
        x_dot_actual = A_diff @ x
        np.testing.assert_array_almost_equal(x_dot_actual, x_dot_expected)

        # Test with the correct x and x_dot, continuity equations are satisfied
        # need to add an x_dot to the first point to make size match. The first point of
        # x_dot is not collocated, so we can add any random number..
        res = A_diff @ x - B_diff @ np.insert(x_dot_expected, 0, 0)
        np.testing.assert_array_almost_equal(res, np.zeros_like(res))

    def test_LGRIntegral_continuity(self):
        """Test LGRIntegral integral and residual computations are correct"""
        num_stages = 5
        lgr_int = make_transcription("LGRIntegral", {"num_stages": num_stages})
        A, B = lgr_int.get_continuity_matrices()
        x = np.random.randn(num_stages)
        s = lgr_int.interp_points
        poly = lagrange(s, x)
        x_dot_actual = poly.deriv()(s)

        # Test integrals are correct.
        x_actual = x[0] + B @ x_dot_actual
        x_expected = x[1:]
        np.testing.assert_array_almost_equal(x_actual, x_expected)

        # Test with the correct x and x_dot, continuity equations are satisfied
        res = A @ x - B @ x_dot_actual
        np.testing.assert_array_almost_equal(res, np.zeros_like(res))

    def test_LGR_invertible(self):
        """LGR scheme can be inverted to reconstruct states from derivatives.
        
        See equation 72-73 on Garg, Rao, et al, 2017, https://hal.archives-ouvertes.fr/hal-01615132
        An overview of three pseudospectral methods for the numerical solution of
        optimal control problems
        """

        num_stages = 5
        lgr = make_transcription("LGR", {"num_stages": num_stages})
        A, B = lgr.get_continuity_matrices()

        x = np.sin(5 * np.linspace(0, 1, num_stages))
        x_dot = A @ x

        x_reconstructed = np.linalg.solve(A[:, 1:], x_dot) + x[0]

        np.testing.assert_array_almost_equal(x_reconstructed, x[1:])
