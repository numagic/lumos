import logging
import numpy as np
from typing import Any, Union

import casadi
import jax.numpy as jnp
import lumos.numpy.casadi_numpy as cnp
from jax.config import config

from lumos.numpy.utils import (
    is_jax_array,
    vector_concat,
    vector_split,
    assert_allclose,
    use_backend,
    vector_tile,
    cmap,
    lmap,
)

logger = logging.getLogger(__name__)

# Enable double precision by default
config.update("jax_enable_x64", True)

__BACKEND_MAP = {"jax": jnp, "numpy": np, "casadi": cnp}
# Use numpy as default backend
__BACKEND = "numpy"

ndarray = Union[np.ndarray, jnp.ndarray, casadi.SX, casadi.MX]


def get_backend() -> str:
    return __BACKEND


def set_backend(backend: str) -> None:
    """Set a numerical backend for model computation."""

    global __BACKEND
    if backend in __BACKEND_MAP:
        __BACKEND = backend
    else:
        logger.warn(
            f"{backend} is not a valid backend. Staying with {__BACKEND} backend"
        )


def __getattr__(name: str):
    """Switcheable backend by overriding the namespace.

    FIXME: The price paid is no more auto-completion.
    """

    return getattr(__BACKEND_MAP[__BACKEND], name)
