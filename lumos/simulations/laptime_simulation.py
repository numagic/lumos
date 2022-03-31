import logging
import numpy as np
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple

from lumos.optimal_control.config import (
    BoundaryConditionConfig,
    StageVarBoundConfig,
    SimConfig,
)
from lumos.models.simple_vehicle_on_track import SimpleVehicleOnTrack
from lumos.models.tracks import RaceTrack
from lumos.optimal_control.fixed_mesh_ocp import FixedMeshOCP
from lumos.optimal_control.nlp import BaseObjective
from lumos.optimal_control.utils import create_offset_structure

logger = logging.getLogger(__name__)


def get_default_bounds() -> Dict[str, Any]:
    """Provides some convenient bound setting for laptime simulation"""
    # Variable bounds

    bounds = (
        StageVarBoundConfig("states", "time", (0, np.inf)),
        StageVarBoundConfig("states", "eta", (-np.pi / 4, np.pi / 4)),
        StageVarBoundConfig("states", "vx", (5, 100)),
        StageVarBoundConfig("states", "vy", (-10, 10)),
        StageVarBoundConfig("states", "yaw_rate", (-np.pi * 2, np.pi * 2)),
        StageVarBoundConfig("inputs", "throttle", (0, 1)),
        StageVarBoundConfig("inputs", "brake", (0, 1)),
        StageVarBoundConfig("inputs", "steer", (-1, 1)),
    )

    _corners = ("fl", "fr", "rl", "rr")
    # Limit wheel speed to (1, 300) rad/s
    # For rolling radius = 0.33, this is ~1kph to 356kph
    bounds += tuple(
        StageVarBoundConfig("states", "wheel_speed_" + c, (0.1, 300)) for c in _corners
    )

    # Limit the slip
    bounds += tuple(
        StageVarBoundConfig("con_outputs", "slip_ratio_" + c, (-0.05, 0.05))
        for c in _corners
    )
    bounds += tuple(
        StageVarBoundConfig(
            "con_outputs", "slip_angle_" + c, (-np.deg2rad(5), np.deg2rad(5))
        )
        for c in _corners
    )

    return bounds


def get_default_boundary_conditions(
    is_cyclic: bool = True,
) -> Tuple[Tuple[int, str, str, float]]:
    """Provides some convenient boundary conditions for laptime simulation"""

    if is_cyclic:
        bc = (BoundaryConditionConfig(0, "states", "time", 0.0),)
    else:
        bc = (
            BoundaryConditionConfig(0, "states", "time", 0.0),
            BoundaryConditionConfig(0, "states", "n", 0.0),
            BoundaryConditionConfig(0, "states", "eta", 0.0),
            BoundaryConditionConfig(0, "states", "vx", 50.0),
            BoundaryConditionConfig(0, "states", "vy", 0.0),
            BoundaryConditionConfig(0, "states", "yaw_rate", 0.0),
        )
    return bc


@dataclass
class LTCConfig(SimConfig):
    track: str = None  # Have to give it a default to make it possible to inherit

    # Overwrite the default factory to those specific to LTC
    # FIXME: default_factory only takes zero argument functions. So here we could end up
    # with a config that has is_cycli==False, but with the default for is_cyclic==True
    boundary_conditions: List[Tuple[int, str, str, float]] = field(
        default_factory=get_default_boundary_conditions
    )
    bounds: Dict[str, Dict[str, Tuple[float]]] = field(
        default_factory=get_default_bounds
    )

    def __post_init__(self):
        super().__post_init__()

        # if track is not set, raise error
        if self.track is None:
            raise ValueError("A valid track file must be defined")

        # Ensure time and track heading are made non-cyclic.
        for name in ["states.time", "inputs.track_heading"]:
            if name not in self.non_cyclic_vars:
                logger.warning(
                    f"{name} must be non-cyclic, automatically adding it to the list."
                )
                self.non_cyclic_vars.append(name)


