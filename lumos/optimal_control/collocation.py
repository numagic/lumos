from enum import auto, Enum
from typing import List

import numpy as np
from numpy.polynomial.legendre import Legendre
from numpy.polynomial.polynomial import Polynomial
from scipy.interpolate import lagrange


class CollocationEnum(Enum):
    """CollocationEnum Scheme enumeration.

    A collcation scheme consists of two main ingredients:
    - the position of the collocation point
    - the interpolating polynomial used

    See: https://hal.archives-ouvertes.fr/hal-01615132/document
    """

    LG = auto()
    LGR = auto()
    LGL = auto()


# FIXME: this is really just getting the Legendere root points, not collocation points
def get_collocation_points(
    num_points: int, scheme: CollocationEnum = CollocationEnum.LGR
) -> np.ndarray:
    """Retrieve 1D collocation points for a given scheme in the interval of [-1, 1]

    Note: Some methods include the end points of -1, 1, while some others don't.
    """

    if not isinstance(scheme, CollocationEnum):
        raise TypeError(
            f"Expected scheme to be of type {CollocationEnum}, but got {type(scheme)} instead"
        )

    # TODO: would this be different for different schemes?
    assert num_points >= 1

    # TODO: perhaps we should just combine everything into a Collocation Class
    if scheme == CollocationEnum.LGR:
        # root of Legendre polynomial, whrre P is a lgrange function
        # P_{N-1} + P_N = 0, but flipped around zero to include t=1
        coefficients = [0] * (num_points - 1) + [1, 1]
        characteristic_polynomial = Legendre(coefficients)

        # solve and flip
        collocation_points = -characteristic_polynomial.roots()[::-1]
    elif scheme == CollocationEnum.LG:
        # roots of P_N = 0
        coefficients = [0] * num_points + [1]
        characteristic_polynomial = Legendre(coefficients)
        collocation_points = characteristic_polynomial.roots()
    elif scheme == CollocationEnum.LGL:
        # roots of P_dot_{N-1} + [-1, 1]
        coefficients = [0] * (num_points - 1) + [1]
        characteristic_polynomial = Legendre(coefficients).deriv()
        collocation_points = np.append(
            np.insert(characteristic_polynomial.roots(), 0, -1), 1
        )
    else:
        raise NotImplemented(scheme)
    return collocation_points


def make_lagrange_polynomial(support: np.ndarray, index: int) -> Polynomial:
    """Create the i-th lagrange polynomial"""

    weights = np.zeros_like(support)
    weights[index] = 1

    # NOTE: lagrange returns coef in decending power order, which is opposite to numpy
    # Polynomials.
    coefficients = lagrange(support, weights).coef[::-1]
    return Polynomial(coefficients)


def make_lagrange_basis(support: np.ndarray) -> List[Polynomial]:
    """Create a list of lagrange basis of varying order on the same support."""

    return [make_lagrange_polynomial(support, index) for index in range(len(support))]


def build_lagrange_differential_matrix(
    support: np.ndarray, evaluation_points: np.ndarray
) -> np.ndarray:
    """Differential matrix for computing the derivative of a lagrange polynomial using
    linear matrix vector multiplication"""

    lagrange_basis = make_lagrange_basis(support)
    polynomials = [
        lagrange_polynomial.deriv() for lagrange_polynomial in lagrange_basis
    ]

    return np.array([p(evaluation_points) for p in polynomials]).T


def build_lagrange_integration_matrix(
    support: np.ndarray, evaluation_points: np.ndarray
) -> np.ndarray:
    """Integration matrix for computing the definitive integral of a lagrange polynomial using
    linear matrix vector multiplication"""

    lagrange_basis = make_lagrange_basis(support)
    polynomials = [
        lagrange_polynomial.integ() for lagrange_polynomial in lagrange_basis
    ]

    # NOTE: eq39, the integral polynomial is a definite integral, so need to call the
    # integral twice to remove the part for tau < support[0]
    return np.array([p(evaluation_points) - p(support[0]) for p in polynomials]).T
