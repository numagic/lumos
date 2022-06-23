from unittest import TestCase

import numpy as np
import jax.numpy as jnp
import jax

from lumos.optimal_control.nlp import BaseConstraints, BaseObjective

# TODO: add other constraint tests: eg, MappedConstraints, LinearConstraints, etc.


class ADFunction:
    def __init__(self, num_in, num_con, input_scales=None, con_scales=None):
        """Ground truth helper from scratch, using AD.

        original function y = f(x)
        scaled version y_hat = f(x_hat)

        where x = x_hat * input_scale
              y = y_hat * con_scale

        So x_hat and y_hat are both 'scaled' or 'normalzed'
        """

        self.num_in, self.num_con = num_in, num_con
        if input_scales is None:
            self.input_scales = np.ones(self.num_in)
        else:
            self.input_scales = input_scales

        if con_scales is None:
            self.con_scales = np.ones(self.num_con)
        else:
            self.con_scales = con_scales

        # generate random coefficients for a quadratic, with fixed seed for repeatibility
        # f(x): 0.5*x'Ax + bx + c
        rng = np.random.default_rng(2022)
        self.A = rng.random((self.num_con, self.num_in, self.num_in))
        self.b = rng.random((self.num_con, self.num_in))
        self.c = rng.random(self.num_con)

    def constraints(self, x_hat):
        # unscale x
        x = x_hat * self.input_scales
        # return scaled constraints
        return (0.5 * x @ self.A @ x + self.b @ x + self.c) / self.con_scales

    def jacobian(self, x_hat):
        return jax.jacobian(self.constraints)(x_hat).ravel()

    def lagrangian(self, x_hat, lagrange):
        return jnp.dot(self.constraints(x_hat), lagrange)

    def hessian(self, x_hat, lagrange=None):
        if lagrange is None:
            lagrange = np.ones(self.num_con)
        return jax.hessian(self.lagrangian)(x_hat, lagrange).ravel()


class TestBaseConstraints(TestCase):
    num_in = 5
    num_con = 2

    def _set_scales_and_test(self, input_scales=None, con_scales=None):
        if input_scales is None:
            input_scales = np.ones(self.num_in)
        else:
            input_scales = input_scales

        if con_scales is None:
            con_scales = np.ones(self.num_con)
        else:
            con_scales = con_scales

        # This one bakes the scaling into the AD, as a ground truth.
        scaled_fn = ADFunction(self.num_in, self.num_con, input_scales, con_scales)
        gt_con = BaseConstraints(
            num_in=self.num_in,
            num_con=self.num_con,
            constraints=scaled_fn.constraints,
            jacobian=scaled_fn.jacobian,
            hessian=scaled_fn.hessian,
        )

        # This one relies on the BaseConstraints class for scaling
        unscaled_fn = ADFunction(self.num_in, self.num_con)
        manual_con = BaseConstraints(
            num_in=self.num_in,
            num_con=self.num_con,
            constraints=unscaled_fn.constraints,
            jacobian=unscaled_fn.jacobian,
            hessian=unscaled_fn.hessian,
        )
        manual_con.set_input_scales(input_scales)
        manual_con.set_con_scales(con_scales)

        # This is the scaled input
        x = np.random.randn(self.num_in)

        # Test on constraints
        expected = gt_con.constraints(x)
        actual = manual_con.constraints(x)
        np.testing.assert_array_almost_equal(expected, actual)

        # Test on jacobian
        expected = gt_con.jacobian(x)
        actual = manual_con.jacobian(x)
        np.testing.assert_array_almost_equal(expected, actual)

        # Test on hessian
        lagrange = np.arange(self.num_con, dtype=np.double)
        expected = gt_con.hessian(x, lagrange)
        actual = manual_con.hessian(x, lagrange)
        np.testing.assert_array_almost_equal(expected, actual)

    def test_set_input_scales(self):
        """Test setting input scales only"""
        input_scales = np.linspace(1, 5, self.num_in)
        self._set_scales_and_test(input_scales=input_scales)

    def test_set_con_scales(self):
        """Test setting constraint scales only"""
        con_scales = np.linspace(5, 10, self.num_con)
        self._set_scales_and_test(con_scales=con_scales)

    def test_set_input_and_con_scales(self):
        """Test setting both input and constraint scales"""
        input_scales = np.linspace(1, 5, self.num_in)
        con_scales = np.linspace(5, 10, self.num_con)
        self._set_scales_and_test(input_scales=input_scales, con_scales=con_scales)


