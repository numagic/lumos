import unittest
from copy import deepcopy

import numpy as np

from lumos.models.base import StateSpaceModel, state_space_io
from lumos.models.drone_model import DroneModel


@state_space_io(
    states=("state0", "state1"),
    inputs=("input0",),
    outputs=("output0", "output1"),
    con_outputs=("output2",),
)
class ModelWithWrongConOutputs(StateSpaceModel):
    def forward(self, states, inputs, mesh=0.0):
        states_dot = self.make_vector(group="states", state0=0.0, state1=0.1)
        outputs = self.make_vector(group="outputs", output0=0.0, output1=1.0)

        return self.make_state_space_model_return(
            states_dot=states_dot, outputs=outputs,
        )


@state_space_io(
    states=("state0", "state1"),
    inputs=("input0",),
    outputs=("output0", "output1"),
    con_outputs=("output0",),
)
class ModelWithCorrectConOutputs(ModelWithWrongConOutputs):
    pass


@state_space_io(
    states=("state0", "state1"), inputs=("input0",), outputs=("output0", "output1"),
)
class ModelWithNoConOutputs(ModelWithCorrectConOutputs):
    pass


@state_space_io(
    states=("state0", "state1"), inputs=("input0",),
)
class ModelWithNoOutputs(StateSpaceModel):
    def forward(self, states, inputs, mesh=0.0):
        states_dot = self.make_vector(group="states", state0=0.0, state1=0.1)

        return self.make_state_space_model_return(states_dot=states_dot,)


class TestStateSpaceModel(unittest.TestCase):
    """Test helper functions defined in StateSpaceModel

    TODO: currently we use a DroneModel for testing these methods. Ideally we would use
    the abstract class directly (although this requires a bit of work)

    TODO: we should also test the Model class, which is the parent of StateSpaceModel.
    """

    def setUp(self) -> None:
        """We start with a clean model every time"""
        self.model = DroneModel()

    def test_make_vector(self):
        """Test the helper function to assemble a vector automatically

        WHEN correct keys are given
        THEN vector elements should be correct

        WHEN a key is missing
        THEN Raise Value Error

        WHEN an extra key is given
        THEN still works (although gives a warning)
        THEN vector elements should be correct
        """

        groups_to_check = self.model.names._asdict()
        # Drone model has an empty set for residuals, so we don't need to test that.
        groups_to_check.pop("residuals")

        for group, names in groups_to_check.items():
            # Correct amount of names.
            var_dict = dict(zip(names, np.random.randn(len(names))))
            vec = self.model.make_vector(group=group, **var_dict)
            for idx, name in enumerate(names):
                self.assertAlmostEqual(vec[idx], var_dict[name])

            # Too many names
            too_many_names = names + ("name_that_should_not_happen",)
            var_dict = dict(zip(too_many_names, np.random.randn(len(too_many_names))))
            vec = self.model.make_vector(group=group, **var_dict)
            for idx, name in enumerate(names):
                self.assertAlmostEqual(vec[idx], var_dict[name])

            # Just missing essential names
            missing_essential_names = names[1:]
            var_dict = dict(
                zip(
                    missing_essential_names,
                    np.random.randn(len(missing_essential_names)),
                )
            )
            with self.assertRaises(ValueError) as context:
                vec = self.model.make_vector(group=group, **var_dict)

            # Missing some essential names but has extra names
            missing_essential_but_with_extra_names = missing_essential_names + (
                "name_that_should_not_happen",
            )
            var_dict = dict(
                zip(
                    missing_essential_but_with_extra_names,
                    np.random.randn(len(missing_essential_but_with_extra_names)),
                )
            )
            with self.assertRaises(ValueError) as context:
                vec = self.model.make_vector(group=group, **var_dict)

    def test_extract_con_outputs(self):
        """WHEN con_outputs not in outputs, THEN raise Value Error.
        WHEN con_outputs in outputs, THEN correct values are extracted
        """
        # When con_outputs is NOT inside outputs, raises ValueError
        with self.assertRaises(ValueError):
            model_incorrect = ModelWithWrongConOutputs()

        # When things are correct
        model_correct = ModelWithCorrectConOutputs()
        states = np.zeros(model_correct.num_states)
        inputs = np.zeros(model_correct.num_inputs)
        model_return = model_correct.forward(states, inputs)

        manually_extracted = np.array(
            [
                model_correct.get_output(model_return.outputs, n)
                for n in model_correct.get_group_names("con_outputs")
            ]
        )
        np.testing.assert_allclose(model_return.con_outputs, manually_extracted)

        # When conoutputs are empty
        model_no_cons = ModelWithNoConOutputs()
        model_return = model_no_cons.forward(states, inputs)
        self.assertEqual(len(model_return.con_outputs), 0)

    def test_model_with_no_outputs(self):
        model = ModelWithNoOutputs()
        states = np.zeros(model.num_states)
        inputs = np.zeros(model.num_inputs)
        model_return = model.forward(states, inputs)

        self.assertEqual(len(model_return.states_dot), model.num_states)
        self.assertEqual(len(model_return.outputs), 0)
        self.assertEqual(len(model_return.con_outputs), 0)
