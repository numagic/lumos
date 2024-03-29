import unittest

import numpy as np

from lumos.models.composition import ModelMaker
from lumos.models.base import (
    StateSpaceModel,
    state_space_io,
    Model,
    model_io,
    ModelReturn,
    StateSpaceModelReturn,
)
from lumos.models.drone_model import DroneModel


@state_space_io(
    states=("state0", "state1"),
    inputs=("input0",),
    outputs=("output0", "output1"),
    con_outputs=("output2",),
)
class ModelWithWrongConOutputs(StateSpaceModel):
    def forward(self, states, inputs, mesh=0.0):
        states_dot = self.make_dict(group="states", state0=0.0, state1=0.1)
        outputs = self.make_dict(group="outputs", output0=0.0, output1=1.0)

        return StateSpaceModelReturn(states_dot=states_dot, outputs=outputs,)


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
        states_dot = self.make_dict(group="states", state0=0.0, state1=0.1)

        return StateSpaceModelReturn(states_dot=states_dot,)


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
        # Drone model has an empty set for residuals and con_outputs, so we don't need
        # to test that.
        groups_to_check.pop("residuals")
        groups_to_check.pop("con_outputs")

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
            with self.assertRaises(KeyError) as context:
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
            with self.assertRaises(KeyError) as context:
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

        for k, v in model_return.con_outputs.items():
            self.assertAlmostEqual(v, model_return.outputs[k])

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


ENGINE_TORQUE = 1.0
ENGINE_POWER = 2.0
EMOTOR_TORQUE = 3.0
EMOTOR_POWER = 4.0
TOTAL_POWER = 5.0
TOTAL_TORQUE = 6.0
AX = 7.0
AY = 8.0


@state_space_io(
    states=("vx", "vy"), inputs=("throttle", "steer", "brake"), outputs=("ax", "ay"),
)
class VehicleForTest(StateSpaceModel):
    # attributes used for introducing error and test exception
    forget_submodel_call: bool = False
    extra_submodel_call: bool = False

    @classmethod
    def get_default_submodel_config(cls):
        return {"powertrain": "HybridPowertrain", "tire": "MF72"}

    def forward(self, states, inputs, mesh):
        vx = states["vx"]
        throttle = inputs["throttle"]

        # Call powertrain model
        powertrain_return = self.call_submodel(
            "powertrain",
            states={"engine_speed": vx / 100.0},
            inputs={"demand": throttle},
            mesh=0.0,
        )

        # Call tire model
        tire_inputs = self.get_submodel("tire").make_const_dict("inputs", 0.3)
        if self.forget_submodel_call:
            # forget to call a submodel, should raise an error
            pass
        elif self.extra_submodel_call:
            # make duplicate call to the same submodel before clearing buffer, should
            # raise an error
            tire_return = self.call_submodel("tire", inputs=tire_inputs)
            tire_return = self.call_submodel("tire", inputs=tire_inputs)
        else:
            # the correct way of doing it, just call the submodel once
            tire_return = self.call_submodel("tire", inputs=tire_inputs)

        # Make some dummy outputs
        outputs = self.make_outputs_dict(ax=AX, ay=AY)

        states_dot = self.make_dict("states_dot", vx=0.1, vy=0.2)
        return StateSpaceModelReturn(states_dot=states_dot, outputs=outputs)


@state_space_io(
    states=("engine_speed",),
    inputs=("demand",),
    outputs=("total_power", "total_torque"),
)
class HybridPowertrain(StateSpaceModel):
    _submodel_names = ("engine", "emotor")

    @classmethod
    def get_default_submodel_config(cls):
        return {"engine": "SimpleEngine", "emotor": "SimpleEMotor"}

    def forward(self, states, inputs, mesh):
        demand = inputs["demand"]
        engine_ratio = 0.8

        # Assemble states_dot vector with dummy values
        states_dot = self.make_dict("states_dot", engine_speed=-25.0)

        # Call engine
        engine_inputs = {"demand": demand * engine_ratio}
        engine_return = self.call_submodel("engine", inputs=engine_inputs)

        # Call e-motor
        emotor_inputs = {"demand": (1 - demand) * engine_ratio}
        emotor_return = self.call_submodel("emotor", inputs=emotor_inputs)

        # Use direct current model outputs and flattened submodel outputs to form the
        # combined outputs vector.
        outputs = self.make_outputs_dict(
            total_power=TOTAL_POWER, total_torque=TOTAL_TORQUE,
        )
        return StateSpaceModelReturn(outputs=outputs, states_dot=states_dot)


@model_io(inputs=("long_slip", "lat_slip"), outputs=("Fx", "Fy"))
class MF72(Model):
    def forward(self, inputs):
        outputs = self.make_dict(
            "outputs", Fx=inputs["long_slip"] * 1000, Fy=inputs["lat_slip"] * 1000
        )
        return ModelReturn(outputs=outputs)