class TestBaseObjective(TestCase):
    """
    TODO:
    1) con set_input scales test
    2) con combined input and con scale test
    3) objective input scale test
    4) change name to test_constraints_and_objectives.py
    """

    def __init__(self, num_in, num_con, input_scales=None, con_scales=None):
        """Ground truth helper from scratch, using AD.

        original function y = f(x)
        scaled version y_hat = f(x_hat)

        where x = x_hat * input_scale
              y = y_hat * con_scale

        So x_hat and y_hat are both 'scaled' or 'normalzed'
        """

        self.num_in, self.num_con = num_in, num_con
        if input_scales is None:
            self.input_scales = np.ones(self.num_in)
        else:
            self.input_scales = input_scales

        if con_scales is None:
            self.con_scales = np.ones(self.num_con)
        else:
            self.con_scales = con_scales

        # generate random coefficients for a quadratic, with fixed seed for repeatibility
        # f(x): 0.5*x'Ax + bx + c
        rng = np.random.default_rng(2022)
        self.A = rng.random((self.num_con, self.num_in, self.num_in))
        self.b = rng.random((self.num_con, self.num_in))
        self.c = rng.random(self.num_con)

    def constraints(self, x_hat):
        # unscale x
        x = x_hat * self.input_scales
        # return scaled constraints
        return (0.5 * x @ self.A @ x + self.b @ x + self.c) / self.con_scales

    def jacobian(self, x_hat):
        return jax.jacobian(self.constraints)(x_hat).ravel()

    def lagrangian(self, x_hat, lagrange):
        return jnp.dot(self.constraints(x_hat), lagrange)

    def hessian(self, x_hat, lagrange):
        return jax.hessian(self.lagrangian)(x_hat, lagrange).ravel()


class TestBaseObjective(TestCase):
    num_in = 7

    def _set_scales_and_test(self, input_scales=None, con_scales=None):
        if input_scales is None:
            input_scales = np.ones(self.num_in)
        else:
            input_scales = input_scales

        # This one bakes the scaling into the AD, as a ground truth.
        scaled_fn = ADFunction(self.num_in, 1, input_scales)
        gt_con = BaseObjective(
            num_in=self.num_in,
            objective=scaled_fn.constraints,
            gradient=scaled_fn.jacobian,
            hessian=scaled_fn.hessian,
        )

        # This one relies on the BaseConstraints class for scaling
        unscaled_fn = ADFunction(self.num_in, 1)
        manual_con = BaseObjective(
            num_in=self.num_in,
            objective=unscaled_fn.constraints,
            gradient=unscaled_fn.jacobian,
            hessian=unscaled_fn.hessian,
        )
        manual_con.set_input_scales(input_scales)

        # This is the scaled input
        x = np.random.randn(self.num_in)

        # Test on objective
        expected = gt_con.objective(x)
        actual = manual_con.objective(x)
        np.testing.assert_array_almost_equal(expected, actual)

        # Test on gradient
        expected = gt_con.gradient(x)
        actual = manual_con.gradient(x)
        np.testing.assert_array_almost_equal(expected, actual)

        # Test on hessian
        expected = gt_con.hessian(x)
        actual = manual_con.hessian(x)
        np.testing.assert_array_almost_equal(expected, actual)

    def test_set_input_scales(self):
        """Test setting input scales only"""
        input_scales = np.linspace(1, 5, self.num_in)
        self._set_scales_and_test(input_scales=input_scales)
