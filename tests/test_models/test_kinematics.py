import logging
import unittest

import numpy as np

from lumos.models.kinematics import TrackPosition2D
from lumos.models.test_utils import BaseStateSpaceModelTest

logger = logging.getLogger(__name__)


class TestTrackPosition2D(BaseStateSpaceModelTest, unittest.TestCase):
    ModelClass: type = TrackPosition2D

    def _build_track_and_drive(
        self,
        curvature: float,
        start_heading: float,
        speed: float,
        yaw_rate: float = 0.0,
        distance_step: float = 1.0,
        num_steps: int = 20,
    ):

        init_states = self.model.make_dict(group="states", n=0.0, time=0.0, eta=0.0)
        states = init_states
        for step in range(num_steps):

            track_heading = start_heading + step * distance_step * curvature
            inputs = self.model.make_dict(
                group="inputs",
                vx=speed,
                vy=0.0,
                yaw_rate=yaw_rate,
                track_curvature=curvature,
                track_heading=track_heading,
            )
            model_return = self.model.forward(states=states, inputs=inputs)

            for k in states:
                states[k] += model_return.states_dot[k] * distance_step

        # Call the model again on the final states to ensure the outputs and states are
        # sync'd
        inputs = self.model.make_dict(
            group="inputs",
            vx=speed,
            vy=0.0,
            yaw_rate=yaw_rate,
            track_curvature=curvature,
            track_heading=start_heading + num_steps * distance_step * curvature,
        )

        model_return = self.model.forward(states=states, inputs=inputs)

        return states, model_return.outputs

    def test_drive_straight_on_straight_track(self):
        """WHEN speed is in x-direction on a straightline track
        THEN distance across should stay at zero
        """

        speed = 5.0
        num_steps = 20
        distance_step = 0.1
        final_states, final_outputs = self._build_track_and_drive(
            curvature=0.0,
            start_heading=0.0,
            speed=speed,
            distance_step=distance_step,
            num_steps=num_steps,
        )

        # 0-distance to centerline
        self.assertAlmostEqual(final_states["n"], 0)
        # distance travelled is correct
        self.assertAlmostEqual(final_states["time"], num_steps * distance_step / speed)

    def test_drive_curve_on_straight_track(self):
        """WHEN speed is in x-direction on a straightline track
            AND yaw rate is +ve
        THEN distance across should be positive (deviate to left)
        THEN yaw angle should be consistent
        """

        # Sign convention
        # curvature +ve to the left (along distance)
        # distance_across +ve to the left of centerline
        # vehicle yaw +ve to the left as seen by the driver
        speed = 5.0
        yaw_rate = np.deg2rad(10)
        num_steps = 20
        distance_step = 0.1
        final_states, final_outputs = self._build_track_and_drive(
            curvature=0.0,
            start_heading=0.0,
            speed=speed,
            yaw_rate=yaw_rate,
            distance_step=distance_step,
            num_steps=num_steps,
        )
        # centerline distance greater than 0
        # TODO: assert greater than 0 isn't that of a great test... Can we be more precise?)
        self.assertGreater(final_states["n"], 0)

        # time spent would be larger than if driving on straightl line
        self.assertGreater(final_states["time"], num_steps * distance_step / speed)

        # assert heading is correct
        self.assertAlmostEqual(
            final_outputs["yaw_angle"],
            num_steps * distance_step / speed * yaw_rate,
            places=3,
        )

    def test_drive_curve_on_curve_track(self):
        """WHEN speed is in x-direction on a curved track
            AND yaw rate is +ve
            AND yaw rate and speed matches track curvature
        THEN should follow centerline
        """

        # Sign convention
        # curvature +ve to the left (along distance)
        # distance_across +ve to the left of centerline
        # vehicle yaw +ve to the left as seen by the driver
        speed = 5.0
        yaw_rate = np.deg2rad(10)
        curvature = yaw_rate / speed
        num_steps = 20
        distance_step = 0.1
        final_states, final_outputs = self._build_track_and_drive(
            curvature=curvature,
            start_heading=0.0,
            speed=speed,
            yaw_rate=yaw_rate,
            distance_step=distance_step,
            num_steps=num_steps,
        )

        # We should stay on centerline
        self.assertAlmostEqual(final_states["n"], 0)

        # time spent would be the same as driving on straightl line
        self.assertAlmostEqual(final_states["time"], num_steps * distance_step / speed)

        # assert heading should be the same as track heading
        self.assertAlmostEqual(final_states["eta"], 0)


if __name__ == "__name__":
    unittest.main()
