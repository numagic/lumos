import logging
import numpy as np
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple

from lumos.optimal_control.config import (
    BoundConfig,
    BoundaryConditionConfig,
    ScaleConfig,
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
        BoundConfig("states", "time", (0, np.inf)),
        BoundConfig("states", "eta", (-np.pi / 4, np.pi / 4)),
        BoundConfig("states", "vx", (5, 100)),
        BoundConfig("states", "vy", (-10, 10)),
        BoundConfig("states", "yaw_rate", (-np.pi * 2, np.pi * 2)),
        BoundConfig("inputs", "throttle", (0, 1)),
        BoundConfig("inputs", "brake", (0, 1)),
        BoundConfig("inputs", "steer", (-1, 1)),
    )

    _corners = ("fl", "fr", "rl", "rr")
    # Limit wheel speed to (1, 300) rad/s
    # For rolling radius = 0.33, this is ~1kph to 356kph
    bounds += tuple(
        BoundConfig("states", "wheel_speed_" + c, (0.1, 300)) for c in _corners
    )

    # Limit the slip
    bounds += tuple(
        BoundConfig("con_outputs", "vehicle.slip_ratio_" + c, (-0.05, 0.05))
        for c in _corners
    )
    bounds += tuple(
        BoundConfig(
            "con_outputs", "vehicle.slip_angle_" + c, (-np.deg2rad(5), np.deg2rad(5))
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


def get_default_scales() -> Tuple[ScaleConfig]:
    scales = (
        ScaleConfig("states", "time", 10.0),
        ScaleConfig("states", "vx", 10.0),
        ScaleConfig("states", "wheel_speed_fl", 50.0),
        ScaleConfig("states", "wheel_speed_fr", 50.0),
        ScaleConfig("states", "wheel_speed_rl", 50.0),
        ScaleConfig("states", "wheel_speed_rr", 50.0),
        ScaleConfig("states_dot", "wheel_speed_fl", 50.0),
        ScaleConfig("states_dot", "wheel_speed_fr", 50.0),
        ScaleConfig("states_dot", "wheel_speed_rl", 50.0),
        ScaleConfig("states_dot", "wheel_speed_rr", 50.0),
    )
    return scales


def get_default_con_output_names() -> Tuple[str]:
    return (
        "vehicle.slip_ratio_fl",
        "vehicle.slip_ratio_fr",
        "vehicle.slip_ratio_rl",
        "vehicle.slip_ratio_rr",
        "vehicle.slip_angle_fl",
        "vehicle.slip_angle_fr",
        "vehicle.slip_angle_rl",
        "vehicle.slip_angle_rr",
    )


@dataclass
class LTCConfig(SimConfig):
    track: str = None  # Have to give it a default to make it possible to inherit

    # Overwrite the default factory to those specific to LTC
    # FIXME: default_factory only takes zero argument functions. So here we could end up
    # with a config that has is_cycli==False, but with the default for is_cyclic==True
    boundary_conditions: Tuple[
        BoundaryConditionConfig
    ] = get_default_boundary_conditions()
    bounds: Tuple[BoundConfig] = get_default_bounds()
    scales: Tuple[ScaleConfig] = get_default_scales()
    con_output_names: Tuple[str] = get_default_con_output_names()

    def __post_init__(self):
        super().__post_init__()

        # if track is not set, raise error
        if self.track is None:
            raise ValueError("A valid track file must be defined")

        # Ensure time and track heading are made non-cyclic.
        # NOTE: somehow if we make track_curvature also non_cyclic, convergence got
        # a lot worse. This is counterintuitive as one would imagine the track curvature
        # from finite difference isn't actually cyclic! (but it's close, ~1e-5 delta)
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

        # The correct mesh_scale must be given here, otherwise the solve would fail
        # This is because we use LinearConstraints for the continuity here
        # which caches the jacobian upon initialization! So the continuity constraints
        # would have been initialized with the wrong total mesh_scale if we didn't pass
        # it in during construction time!
        # This seems very dangerous
        model = SimpleVehicleOnTrack(params=model_params, model_config=model_config,)

        # Set a dummy meshscale first, and update it later when we set the track.
        # Unfortunately setting track must happen AFTER problem construction because we
        # need to add track related bounds on top of existing bounds.
        super().__init__(model=model, sim_config=sim_config, mesh_scale=1.0)
        self.set_track(sim_config.track)

    @property
    def distance_mesh(self):
        return self._flat_normalized_mesh * self._track.total_distance

    def set_track(self, track_file):
        """Set the track and update the variable bounds accordingly.

        This is the method to overwrite if the user wants to create track from a
        different format.

        We've made it possible to change track afte problem initiation mainly to save
        jit overhead for jax models. But is this really worth it? Price we pay now:
        - need to reconstruct continuity constarints
        - need to reconstruct condensed constraints -> because it also has a copy of continuity
        - need to store and reapply boundary conditions (and check for conflicts, eg
        someone setting a starting offcenter position 10m for a track that is 8m wide.)
        """

        # Create track object
        self._track = RaceTrack.from_tum_csv(track_file)

        # update mesh_scale
        self.set_mesh_scale(self._track.total_distance)

        # update variable bounds
        curvature = self._track.curvature_at(self.distance_mesh)
        heading = self._track.heading_at(self.distance_mesh)
        left_distance = self._track.left_distance_at(self.distance_mesh)
        right_distance = self._track.right_distance_at(self.distance_mesh)

        track_bounds = (
            BoundConfig("inputs", "track_curvature", (curvature, curvature)),
            BoundConfig("inputs", "track_heading", (heading, heading)),
            BoundConfig("states", "n", (-right_distance, left_distance)),
        )

        self.update_bounds(track_bounds)

    def _build_objective(self):
        # Common objective regardless of the problem
        time_objective = BaseObjective(
            num_in=self.num_dec,
            objective=lambda x: self._time_objective(x),
            gradient=lambda x: self._time_gradient(x),
            hessian=lambda x: np.array([]),
            hessian_structure=(
                np.array([], dtype=np.int32),
                np.array([], dtype=np.int32),
            ),
        )
        self.add_objective("time", time_objective)

        inputs_penalty_objective = BaseObjective(
            num_in=self.num_dec,
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
        op = self.dec_var_operator
        base_rows = base_cols = op.get_group_indices_at_stage("inputs", stage=0)

        rows, cols = create_offset_structure(
            base_rows,
            base_cols,
            row_offset=op.num_var_stage,
            col_offset=op.num_var_stage,
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

        # Produce unscaled initial guess
        return np.array(
            self.dec_var_operator.flatten_var(
                states=states,
                inputs=inputs,
                states_dot=model_return.states_dot,
                con_outputs=model_return.con_outputs,
            )
        )
