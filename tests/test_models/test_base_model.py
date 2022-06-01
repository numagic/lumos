import unittest

import numpy as np

from lumos.models.base import (
    Model,
    ModelReturn,
    StateSpaceModel,
    StateSpaceModelReturn,
    model_io,
    state_space_io,
)
from lumos.models.composition import ModelMaker
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


# Here we test the automatic output collection functionality
# TODO:
# 1) also needs to test con_outputs still work correctly -> maybe we should move
# con_outputs definition output of the model, as we can set any outputs subset to be
# con_outputs!
# 2) it's quite easy to make the mistake of forgetting a tuple with only 1 ewlement
# needs a comma as well, in name definition. And error message is not helpful
# 3) its' quite common to make the mistake of mixing model_return with model_return.outputs
# and the error message is not helping -> we can create a better error message in get_xxx
# 4) the 'make_vector' syntax expects a scalar for each kwargs, but if we get an array,
# it just carries on and fail later at arbitrary places
# 5) do we really want to keep the model's main 'forward' I/O as arrays? Given how often
# we do ops like getting a scalar from the vector or merging scalars to form a vector,
# maybe vectors form a 'low-level' I/O used for computation, and we can use namedtuples
# or dictionaries for 'user-facing' I/O? With vectors, even after getting the output
# from a model, we still need to have access to that model in order to extract the
# correct element from the vector!
# 6) do we really need states_dot with names '_dot'? If they are always separated by the
# groups with states, then ideally we could just keep them with the same name!
# 7）can we get rid of the need to define the '_submodel_names' attribute? it is
# redudant when we have the get_default_submodel_config class method defined.


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
class TestVehicle(StateSpaceModel):
    _submodel_names = ("powertrain", "tire")

    @classmethod
    def get_default_submodel_config(cls):
        return {"powertrain": "HybridPowertrain", "tire": "MF72"}

    def forward(self, states, inputs, mesh):
        vx = self.get_state(states, "vx")
        throttle = self.get_input(inputs, "throttle")

        # Call powertrain model
        powertrain_model = self.get_submodel("powertrain")
        powertrain_inputs = powertrain_model.make_vector("inputs", demand=throttle)
        powertrain_states = powertrain_model.make_vector(
            "states", engine_speed=vx / 100.0
        )

        powertrain_return = powertrain_model.forward(
            powertrain_states, powertrain_inputs, 0.0
        )

        # Call tire model
        tire_model = self.get_submodel("tire")
        tire_inputs = tire_model.make_const_vector("inputs", 0.3)
        tire_return = tire_model.forward(tire_inputs)

        submodel_outputs = self.combine_submodel_outputs(
            powertrain=powertrain_return.outputs, tire=tire_return.outputs,
        )

        # Make some dummy outputs
        outputs = self.make_vector("outputs", ax=AX, ay=AY, **submodel_outputs)
        states_dot = self.make_vector("states_dot", vx_dot=0.1, vy_dot=0.2)
        return self.make_state_space_model_return(
            states_dot=states_dot, outputs=outputs
        )


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
        demand = self.get_input(inputs, "demand")
        engine_ratio = 0.8

        # Assemble states_dot vector with dummy values
        states_dot = self.make_vector("states_dot", engine_speed_dot=-25.0)

        # Call engine
        engine_model = self.get_submodel("engine")
        engine_inputs = engine_model.make_vector("inputs", demand=demand * engine_ratio)
        engine_return = engine_model.forward(engine_inputs)

        # Call e-motor
        emotor_model = self.get_submodel("emotor")
        emotor_inputs = emotor_model.make_vector(
            "inputs", demand=(1 - demand) * engine_ratio
        )
        emotor_return = emotor_model.forward(emotor_inputs)

        # Combine all submodel outputs into a flattened dictionary
        submodel_outputs = self.combine_submodel_outputs(
            engine=engine_return.outputs, emotor=emotor_return.outputs,
        )

        # Use direct current model outputs and flattened submodel outputs to form the
        # combined outputs vector.
        outputs = self.make_vector(
            "outputs",
            total_power=TOTAL_POWER,
            total_torque=TOTAL_TORQUE,
            **submodel_outputs
        )
        return self.make_state_space_model_return(
            outputs=outputs, states_dot=states_dot
        )


@model_io(inputs=("long_slip", "lat_slip"), outputs=("Fx", "Fy"))
class MF72(Model):
    def forward(self, inputs):
        long_slip = self.get_input(inputs, "long_slip")
        lat_slip = self.get_input(inputs, "lat_slip")
        outputs = self.make_vector("outputs", Fx=long_slip * 1000, Fy=lat_slip * 1000)
        return ModelReturn(outputs=outputs)


@model_io(inputs=("demand",), outputs=("torque", "power"))
class SimpleEMotor(Model):
    def forward(self, inputs):
        outputs = self.make_vector("outputs", torque=EMOTOR_TORQUE, power=EMOTOR_POWER)
        return ModelReturn(outputs=outputs)


@model_io(inputs=("demand",), outputs=("torque", "power"))
class SimpleEngine(Model):
    def forward(self, inputs):
        outputs = self.make_vector("outputs", torque=ENGINE_TORQUE, power=ENGINE_POWER)
        return ModelReturn(outputs=outputs)


@model_io(inputs=("demand",))
class SimpleEngineWithNoOutputs(Model):
    def forward(self, inputs):
        return ModelReturn()


class TestOutputsCollection(unittest.TestCase):
    types = [
        TestVehicle,
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
        base_config = ModelMaker.make_config("TestVehicle")
        base_model = ModelMaker.make_model_from_config(base_config)

        self.assertIn("powertrain.engine.power", base_model.names.outputs)

        # Make sure things still work when some model doesn't have an output
        variant1_config = ModelMaker.make_config("TestVehicle")
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
        base_config = ModelMaker.make_config("TestVehicle")
        base_model = ModelMaker.make_model_from_config(base_config)

        states = base_model.make_const_vector("states", 1.0)
        inputs = base_model.make_const_vector("inputs", 0.5)

        base_model_return = base_model.forward(states, inputs, 0.0)
        outputs = base_model_return.outputs

        # Check grand children outputs
        self.assertAlmostEqual(
            base_model.get_output(outputs, "powertrain.engine.power"), ENGINE_POWER
        )
        self.assertAlmostEqual(
            base_model.get_output(outputs, "powertrain.engine.torque"), ENGINE_TORQUE
        )
        self.assertAlmostEqual(
            base_model.get_output(outputs, "powertrain.emotor.power"), EMOTOR_POWER
        )
        self.assertAlmostEqual(
            base_model.get_output(outputs, "powertrain.emotor.torque"), EMOTOR_TORQUE
        )

        # Check child outputs
        self.assertAlmostEqual(
            base_model.get_output(outputs, "powertrain.total_power"), TOTAL_POWER
        )
        self.assertAlmostEqual(
            base_model.get_output(outputs, "powertrain.total_torque"), TOTAL_TORQUE
        )

        # Check top level outputs
        self.assertAlmostEqual(base_model.get_output(outputs, "ax"), AX)
        self.assertAlmostEqual(base_model.get_output(outputs, "ay"), AY)
