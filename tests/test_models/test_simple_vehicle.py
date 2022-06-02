import logging
import unittest

import numpy as np

from lumos.models.test_utils import BaseStateSpaceModelTest, use_backends
from lumos.models.vehicles.simple_vehicle import SimpleVehicle


class TestSimpleVehicle(BaseStateSpaceModelTest, unittest.TestCase):
    ModelClass: type = SimpleVehicle

    def _get_initial_states(self, vx=40.0):
        vy = 0.0
        yaw_rate = 0.0
        no_slip_omega = vx / self.model._params["rolling_radius"]

        return dict(
            vx=vx,
            vy=vy,
            yaw_rate=yaw_rate,
            wheel_speed_fl=no_slip_omega,
            wheel_speed_fr=no_slip_omega,
            wheel_speed_rl=no_slip_omega,
            wheel_speed_rr=no_slip_omega,
        )

    # TODO: there seems to be some common patterns which we might be able to abstract
    # (but maybe it's also not worth it)
    # 1) run model at a given point
    # 2) assert something
    # 3) solve IVP with a fixed input
    # 4) assert some other stuff

    # NOTE: as the model is implicit now, we set the algebraic variables ax and ay to 0,
    # which should just remove the load transfer effect

    def test_accel_straight(self):
        init_states = self._get_initial_states()
        inputs = dict(throttle=0.6, brake=0, steer=0, ax=0, ay=0)

        model_return = self.model.forward(init_states, inputs)

        # Rear wheel should accelerate
        self.assertGreater(model_return.states_dot["wheel_speed_rl_dot"], 0)
        self.assertGreater(model_return.states_dot["wheel_speed_rr_dot"], 0)

        # After a few timesteps, the vehicle should be faster and still driving straight
        num_steps = 21
        time_step = 0.05

        # Careful, numpy arrays are mutable!
        states, outputs = self._forward_euler(init_states, inputs, time_step, num_steps)

        # Speed should have increased
        # TODO: should we put a threshold on 'sufficient increase'?
        self.assertGreater(states["vx"], init_states["vx"])

        # lateral speed and yaw rate should stay at 0
        self.assertAlmostEqual(states["vy"], 0)
        self.assertAlmostEqual(states["yaw_rate"], 0)

    def test_brake_straight(self):
        init_states = self._get_initial_states()
        inputs = dict(throttle=0.0, brake=0.1, steer=0, ax=0, ay=0)

        model_return = self.model.forward(init_states, inputs)

        # All wheels should decelerate
        for c in ("fl", "fr", "rl", "rr"):
            self.assertLess(model_return.states_dot[f"wheel_speed_{c}_dot"], 0)

        # After a few timesteps, the vehicle should be slower and still driving straight
        num_steps = 21
        time_step = 0.05

        states, outputs = self._forward_euler(init_states, inputs, time_step, num_steps)

        # Speed should have increased
        # TODO: should we put a threshold on 'sufficient increase'?
        self.assertLess(states["vx"], init_states["vx"])

        # lateral speed and yaw rate should stay at 0
        self.assertAlmostEqual(states["vy"], 0)
        self.assertAlmostEqual(states["yaw_rate"], 0)

    def test_turn_left(self):
        init_states = self._get_initial_states()
        inputs = dict(throttle=0.0, brake=0, steer=0.2, ax=0, ay=0)

        model_return = self.model.forward(init_states, inputs)

        # should directly get +ve lateral acceleration, +ve yaw acceleration and derivative of vy
        self.assertGreater(model_return.states_dot["vy_dot"], 0)
        self.assertGreater(model_return.states_dot["yaw_rate_dot"], 0)
        self.assertGreater(model_return.outputs["ay"], 0)

        # After a few timesteps:
        # The speed should decelerate due to cornering resistance
        # the vehicle should have a +ve yaw rate
        # The vehicle should have -ve vy (excpet for very low speed, the vehicle slips
        # to the inside of the turn because tire slip is heavily influenced by yaw rate)
        num_steps = 21
        time_step = 0.05

        states, outputs = self._forward_euler(init_states, inputs, time_step, num_steps)

        self.assertLess(states["vx"], init_states["vx"])
        self.assertLess(states["vy"], 0)
        self.assertGreater(states["yaw_rate"], 0)

        # TODO: we could also check that the vehicle gets into kind of a steady-state turn

    def test_turn_right(self):
        init_states = self._get_initial_states()
        inputs = dict(throttle=0.0, brake=0, steer=-0.2, ax=0, ay=0)

        model_return = self.model.forward(init_states, inputs)

        # should directly get +ve lateral acceleration, +ve yaw acceleration and derivative of vy
        self.assertLess(model_return.states_dot["vy_dot"], 0)
        self.assertLess(model_return.states_dot["yaw_rate_dot"], 0)
        self.assertLess(model_return.outputs["ay"], 0)

        num_steps = 21
        time_step = 0.05

        states, outputs = self._forward_euler(init_states, inputs, time_step, num_steps)

        # All the other assertions change sign compared to left turn, except for this one
        self.assertLess(states["vx"], init_states["vx"])
        self.assertGreater(states["vy"], 0)
        self.assertLess(states["yaw_rate"], 0)

    def test_delta_torque(self):
        """When there is a delta speed
        There is a delta torque of the opposite sign.
        """

        states = self._get_initial_states()
        wheel_speed_rr = states["wheel_speed_rr"]

        for delta_speed in [-1.0, 1.0]:
            wheel_speed_rl = wheel_speed_rr + delta_speed

            states["wheel_speed_rl"] = wheel_speed_rl

            inputs = self.model.make_dict(
                "inputs", throttle=0.3, brake=0, steer=0.0, ax=0, ay=0
            )

            model_return = self.model.forward(states, inputs)
            delta_torque = (
                model_return.outputs["drive_torque_rl"]
                - model_return.outputs["drive_torque_rr"]
            )

            # delta speed and torque should be opposite signs
            self.assertLess(delta_speed * delta_torque, 0.0)
