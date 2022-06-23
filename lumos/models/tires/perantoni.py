import logging
from typing import Any, Dict

import numpy as np

import lumos.numpy as lnp
from lumos.models.base import model_io, ModelReturn
from lumos.models.tires.base import BaseTire

logger = logging.getLogger(__name__)


@model_io(
    inputs=(
        "Fz",  # vertical load
        "kappa",  # slip ratio
        "alpha",  # slip angle
        "vx",  # x-velocity in tire coordinate
        "gamma",  # inclination angle
    ),
    outputs=(
        "Fx",
        "Fy",
        "Mx",
        "My",
        "Mz",
    ),
)
class PerantoniTire(BaseTire):
    """Tire model used in Perantoni Paper
    Optimal Control of F1 with variable parameters.

    Perantoni papers sticks to some werid sign convention (Fz -ve, omega -ve).
    We make slight modifications to adopt iso convention, which is the same as used in
    MF5.2. See page 29 of:
    https://functionbay.com/documentation/onlinehelp/Documents/Tire/MFTire-MFSwift_Help.pdf

    As a result:
    - longitudinal slip and force are the same sign
    - lateral slip and force are the opposite sign.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def forward(self, inputs: Dict[str, float]):
        """Perantoni Apendix A, page 32"""
        params = self._params

        # unpack inputs
        kappa = inputs["kappa"]
        alpha = inputs["alpha"]
        Fz = inputs["Fz"]

        # unpack parameters
        Fz1 = params["Fz1"]
        Fz2 = params["Fz2"]
        mux1 = params["mux1"]
        mux2 = params["mux2"]
        muy1 = params["muy1"]
        muy2 = params["muy2"]
        kappa1 = params["kappa1"]
        kappa2 = params["kappa2"]
        alpha1 = params["alpha1"]
        alpha2 = params["alpha2"]
        Qx = params["Qx"]
        Qy = params["Qy"]

        # NOTE: here there are some inconsistency in the paper regarding parameter names
        # in the parameters, we have mux1, mux2, but in equations we have mux_max1, mux_max2
        # TODO: these are just linear interpolation, could abstract out.
        interp_val = (Fz - Fz1) / (Fz2 - Fz1)
        mux_max = interp_val * (mux2 - mux1) + mux1
        muy_max = interp_val * (muy2 - muy1) + muy1
        kappa_max = interp_val * (kappa2 - kappa1) + kappa1
        alpha_max = interp_val * (alpha2 - alpha1) + alpha1

        kappa_n = kappa / kappa_max
        alpha_n = alpha / alpha_max

        # NOTE: we need to add a jitter here to avoid divide by zero error at 0 slip
        jitter = 1e-6
        rho = lnp.sqrt(alpha_n**2 + kappa_n**2 + jitter)

        Sx = np.pi / 2 / lnp.arctan(Qx)
        Sy = np.pi / 2 / lnp.arctan(Qy)

        mux = mux_max * lnp.sin(Qx * lnp.arctan(Sx * rho))
        muy = muy_max * lnp.sin(Qy * lnp.arctan(Sy * rho))

        Fx = mux * Fz * kappa_n / rho
        Fy = -muy * Fz * alpha_n / rho

        # Fill moments with 0.0
        outputs = dict(Fx=Fx, Fy=Fy, Mx=0.0, My=0.0, Mz=0.0)
        return ModelReturn(outputs=outputs)

    @classmethod
    def get_default_params(cls) -> Dict[str, Any]:

        # parameters from Perantoni page 34
        params = {
            "Fz1": 2000,  # reference load 1
            "Fz2": 6000,  # reference load 2
            "mux1": 1.75,  # peak longitudinal friction coefficient at load 1
            "mux2": 1.4,  # peak longitudinal friction coefficient at load 2
            "kappa1": 0.11,  # slip coefficient for the friction peak at load 1
            "kappa2": 0.10,  # slip coefficient for the friction peak at load 2
            "muy1": 1.80,  # peak lateral friction coefficient at load 1
            "muy2": 1.45,  # peak lateral friction coefficient at load 2
            "alpha1": np.deg2rad(9.0),  # slip angle for the friction peak at load 1
            "alpha2": np.deg2rad(8.0),  # slip angle for the friction peak at load 2
            "Qx": 1.9,  # longitudinal shape factor
            "Qy": 1.9,  # lateral shape factor
        }

        return params
