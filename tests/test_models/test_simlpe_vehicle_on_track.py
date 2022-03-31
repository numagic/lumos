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

        return self.model.make_vector(
            group="states",
            time=0,
            n=0,
            eta=0,
            vx=vx,
            vy=vy,
            yaw_rate=yaw_rate,
            wheel_speed_fl=no_slip_omega,
            wheel_speed_fr=no_slip_omega,
            wheel_speed_rl=no_slip_omega,
            wheel_speed_rr=no_slip_omega,
        )

    def test_turn_left(self):
        init_states = self._get_initial_states()
        inputs = self.model.make_vector(
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
        self.assertGreater(self.model.get_state(model_return.states_dot, "vy"), 0)
        self.assertGreater(self.model.get_state(model_return.states_dot, "yaw_rate"), 0)
        self.assertGreater(self.model.get_output(model_return.outputs, "ay"), 0)

        # After a few timesteps:
        # The speed should decelerate due to cornering resistance
        # the vehicle should have a +ve yaw rate
        # The vehicle should have -ve vy (excpet for very low speed, the vehicle slips
        # to the inside of the turn because tire slip is heavily influenced by yaw rate)
        num_steps = 21
        dist_step = 1.0

        # Careful, numpy arrays are mutable!
        states = np.copy(init_states)
        distance = 0.0
        for _ in range(num_steps):
            model_return = self.model.forward(states, inputs, mesh=distance)
            states += model_return.states_dot * dist_step
            distance += dist_step

        self.assertLess(
            self.model.get_state(states, "vx"), self.model.get_state(init_states, "vx")
        )
        self.assertLess(self.model.get_state(states, "vy"), 0)
        self.assertGreater(self.model.get_state(states, "yaw_rate"), 0)

        # Assert position states
        self.assertGreater(
            self.model.get_output(model_return.outputs, "yaw_angle"),
            0,
            msg="Yaw angle should be positive for turning left",
        )

        self.assertGreater(
            self.model.get_state(states, "n"),
            0,
            msg="Distance across should be positive for turning left on straightline track",
        )

        self.assertGreater(
            self.model.get_state(states, "time"),
            0,
            msg="Time used should be positive for turning left on straightline track",
        )

        self.assertLess(
            distance,
            self.model.get_state(init_states, "vx") * dist_step * num_steps,
            msg="Distance travelled should be less than going straight from the start",
        )