@model_io(inputs=("demand",), outputs=("torque", "power"))
class SimpleEMotor(Model):
    def forward(self, inputs):
        outputs = self.make_dict("outputs", torque=EMOTOR_TORQUE, power=EMOTOR_POWER)
        return ModelReturn(outputs=outputs)


@model_io(inputs=("demand",), outputs=("torque", "power"))
class SimpleEngine(Model):
    def forward(self, inputs):
        outputs = self.make_dict("outputs", torque=ENGINE_TORQUE, power=ENGINE_POWER)
        return ModelReturn(outputs=outputs)


@model_io(inputs=("demand",))
class SimpleEngineWithNoOutputs(Model):
    def forward(self, inputs):
        return ModelReturn()


class TestOutputsCollection(unittest.TestCase):
    types = [
        VehicleForTest,
        HybridPowertrain,
        MF72,
        SimpleEMotor,
        SimpleEngine,
        SimpleEngineWithNoOutputs,
    ]

    @classmethod
    def setUpClass(cls):
        for model_type in cls.types:
            ModelMaker.add_to_registry(model_type)

    @classmethod
    def tearDownClass(cls):
        for model_type in cls.types:
            ModelMaker.remove_from_registry(model_type)

    def test_output_names_are_correctly_setup_after_constructions(self):
        base_config = ModelMaker.make_config("VehicleForTest")
        base_model = ModelMaker.make_model_from_config(base_config)

        self.assertIn("powertrain.engine.power", base_model.names.outputs)

        # Make sure things still work when some model doesn't have an output
        variant1_config = ModelMaker.make_config("VehicleForTest")
        variant1_config.replace_subtree(
            "powertrain.engine", ModelMaker.make_config("SimpleEngineWithNoOutputs")
        )
        variant1_model = ModelMaker.make_model_from_config(variant1_config)
        self.assertNotIn("powertrain.engine.power", variant1_model.names.outputs)

        # Check that there are no duplicates
        self.assertEqual(
            len(set(base_model.names.outputs)),
            len(base_model.names.outputs),
            msg="Duplicates detected in model output names",
        )

    def test_output_values_are_correctly_set_after_execution(self):
        base_config = ModelMaker.make_config("VehicleForTest")
        base_model = ModelMaker.make_model_from_config(base_config)

        states = base_model.make_const_dict("states", 0.1)
        inputs = base_model.make_const_dict("inputs", 0.5)

        global ENGINE_POWER, ENGINE_TORQUE
        for _ in range(10):
            # We increment the global value so that the outputs of the model should
            # change. This is to ensure the buffer for submodel returns are correctly
            # updated and clearned at every call.
            ENGINE_POWER += 1.7
            ENGINE_TORQUE += 3.2
            base_model_return = base_model.forward(states, inputs, 0.0)
            outputs = base_model_return.outputs

            # Check grand children outputs
            self.assertAlmostEqual(outputs["powertrain.engine.power"], ENGINE_POWER)
            self.assertAlmostEqual(outputs["powertrain.engine.torque"], ENGINE_TORQUE)
            self.assertAlmostEqual(outputs["powertrain.emotor.power"], EMOTOR_POWER)
            self.assertAlmostEqual(outputs["powertrain.emotor.torque"], EMOTOR_TORQUE)

            # Check child outputs
            self.assertAlmostEqual(outputs["powertrain.total_power"], TOTAL_POWER)
            self.assertAlmostEqual(outputs["powertrain.total_torque"], TOTAL_TORQUE)

            # Check top level outputs
            self.assertAlmostEqual(outputs["ax"], AX)
        self.assertAlmostEqual(outputs["ay"], AY)

    def test_exceptions_are_raised_when_missing_submodel_call(self):
        base_config = ModelMaker.make_config("VehicleForTest")
        base_model = ModelMaker.make_model_from_config(base_config)
        # Make the model forget to call a submodel
        base_model.forget_submodel_call = True

        states = base_model.make_const_dict("states", 0.1)
        inputs = base_model.make_const_dict("inputs", 0.5)

        with self.assertRaises(KeyError) as context:
            base_model_return = base_model.forward(states, inputs, 0.0)
            outputs = base_model_return.outputs

    def test_exceptions_are_raised_when_extra_submodel_call(self):
        base_config = ModelMaker.make_config("VehicleForTest")
        base_model = ModelMaker.make_model_from_config(base_config)
        # Make the model make an extra call the same submodel
        base_model.extra_submodel_call = True

        states = base_model.make_const_dict("states", 0.1)
        inputs = base_model.make_const_dict("inputs", 0.5)

        with self.assertRaises(RuntimeError) as context:
            base_model_return = base_model.forward(states, inputs, 0.0)
            outputs = base_model_return.outputs
