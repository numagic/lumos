import logging
from enum import IntEnum
from functools import reduce
from operator import add
from typing import Any, Dict

import numpy as np

import lumos.numpy as lnp
from lumos.models.base import StateSpaceModel, StateSpaceModelReturn, state_space_io


logger = logging.getLogger(__name__)


class Vector3dEnum(IntEnum):
    X = 0
    Y = 1
    Z = 2


# TODO: these module level variables are not very nice...
_corners = ("fl", "fr", "rl", "rr")


def _rotate_z(theta: float) -> lnp.ndarray:
    """Helper function to create 3x3 transformation matrix.

    Transform a 3d vector from its current frame to another frame that is
    rotated around the z-axis by theta

    Note here the rotation of frame is theta, so the rotation of the vector is
    eqvauiletn to -theta
    """
    return lnp.array(
        [
            [lnp.cos(theta), lnp.sin(theta), 0],
            [-lnp.sin(theta), lnp.cos(theta), 0],
            [0, 0, 1],
        ]
    )


# See Perantoni 2014 "Optimal Contorl for a Formula One Car with Variable Parameters"


@state_space_io(
    states=(
        "vx",  # speed in vehicle x-coordinate
        "vy",  # speed in vehicle y-coordinate
        "yaw_rate",  # yaw rate
        "wheel_speed_fl",
        "wheel_speed_fr",
        "wheel_speed_rl",
        "wheel_speed_rr",
    ),
    inputs=(
        "throttle",  # normalized [0, 1]
        "brake",  # normalized [0, 1]
        "steer",  # directly front wheel steering angle
        "ax",
        "ay",
    ),
    outputs=(
        "ax",
        "ay",
        "drive_torque_rl",
        "drive_torque_rr",
        "Fx_tire_fl",
        "Fy_tire_fl",
        "Fz_tire_fl",
        "Fx_tire_fr",
        "Fy_tire_fr",
        "Fz_tire_fr",
        "Fx_tire_rl",
        "Fy_tire_rl",
        "Fz_tire_rl",
        "Fx_tire_rr",
        "Fy_tire_rr",
        "Fz_tire_rr",
        "slip_ratio_fl",
        "slip_ratio_fr",
        "slip_ratio_rl",
        "slip_ratio_rr",
        "slip_angle_fl",
        "slip_angle_fr",
        "slip_angle_rl",
        "slip_angle_rr",
        "res_ax",
        "res_ay",
    ),
    residuals=("res_ax", "res_ay"),
)
class SimpleVehicle(StateSpaceModel):
    """2D kinematics Model with acceleration limit"""

    def __init__(self, model_config={}, params={}):
        super().__init__(model_config=model_config, params=params)

    @classmethod
    def get_default_submodel_config(cls):
        return {
            "tire_fl": "MF52",
            "tire_fr": "MF52",
            "tire_rl": "MF52",
            "tire_rr": "MF52",
            "aero": "ConstAero",
        }

    def forward(
        self,
        states: Dict[str, float],
        inputs: Dict[str, float],
        mesh: float = 0.0,  # time invariant
    ) -> StateSpaceModelReturn:
        """
        Sign convention:
        x-y in vehicle coordiante:
            x forward
            y to the left of the vehicle as seen by the driver
        """
        params = self._params

        throttle = inputs["throttle"]
        brake = inputs["brake"]
        steer = inputs["steer"]
        ax_in = inputs["ax"]
        ay_in = inputs["ay"]

        vx = states["vx"]
        vy = states["vy"]
        yaw_rate = states["yaw_rate"]

        wheel_speed = {c: states[f"wheel_speed_{c}"] for c in _corners}

        max_power = params["max_power"]
        max_steer_angle = params["max_steer_angle"]
        kd = params["kd"]
        rolling_radius = params["rolling_radius"]
        max_total_brake_torque = params["max_total_brake_torque"]
        brake_balance = params["brake_balance"]
        cog_to_fa = params["cog_to_fa"]
        cog_to_ra = params["cog_to_ra"]
        cog_height = params["cog_height"]
        track_front = params["track_front"]
        track_rear = params["track_rear"]
        gravity = params["gravity"]
        vehicle_mass = params["vehicle_mass"]
        Iz = params["Iz"]
        wheel_inertia = params["wheel_inertia"]
        air_density = params["air_density"]
        mech_balance = params["mech_balance"]

        # scale steering from [-1, 1] to [-max_angle, max_angle]
        steer = steer * max_steer_angle
        # Drivetrain model: compute drive torque
        # NOTE: rear wheel drive only at the moment
        drive_power = throttle * max_power
        # kd is +ve -> delta_troque +ve when left is faster -> left torque would be smalelr
        delta_torque = -kd * (wheel_speed["rl"] - wheel_speed["rr"])
        # TODO: if left and right can have different rolling radius, then this would be different

        # NOTE: here the torque, speed and power satisfy:
        # 1) power conservation: torque_left*speed_left + torque_right + speed_right = total_power
        # 2) differentia: torque_left - torque_right = -kd*(speed_left - speed_right)
        #
        # two equations and two unknowns (the torque), so we could solve them analytically
        #
        # torque_left - delta_torque = torque_right
        # torque_left*speed_left + (torque_left - delta_torque)*speed_right = P
        # torque_left*(speed_left + speed_right) - delta_torque*speed_right = P
        # torque_left = (P + delta_torque*speed_right)/(speed_left + speed_right)
        drive_torque_rl = (drive_power + delta_torque * wheel_speed["rr"]) / (
            wheel_speed["rl"] + wheel_speed["rr"]
        )
        drive_torque_rr = drive_torque_rl - delta_torque
        drive_torque = {
            "fl": 0,
            "fr": 0,
            "rl": drive_torque_rl,
            "rr": drive_torque_rr,
        }

        # Brake Model
        total_brake_torque = max_total_brake_torque * brake
        # TODO: here we assume equal brake torque L/R
        brake_torque = {
            "fl": total_brake_torque * brake_balance * 0.5,
            "fr": total_brake_torque * brake_balance * 0.5,
            "rl": total_brake_torque * (1 - brake_balance) * 0.5,
            "rr": total_brake_torque * (1 - brake_balance) * 0.5,
        }

        # FIXME: we use some dummy inputs for speed evaluation only for now.
        aero_inputs = dict(front_ride_height=vx, rear_ride_height=vy, yaw=yaw_rate)

        # FIXME: aero sign convention
        aero_return = self.call_submodel("aero", inputs=aero_inputs)
        aero_coeff = aero_return.outputs

        Fz_total = vehicle_mass * gravity + aero_coeff["Cz"] * (
            0.5 * air_density * (vx ** 2 + vy ** 2)
        )

        # Compute tire load
        # TODO: currently we ignore
        # - load transfer -> without suspension model this would be an algebraic loop

        # ay +ve -> accelerating to left -> rhs heavier

        # lateral transfer determiend by mechnical balance
        # left turn -> +ve ay -> -ve roll moment -> -ve transfer -> add to left
        roll_moment = -ay_in * vehicle_mass * cog_height
        lateral_transfer_front = roll_moment * mech_balance / track_front
        lateral_transfer_rear = roll_moment * (1 - mech_balance) / track_rear

        # longitudinal transfer is equal left and right
        # braking -> -ve ax_in -> +ve pitch_moment -> +ve transfer --> add to front
        pitch_moment = -ax_in * vehicle_mass * cog_height
        longitudinal_transfer = pitch_moment / (cog_to_fa + cog_to_ra) / 2
        # load_transfer = {"fl"}

        weight_distribution_front = cog_to_ra / (cog_to_fa + cog_to_ra)
        wheel_load = {
            "fl": 0.5 * weight_distribution_front * Fz_total
            + lateral_transfer_front
            + longitudinal_transfer,
            "fr": 0.5 * weight_distribution_front * Fz_total
            - lateral_transfer_front
            + longitudinal_transfer,
            "rl": 0.5 * (1 - weight_distribution_front) * Fz_total
            + lateral_transfer_rear
            - longitudinal_transfer,
            "rr": 0.5 * (1 - weight_distribution_front) * Fz_total
            - lateral_transfer_rear
            - longitudinal_transfer,
        }

        # Compute contact patch velocity in tire coordinates.
        #
        # TODO: this should form 2 generic steps:
        # 1) compute point velocity on a rigid body
        # 2) transform to a different coordinate system.
        # But these steps will be obsolete once we move to a multibody representation
        # where the forward kinematics would give us the velocity of each body in its frame
        corner_positions = {
            "fl": lnp.array([cog_to_fa, track_front / 2, -cog_height]),
            "fr": lnp.array([cog_to_fa, -track_front / 2, -cog_height]),
            "rl": lnp.array([-cog_to_ra, track_rear / 2, -cog_height]),
            "rr": lnp.array([-cog_to_ra, -track_rear / 2, -cog_height]),
        }

        vehicle_vel = lnp.array([vx, vy, 0.0])
        vehicle_rotational_vel = lnp.array([0, 0, yaw_rate])
        corner_vel_in_body_coordinate = {
            c: vehicle_vel + lnp.cross(vehicle_rotational_vel, pos)
            for c, pos in corner_positions.items()
        }

        wheel_angle = {"fl": steer, "fr": steer, "rl": 0, "rr": 0}
        corner_vel_in_wheel_coordinate = {
            c: _rotate_z(wheel_angle[c]) @ vel
            for c, vel in corner_vel_in_body_coordinate.items()
        }

        # Compute tire forces
        # TODO: for code optimization, we should use vectorize/vmap here
        # Not because of parallelization, but mainlyl for reducing ops inside the code to JIT
        # to improve compile time.
        mirror_coeff = {"fl": 1.0, "fr": -1.0, "rl": 1.0, "rr": -1.0}
        tire_force_in_wheel_coordinate = {}
        slips = {}
        tire_outputs = {}
        for c, vel in corner_vel_in_wheel_coordinate.items():
            kappa = -(1 - rolling_radius * wheel_speed[c] / vx)
            # NOTE: this assumes vx > 0
            alpha = lnp.arctan(vel[Vector3dEnum.Y] / vel[Vector3dEnum.X])

            slips["slip_ratio_" + c] = kappa
            slips["slip_angle_" + c] = alpha

            inputs = dict(
                Fz=wheel_load[c],
                kappa=kappa,
                alpha=alpha * mirror_coeff[c],
                vx=vel[Vector3dEnum.X],
                gamma=0.0 * mirror_coeff[c],  # TODO: hardcoded for now
            )

            outputs = self.call_submodel("tire_" + c, inputs=inputs).outputs

            # TODO: store the outputs, but in a nicer way.
            tire_outputs[c] = outputs
            # TODO: tire moments are not taken into account yet.
            tire_force_in_wheel_coordinate[c] = lnp.array(
                [outputs["Fx"], outputs["Fy"] * mirror_coeff[c], wheel_load[c],]
            )

        # Transform tire forces to body coordinate
        tire_force_in_body_coordinate = {
            c: _rotate_z(-wheel_angle[c]) @ f
            for c, f in tire_force_in_wheel_coordinate.items()
        }

        # tire force moment on body
        tire_moment_in_body_coordinate = {
            c: lnp.cross(corner_positions[c], f)
            for c, f in tire_force_in_body_coordinate.items()
        }

        # aero force in body coordinate
        # FIXME: drag should be absolute speed
        drag = lnp.array(
            [-aero_coeff["Cx"] * (0.5 * air_density * (vx ** 2 + vy ** 2)), 0, 0]
        )

        # Sum up all the forces
        total_force_on_body = reduce(add, tire_force_in_body_coordinate.values())
        total_force_on_body += drag
        total_moment_on_body = reduce(add, tire_moment_in_body_coordinate.values())

        # TODO: compute acceleration in vehicle frame
        linear_accel = total_force_on_body / vehicle_mass
        ax = linear_accel[Vector3dEnum.X]
        ay = linear_accel[Vector3dEnum.Y]
        yaw_accel = total_moment_on_body[Vector3dEnum.Z] / Iz

        # Compute wheel acceleration
        # TODO: here we assume all wheels have the same inertia
        wheel_speed_dot = {
            c: (drive_torque[c] - brake_torque[c] - f[Vector3dEnum.X] * rolling_radius)
            / wheel_inertia
            for c, f in tire_force_in_wheel_coordinate.items()
        }

        vx_dot = ax + yaw_rate * vy
        vy_dot = ay - yaw_rate * vx

        states_dot = self.make_dict(
            "states_dot",
            vx=vx_dot,
            vy=vy_dot,
            yaw_rate=yaw_accel,
            wheel_speed_fl=wheel_speed_dot["fl"],
            wheel_speed_fr=wheel_speed_dot["fr"],
            wheel_speed_rl=wheel_speed_dot["rl"],
            wheel_speed_rr=wheel_speed_dot["rr"],
        )

        outputs = self.make_outputs_dict(
            ax=ax,
            ay=ay,
            drive_torque_rl=drive_torque_rl,
            drive_torque_rr=drive_torque_rr,
            Fx_tire_fl=tire_force_in_body_coordinate["fl"][Vector3dEnum.X],
            Fy_tire_fl=tire_force_in_body_coordinate["fl"][Vector3dEnum.Y],
            Fz_tire_fl=tire_force_in_body_coordinate["fl"][Vector3dEnum.Z],
            Fx_tire_fr=tire_force_in_body_coordinate["fr"][Vector3dEnum.X],
            Fy_tire_fr=tire_force_in_body_coordinate["fr"][Vector3dEnum.Y],
            Fz_tire_fr=tire_force_in_body_coordinate["fr"][Vector3dEnum.Z],
            Fx_tire_rl=tire_force_in_body_coordinate["rl"][Vector3dEnum.X],
            Fy_tire_rl=tire_force_in_body_coordinate["rl"][Vector3dEnum.Y],
            Fz_tire_rl=tire_force_in_body_coordinate["rl"][Vector3dEnum.Z],
            Fx_tire_rr=tire_force_in_body_coordinate["rr"][Vector3dEnum.X],
            Fy_tire_rr=tire_force_in_body_coordinate["rr"][Vector3dEnum.Y],
            Fz_tire_rr=tire_force_in_body_coordinate["rr"][Vector3dEnum.Z],
            res_ax=ax - ax_in,
            res_ay=ay - ay_in,
            **slips,
        )

        return StateSpaceModelReturn(states_dot=states_dot, outputs=outputs)

    @classmethod
    def get_default_params(self) -> Dict[str, Any]:
        # FIXME: here the parameter types are not speicfied. Could get int and float mix!
        return {
            "gravity": 9.81,  # gravitational constant [N/kg]
            "vehicle_mass": 1800.0,  # vehicle mass in [kg]
            "Iz": 1200,  # moment of inertia about z-axis in [kg m^2]
            "cog_to_fa": 1.8,  # distance from cog to front axle [m]
            "cog_to_ra": 1.8,  # distance from cog to rear axle [m]
            "cog_height": 0.3,  # cog height in [m]
            "mech_balance": 0.5,  # roll moment distribution front [-]
            "track_front": 1.46,  # track width of front in [m]
            "track_rear": 1.46,  # track width of rear in [m]
            # FIXME: at the moment the rolling radius is used both by the vehicle and
            # by the tire model. In the future, it would be most likely computed by the
            # tire model.
            "rolling_radius": 0.33,  # rolling radius in [m]
            "kd": 10.47,  # differential friction coefficient [Nm/(rad/s)]
            "air_density": 1.2,  # air density in [kg/m^3]
            "aero_balance": 1.7 / 3.6,  # aero load distribution front [-]
            # These are parameters NOT in the paper
            "max_steer_angle": np.deg2rad(10),  # maximum steer angle at the wheel.
            "max_power": 500000,  # power in watt
            "max_total_brake_torque": 16000,  # non-physical parameter, allow 5g decel without aero [Nm]
            "brake_balance": 0.6,  # brake torque distributed to the front.
            "wheel_inertia": 5,  # wheel rotational inertia [kg m^2]
            "some_array": np.ones(
                (10, 3)
            ),  # some random array to ensure code works with array param
        }
