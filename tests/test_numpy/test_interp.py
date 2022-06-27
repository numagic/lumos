from unittest import TestCase
from typing import Callable, List


import casadi as cas
import numpy as onp
from parameterized import parameterized

import lumos.numpy as lnp


class TestInterp(TestCase):
    @parameterized.expand([["casadi"], ["jax"]])
    def test_interp(self, backend: str):
        num_points = 11
        xp = onp.linspace(0, 1, num_points)
        fp = onp.sin(xp)

        # NOTE: we test also out of range behaviour
        for x in [-1.0, 0.0, 0.314, 1.0, 2.0]:
            expected = onp.interp(x, xp, fp)
            with lnp.use_backend(backend):
                if backend == "jax":
                    actual = lnp.interp(x, xp, fp)
                elif backend == "casadi":
                    # For casadi, we test the one with symbolic evaluation
                    x_sym = cas.MX.sym("x", 1)
                    fun = cas.Function("fun", [x_sym], [lnp.interp(x_sym, xp, fp)])
                    actual = float(fun(x))
            self.assertAlmostEqual(actual, expected)
