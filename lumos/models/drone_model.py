import logging

from typing import Any, Dict

import lumos.numpy as lnp
from lumos.models.base import state_space_io, StateSpaceModel, StateSpaceModelReturn

logger = logging.getLogger(__name__)


@state_space_io(
    states=("x", "x_dot", "z", "z_dot", "theta"),
    inputs=("f", "omega"),
    outputs=("sin_theta", "f_omega"),
    con_outputs=("sin_theta",),
)
class DroneModel(StateSpaceModel):
    def __init__(
        self, model_config: Dict[str, Any] = {}, params: Dict[str, Any] = {},
    ):
        super().__init__(model_config=model_config, params=params)

    def forward(
        self,
        states: lnp.ndarray,
        inputs: lnp.ndarray,
        mesh: float = 0.0,  # time invariant model
    ) -> StateSpaceModelReturn:
        params = self._params
        theta = self.get_state(states, "theta")
        x_dot_dot = self.get_input(inputs, "f") * lnp.sin(theta)
        z_dot_dot = self.get_input(inputs, "f") * lnp.cos(theta) - params["gravity"]

        # Assemble result
        states_dot = self.make_vector(
            group="states",
            x=self.get_state(states, "x_dot"),
            x_dot=x_dot_dot,
            z=self.get_state(states, "z_dot"),
            z_dot=z_dot_dot,
            theta=self.get_input(inputs, "omega"),
        )

        outputs = self.make_vector(
            group="outputs",
            sin_theta=lnp.sin(theta),
            f_omega=self.get_input(inputs, "omega") * self.get_input(inputs, "f"),
        )

        return self.make_state_space_model_return(
            states_dot=states_dot, outputs=outputs,
        )

    @classmethod
    def get_default_params(self) -> Dict[str, Any]:
        return {"gravity": 9.81}
