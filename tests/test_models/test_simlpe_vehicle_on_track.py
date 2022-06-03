from mimetypes import init
import unittest

import numpy as np

from lumos.models.test_utils import BaseStateSpaceModelTest
from lumos.models.simple_vehicle_on_track import SimpleVehicleOnTrack


class TestSimpleVehicleOnTrack(BaseStateSpaceModelTest, unittest.TestCase):
    ModelClass = SimpleVehicleOnTrack

    def _get_initial_states(self, vx=40.0):
        vy = 0.0
        yaw_rate = 0.0
        # FIXME: this is really bad. How do we get the rolling radius estimate?
        no_slip_omega = vx / 0.33

        # HACK: since we now have hierarchical name: vehicle.vx, the kwargs way of
        # construction no longer works as vehicle.vx is not a legal keyword!
        return {
            "kinematics.time": 0,
            "kinematics.n": 0,
            "kinematics.eta": 0,
            "vehicle.vx": vx,
            "vehicle.vy": vy,
            "vehicle.yaw_rate": yaw_rate,
            "vehicle.wheel_speed_fl": no_slip_omega,
            "vehicle.wheel_speed_fr": no_slip_omega,
            "vehicle.wheel_speed_rl": no_slip_omega,
            "vehicle.wheel_speed_rr": no_slip_omega,
        }

    def test_turn_left(self):
        init_states = self._get_initial_states()
        inputs = self.model.make_dict(
            group="inputs",
            throttle=0.0,
            brake=0,
            ax=0.0,
            ay=0.0,
            steer=np.deg2rad(3.0),
            track_curvature=0.0,
            track_heading=0.0,
        )

        model_return = self.model.forward(init_states, inputs, mesh=0.0)

        # should directly get +ve lateral acceleration, +ve yaw acceleration and derivative of vy
        self.assertGreater(model_return.states_dot["vehicle.vy"], 0)
        self.assertGreater(model_return.states_dot["vehicle.yaw_rate"], 0)
        self.assertGreater(model_return.outputs["vehicle.ay"], 0)

        # After a few timesteps:
        # The speed should decelerate due to cornering resistance
        # the vehicle should have a +ve yaw rate
        # The vehicle should have -ve vy (excpet for very low speed, the vehicle slips
        # to the inside of the turn because tire slip is heavily influenced by yaw rate)
        num_steps = 21
        dist_step = 1.0

        states, outputs = self._forward_euler(init_states, inputs, dist_step, num_steps)

        self.assertLess(states["vehicle.vx"], init_states["vehicle.vx"])
        self.assertLess(states["vehicle.vy"], 0)
        self.assertGreater(states["vehicle.yaw_rate"], 0)

        # Assert position states
        self.assertGreater(
            outputs["kinematics.yaw_angle"],
            0,
            msg="Yaw angle should be positive for turning left",
        )

        self.assertGreater(
            states["kinematics.n"],
            0,
            msg="Distance across should be positive for turning left on straightline track",
        )

        self.assertGreater(
            states["kinematics.time"],
            0,
            msg="Time used should be positive for turning left on straightline track",
        )

        self.assertLess(
            dist_step * num_steps,
            init_states["vehicle.vx"] * dist_step * num_steps,
            msg="Distance travelled should be less than going straight from the start",
        )
