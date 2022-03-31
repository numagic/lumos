import logging
from typing import Any, Dict

import lumos.numpy as lnp
from lumos.models.base import state_space_io, StateSpaceModel, StateSpaceModelReturn

logger = logging.getLogger(__name__)


@state_space_io(
    states=("time", "n", "eta"),
    inputs=("vx", "vy", "yaw_rate", "track_curvature", "track_heading"),
    outputs=("yaw_angle", "curvature"),
)
class TrackPosition2D(StateSpaceModel):
    """2D kinematics Model with velocities and yaw rate as yaw angle as inputs

    Sign convention:
    - road: curvature: +ve for LHS turn, rotation +ve anti-clockwise. Distance across is
    +ve if the vehicle is to the left of the centerline.
    - vehicle body coordinate: x forward, y to the left, z up
    """

    def __init__(
        self, params: Dict[str, Any] = {}, model_config: Dict[str, Any] = None,
    ):
        super().__init__(model_config=model_config, params=params)

    def forward(
        self, states: lnp.ndarray, inputs: lnp.ndarray, mesh: float = 0.0,
    ) -> StateSpaceModelReturn:
        """
        Sign convention:
        x-y in vehicle coordiante:
            x forward
            y to the left of the vehicle as seen by the driver
        """

        n = self.get_state(states, "n")
        eta = self.get_state(states, "eta")
        vx = self.get_input(inputs, "vx")
        vy = self.get_input(inputs, "vy")
        yaw_rate = self.get_input(inputs, "yaw_rate")

        curvature = self.get_input(inputs, "track_curvature")
        track_heading = self.get_input(inputs, "track_heading")
        yaw_angle = self.get_state(states, "eta") + track_heading

        ds_dt = (vx * lnp.cos(eta) - vy * lnp.sin(eta)) / (1 - n * curvature)
        dn_dt = vx * lnp.sin(eta) + vy * lnp.cos(eta)
        deta_dt = yaw_rate - curvature * ds_dt

        # Pure kinematics related calculation. This is where vehicle models will be
        # executed in the future
        states_dot = self.make_vector(
            group="states", time=1 / ds_dt, n=dn_dt / ds_dt, eta=deta_dt / ds_dt,
        )
        outputs = self.make_vector(
            group="outputs", yaw_angle=yaw_angle, curvature=curvature
        )
        return self.make_state_space_model_return(
            states_dot=states_dot, outputs=outputs
        )

    @classmethod
    def get_default_params(self) -> Dict[str, Any]:
        return {}
