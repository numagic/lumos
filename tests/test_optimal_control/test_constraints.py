from unittest import TestCase

import numpy as np

from lumos.optimal_control.nlp import BaseConstraints

# TODO: add other constraint tests: eg, MappedConstraints, LinearConstraints, etc.


class TestBaseConstraints(TestCase):
    def setUp(self):

        # Create a quadratic with analytical solutions
        # f(x): 0.5*x'Ax + bx + c
        num_in, num_con = 5, 2

        A = np.random.randn(num_con, num_in, num_in)
        b = np.random.randn(num_con, num_in)
        c = np.random.randn(num_con)

        def constraints(x):
            return 0.5 * x @ A @ x + b @ x + c

        def jacobian(x):
            return np.ravel(A @ x + b)

        def hessian(x, lagrange):
            hess = np.einsum("i, ijk->jk", lagrange, A)
            return np.ravel(hess)

        self._gt_constraints = constraints
        self._gt_jacobian = jacobian
        self._gt_hessian = hessian

        self._original_con = BaseConstraints(
            num_in=num_in,
            num_con=num_con,
            constraints=constraints,
            jacobian=jacobian,
            hessian=hessian,
        )

        self._scaled_con = BaseConstraints(
            num_in=num_in,
            num_con=num_con,
            constraints=constraints,
            jacobian=jacobian,
            hessian=hessian,
        )

    def test_set_con_scales(self):
        """When a constraint is scaled, the con/jac/hss are scaled correctly"""

        num_in = self._original_con.num_in
        num_con = self._original_con.num_con
        x = np.random.randn(num_in)
        con_scales = np.linspace(1, 10, num_con)
        self._scaled_con.set_con_scales(con_scales)

        # Test on constraints
        expected = self._original_con.constraints(x) / con_scales
        actual = self._scaled_con.constraints(x)
        np.testing.assert_array_almost_equal(expected, actual)

        # Test on jacobian
        expected = (
            np.diag(1 / con_scales) @ self._original_con.get_csc_jacobian(x).toarray()
        )
        actual = self._scaled_con.get_csc_jacobian(x).toarray()
        np.testing.assert_array_almost_equal(expected, actual)

        # Test on hessian
        lagrange = np.arange(num_con, dtype=np.double)
        expected = self._original_con.get_csc_hessian(
            x, lagrange / con_scales
        ).toarray()
        actual = self._scaled_con.get_csc_hessian(x, lagrange).toarray()
        np.testing.assert_array_almost_equal(expected, actual)