class LaptimeSimulation(FixedMeshOCP):
    ConfigClass: type = LTCConfig

    def __init__(
        self,
        model_params: Dict[str, Any] = {},
        model_config: Dict[str, Any] = {},
        sim_config: Dict[str, Any] = None,
    ):

        self._build_track_from_file(sim_config.track)

        model = SimpleVehicleOnTrack(params=model_params, model_config=model_config,)

        super().__init__(
            model=model, sim_config=sim_config, mesh_scale=self._track.total_distance
        )

    @property
    def distance_mesh(self):
        return self._flat_normalized_mesh * self._track.total_distance

    def _build_track_from_file(self, track_file):
        """Build a track private property from a track file

        This is the method to overwrite if the user wants to create track from a
        different format.
        """
        self._track = RaceTrack.from_tum_csv(track_file)

    def set_bounds(self, bounds: Tuple[StageVarBoundConfig]):
        """Override the base class method by adding fixed varialbe bounds to track properties"""
        curvature = self._track.curvature_at(self.distance_mesh)
        heading = self._track.heading_at(self.distance_mesh)
        left_distance = self._track.left_distance_at(self.distance_mesh)
        right_distance = self._track.right_distance_at(self.distance_mesh)

        track_bounds = (
            StageVarBoundConfig("inputs", "track_curvature", (curvature, curvature)),
            StageVarBoundConfig("inputs", "track_heading", (heading, heading)),
            StageVarBoundConfig("states", "n", (-right_distance, left_distance)),
        )

        super().set_bounds(bounds + track_bounds)

    def _build_objective(self):
        # Common objective regardless of the problem
        time_objective = BaseObjective(
            objective=lambda x: self._time_objective(x),
            gradient=lambda x: self._time_gradient(x),
            hessian=lambda x: np.array([]),
            hessian_structure=(np.array([]), np.array([])),
        )
        self.add_objective("time", time_objective)

        inputs_penalty_objective = BaseObjective(
            objective=lambda x: self._inputs_penalty(x),
            gradient=lambda x: self._inputs_penalty_grad(x),
            hessian=self._inputs_penalty_hessian,
            hessian_structure=self._inputs_penalty_hessian_structure(),
        )

        self.add_objective("inputs_penalty", inputs_penalty_objective)

    def _expand_weights(self, weights: Dict[str, float]):
        vec = np.zeros(self.model.num_inputs)
        for n, w in weights.items():
            vec[self.dec_var_operator.get_var_index_in_group("inputs", n)] = w

        # make it a matrix
        return np.tile(vec, (self.num_stages, 1))

    # FIXME:
    # 1) this is pretty vehicle model specific, move to subclass (or at least move weights)
    # 2) make this weights a config, so don't need to rely on default inputs on functions!
    def _inputs_penalty(self, x, weights: Dict[str, float] = {"steer": 1.0}):

        weight_matrix = self._expand_weights(weights)

        structured_vars = self.dec_var_operator.unflatten_var(x)
        return (structured_vars.inputs ** 2 * weight_matrix).sum() / self.num_stages

    def _inputs_penalty_grad(self, x, weights: Dict[str, float] = {"steer": 1.0}):
        weight_matrix = self._expand_weights(weights)
        structured_vars = self.dec_var_operator.unflatten_var(x)
        inputs_grad = 2.0 * (structured_vars.inputs * weight_matrix) / self.num_stages

        structured_grads = {g: v * 0 for g, v in structured_vars._asdict().items()}
        structured_grads["inputs"] = inputs_grad

        return self.dec_var_operator.flatten_var(**structured_grads)

    def _inputs_penalty_hessian(self, x, weights: Dict[str, float] = {"steer": 1.0}):
        weight_matrix = self._expand_weights(weights)
        inputs_hess = 2.0 * weight_matrix / self.num_stages

        return np.ravel(inputs_hess)

    def _inputs_penalty_hessian_structure(self):
        base_rows = base_cols = self.dec_var_operator.get_group_indices_at_stage(
            "inputs", stage=0
        )

        rows, cols = create_offset_structure(
            base_rows,
            base_cols,
            row_offset=self.num_var_stage,
            col_offset=self.num_var_stage,
            num_blocks=self.num_stages,
        )

        return np.ravel(rows), np.ravel(cols)

    def get_init_guess(self):
        vx = 50

        dt = np.diff(self.distance_mesh) / vx
        time = np.cumsum(np.insert(dt, 0, 0.0))
        omega_no_slip = vx / 0.33
        const_states = {
            "time": 0,
            "n": 0,
            "eta": 0,
            "vx": vx,
            "vy": 0,
            "yaw_rate": 0,
            "wheel_speed_fl": omega_no_slip,
            "wheel_speed_fr": omega_no_slip,
            "wheel_speed_rl": omega_no_slip,
            "wheel_speed_rr": omega_no_slip,
        }

        # FIXME: from make_vector, a lnp.ndarray will come out, which makes the inplace
        # replacement of time error out
        states_vec = np.array(self.model.make_vector(group="states", **const_states))
        states = np.tile(states_vec, (self.num_stages, 1))

        # replace states vec time with estimated time
        time_idx = self.dec_var_operator.get_var_index_in_group(
            group="states", name="time"
        )
        states[:, time_idx] = time

        const_inputs = {
            "throttle": 0.0,
            "brake": 0.0,
            "steer": 0.0,
            "ax": 0.0,
            "ay": 0.0,
            "track_curvature": 0.0,
            "track_heading": 0.0,
        }
        inputs_vec = self.model.make_vector(group="inputs", **const_inputs)
        inputs = np.tile(inputs_vec, (self.num_stages, 1))
        # Use real curvature and heading
        inputs[
            :, self.model.get_var_index("inputs", "track_curvature")
        ] = self._track.curvature_at(self.distance_mesh)
        inputs[
            :, self.model.get_var_index("inputs", "track_heading")
        ] = self._track.heading_at(self.distance_mesh)

        model_return = self.model.batched_forward(
            states, inputs, self.distance_mesh, self._params
        )

        return np.array(
            self.dec_var_operator.flatten_var(
                states=states,
                inputs=inputs,
                states_dot=model_return.states_dot,
                con_outputs=model_return.con_outputs,
            )
        )