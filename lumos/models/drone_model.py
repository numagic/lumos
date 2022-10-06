import logging

from typing import Any, Dict

import lumos.numpy as lnp
from lumos.models.base import state_space_io, StateSpaceModel, StateSpaceModelReturn

logger = logging.getLogger(__name__)


@state_space_io(
    states=("x", "x_dot", "z", "z_dot", "theta"),
    inputs=("f", "omega"),
    outputs=("sin_theta", "f_omega"),
)
class DroneModel(StateSpaceModel):
    def __init__(
        self, model_config: Dict[str, Any] = {}, params: Dict[str, Any] = {},
    ):
        super().__init__(model_config=model_config, params=params)

    def forward(
        self,
        states: Dict[str, float],
        inputs: Dict[str, float],
        mesh: float = 0.0,  # time invariant model
    ) -> StateSpaceModelReturn:
        params = self._params
        theta = states["theta"]
        x_dot_dot = inputs["f"] * lnp.sin(theta)
        z_dot_dot = inputs["f"] * lnp.cos(theta) - params["gravity"]

        # Assemble result
        states_dot = self.make_dict(
            "states_dot",
            x=states["x_dot"],
            x_dot=x_dot_dot,
            z=states["z_dot"],
            z_dot=z_dot_dot,
            theta=inputs["omega"],
        )

        outputs = self.make_dict(
            "outputs", sin_theta=lnp.sin(theta), f_omega=inputs["omega"] * inputs["f"],
        )

        return StateSpaceModelReturn(states_dot=states_dot, outputs=outputs,)

    @classmethod
    def get_default_params(self) -> Dict[str, Any]:
        return {"gravity": 9.81}
