import numpy as np

import lumos.numpy as lnp


def sqeuclidean_distance(x, y):
    return lnp.sum((x - y) ** 2, axis=1)


def rbf_kernel(x, y):
    return lnp.exp(-sqeuclidean_distance(x, y))


def tanh_kernel(x, y):
    return lnp.tanh(-sqeuclidean_distance(x, y))


def poly_kernel(x, y):
    return lnp.sum((x - y) ** 2, axis=1)


def gp(x, gp_points, alpha):
    """Gaussian processes aero model"""

    # NOTE: need to do the vector_tile here because casadi does not use broadcast by
    # default.
    num_points = gp_points.shape[0]
    kxy = rbf_kernel(gp_points, lnp.vector_tile(x, num_points))
    return alpha @ kxy


def mlp(x, weights):
    """Dense fully connected neuralnet"""

    y = x
    for w in weights:
        y = lnp.tanh(w @ y)

    return y
