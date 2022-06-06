from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple

import numpy as np

from lumos.optimal_control.config import (
    BoundConfig,
    BoundaryConditionConfig,
    BoundConfig,
    SimConfig,
)
from lumos.models.drone_model import DroneModel
from lumos.optimal_control.scaled_mesh_ocp import ScaledMeshOCP


def get_default_boundary_conditions():
    return (
        BoundaryConditionConfig(0, "states", "x", 0.0),
        BoundaryConditionConfig(0, "states", "x_dot", 0.0),
        BoundaryConditionConfig(0, "states", "z", 0.0),
        BoundaryConditionConfig(0, "states", "z_dot", 0.0),
        BoundaryConditionConfig(0, "states", "theta", 0.0),
        BoundaryConditionConfig(-1, "states", "x", 0.0),
        BoundaryConditionConfig(-1, "states", "x_dot", 0.0),
        BoundaryConditionConfig(-1, "states", "z", 5.0),
        BoundaryConditionConfig(-1, "states", "z_dot", 0.0),
        BoundaryConditionConfig(-1, "states", "theta", 2 * np.pi),
    )


def get_default_bounds():
    return (
        BoundConfig(group="states", name="x", values=(-50, 50)),
        BoundConfig(group="states", name="x_dot", values=(-50, 50)),
        BoundConfig(group="states", name="z", values=(-50, 50)),
        BoundConfig(group="states", name="z_dot", values=(-50, 50)),
        BoundConfig(group="states", name="theta", values=(-10 * np.pi, 10 * np.pi)),
        BoundConfig(group="inputs", name="f", values=(1, 20)),
        BoundConfig(group="inputs", name="omega", values=(-10, 10)),
        BoundConfig(group="global", name="mesh_scale", values=(0.1, 50)),
    )


@dataclass
class DroneSimulationConfig(SimConfig):
    boundary_conditions: Tuple[BoundaryConditionConfig] = field(
        default_factory=get_default_boundary_conditions
    )
    bounds: Tuple[BoundConfig] = field(default_factory=get_default_bounds)
    con_output_names: Tuple[str] = ("sin_theta",)


class DroneSimulation(ScaledMeshOCP):
    ConfigClass: type = DroneSimulationConfig

    def __init__(
        self,
        model_params: Dict[str, Any] = {},
        model_config: Dict[str, Any] = {},
        sim_config: Dict[str, Any] = None,
    ):

        model = DroneModel(model_config=model_config, params=model_params,)
        super().__init__(
            model=model, sim_config=sim_config,
        )

    def get_init_guess(self) -> np.ndarray:
        t_guess = 1.0

        inputs = np.zeros((self.num_stages, self.model.num_inputs)) + np.array(
            [10.0, 0]
        )

        states = (
            np.tile(self.model.make_const_vector(group="states"), (self.num_stages, 1),)
            + 0.1
        )
        model_return = self.model.batched_forward(
            states, inputs, self.get_mesh_from_scale(t_guess), self._params
        )

        return self.dec_var_operator.flatten_var(
            states=states,
            inputs=inputs,
            states_dot=model_return.states_dot,
            con_outputs=model_return.con_outputs,
            mesh_scale=t_guess,
        )

    def get_total_time(self, x: np.array) -> float:
        return self._time_objective(x)
