import casadi as cas
from lumos.numpy.casadi_numpy.conditionals import where


def interp(x, xp, fp, left=None, right=None, period=None):
    """One-dimensional linear interpolation, analogous to numpy.interp().

    does not handle period yet.
    see: https://jax.readthedocs.io/en/latest/_autosummary/jax.numpy.interp.html
    """
    if period is not None:
        raise NotImplemented("Handling of period are not implemented yet")
    # Casadi supports 'bspline' and 'linear'
    lut = cas.interpolant("LUT", "linear", [xp], fp)
    f = lut(x)

    # Left and right default to end values, like jax.numpy
    if left is None:
        left = fp[0]

    if right is None:
        right = fp[-1]

    f = where(x < xp[0], left, f)
    f = where(x > xp[-1], right, f)

    return f
