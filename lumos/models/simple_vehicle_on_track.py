from typing import Any, Dict, Optional

import lumos.numpy as lnp
from lumos.models.base import StateSpaceModel, state_space_io
from lumos.models.kinematics import TrackPosition2D
from lumos.models.vehicles.simple_vehicle import SimpleVehicle


# Combine the signals to create the names. TODO: can we make it more automatic?
@state_space_io(
    states=TrackPosition2D.get_direct_group_names("states")
    + SimpleVehicle.get_direct_group_names("states"),
    inputs=SimpleVehicle.get_direct_group_names("inputs")
    + ("track_curvature", "track_heading"),
    con_outputs=(
        "vehicle.slip_ratio_fl",
        "vehicle.slip_ratio_fr",
        "vehicle.slip_ratio_rl",
        "vehicle.slip_ratio_rr",
        "vehicle.slip_angle_fl",
        "vehicle.slip_angle_fr",
        "vehicle.slip_angle_rl",
        "vehicle.slip_angle_rr",
    ),
    residuals=TrackPosition2D.get_direct_group_names("residuals")
    + SimpleVehicle.get_direct_group_names("residuals"),
)
class SimpleVehicleOnTrack(StateSpaceModel):
    _submodel_names = ("vehicle", "kinematics")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def get_default_submodel_config(self):

        return {
            "vehicle": "SimpleVehicle",
            "kinematics": "TrackPosition2D",
        }

    def forward(self, states: lnp.ndarray, inputs: lnp.ndarray, mesh: float):

        # Pick out the vehicle inputs
        vehicle_inputs = {
            k: inputs[k] for k in self.get_submodel("vehicle").get_group_names("inputs")
        }

        # Pick out vehicle states
        vehicle_states = {
            k: states[k] for k in self.get_submodel("vehicle").get_group_names("states")
        }

        # Pick out vehicle params. NOT DONE! NOT EASY!
        vehicle_return = self.get_submodel("vehicle").forward(
            states=vehicle_states, inputs=vehicle_inputs
        )

        # Call Kinematics model
        # Pick out states
        kinematic_states = {
            k: states[k]
            for k in self.get_submodel("kinematics").get_group_names("states")
        }

        # pick out inputs
        # NOTE: this step is very custom, because the inputs come from vehicle model
        # outputs
        inputs_from_vehicle = {k: vehicle_states[k] for k in ("vx", "vy", "yaw_rate")}

        track_inputs = {k: inputs[k] for k in ["track_curvature", "track_heading"]}

        kinematic_inputs = dict(**track_inputs, **inputs_from_vehicle)

        # Pick out vehicle params. NOT DONE! NOT EASY!
        kinematics_return = self.get_submodel("kinematics").forward(
            states=kinematic_states, inputs=kinematic_inputs, mesh=mesh,
        )

        # Convert to distance domain derivatives
        dt_ds = kinematics_return.states_dot["time"]
        states_dot = {
            **kinematics_return.states_dot,
            **{k: v * dt_ds for k, v in vehicle_return.states_dot.items()},
        }

        # Assemble final outputs
        outputs = self.combine_submodel_outputs(
            vehicle=vehicle_return.outputs, kinematics=kinematics_return.outputs
        )

        residuals = vehicle_return.residuals

        return self.make_state_space_model_return(
            states_dot=states_dot, outputs=outputs, residuals=residuals,
        )
