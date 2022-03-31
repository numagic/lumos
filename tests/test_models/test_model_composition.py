from __future__ import annotations  # Model referencing Model

from copy import deepcopy
from unittest import TestCase

import numpy as np

from lumos.models.composition import ModelMaker, CompositeModel


class TestModekMaker(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # Add test models to registry
        for t in ALL_TYPES:
            ModelMaker.add_to_registry(t)

    @classmethod
    def tearDownClass(cls) -> None:
        for t in ALL_TYPES:
            ModelMaker.remove_from_registry(t)

    def test_add_and_remove_model(self):
        ModelMaker.remove_from_registry(DummyRigidVehicle)

        with self.assertRaises(KeyError):
            ModelMaker.get_model_class(DummyRigidVehicle.__name__)

        ModelMaker.add_to_registry(DummyRigidVehicle)

        self.assertEqual(
            ModelMaker.get_model_class(DummyRigidVehicle.__name__),
            DummyRigidVehicle,
        )

    def test_make_config(self):
        model_config = ModelMaker.make_config("DummyRigidVehicle")
        expetected_config = {
            "data": "DummyRigidVehicle",
            "children": {
                "aero": {
                    "data": "DummyAeroWithDRS",
                    "children": {
                        "base": {"data": "DummyGPAeroBase", "children": {}},
                        "drs": {"data": "DummyConstDRS", "children": {}},
                    },
                },
                "tire": {"data": "DummyMF52", "children": {}},
            },
        }
        self.assertDictEqual(model_config.to_dict(), expetected_config)

    def test_make_model_from_name(self):
        """Build model with no config change or parameter change"""
        model = ModelMaker.make_model_from_name("DummyRigidVehicle")
        direct_submodel_config = DummyRigidVehicle.get_default_submodel_config()
        for name, type_name in direct_submodel_config.items():
            self.assertIsInstance(
                model.get_submodel(name),
                ModelMaker.get_model_class(type_name),
            )

        # Check grandchildren model type
        self.assertIsInstance(model.get_submodel("aero.base"), DummyGPAeroBase)

    def test_make_model_from_config(self):
        """Build model with no config change or parameter change"""
        model_config = ModelMaker.make_config("DummyRigidVehicle")
        model = ModelMaker.make_model_from_config(model_config)
        direct_submodel_config = DummyRigidVehicle.get_default_submodel_config()
        for name, type_name in direct_submodel_config.items():
            self.assertIsInstance(
                model.get_submodel(name),
                ModelMaker.get_model_class(type_name),
            )

        # Check grandchildren model type
        self.assertIsInstance(model.get_submodel("aero.base"), DummyGPAeroBase)


class TestModelComposition(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # Add test models to registry
        for t in ALL_TYPES:
            ModelMaker.add_to_registry(t)

    @classmethod
    def tearDownClass(cls) -> None:
        for t in ALL_TYPES:
            ModelMaker.remove_from_registry(t)

    def test_modify_config(self):
        default_model_config = DummyRigidVehicle.get_recursive_default_model_config()
        default_model = DummyRigidVehicle(model_config=default_model_config)

        # Change a leaf config
        # FIXME: why does deep copy just work? is it because inside it's just a dict?
        model_config = deepcopy(default_model_config)
        model_config.replace_subtree("tire", ModelMaker.make_config("DummyMF62"))
        changed_model = DummyRigidVehicle(model_config=model_config)

        self.assertIsInstance(default_model.get_submodel("tire"), DummyMF52)
        self.assertIsInstance(changed_model.get_submodel("tire"), DummyMF62)
        self.assertNotIn("thermal_coeff", default_model.get_submodel("tire")._params)
        self.assertIn("thermal_coeff", changed_model.get_submodel("tire")._params)

        # TODO: Change a multi-level down config is clumsy
        model_config = deepcopy(default_model_config)
        model_config.replace_subtree(
            "aero.base", ModelMaker.make_config("DummyLinearAeroBase")
        )
        changed_model = DummyRigidVehicle(model_config=model_config)
        self.assertIsInstance(
            changed_model.get_submodel("aero.base"), DummyLinearAeroBase
        )

        # Change a non-leaf config
        model_config = deepcopy(default_model_config)
        model_config.replace_subtree(
            "aero", ModelMaker.make_config("DummyAeroWithoutDRS")
        )
        changed_model = DummyRigidVehicle(model_config=model_config)
        self.assertIsInstance(default_model.get_submodel("aero"), DummyAeroWithDRS)
        self.assertIsInstance(changed_model.get_submodel("aero"), DummyAeroWithoutDRS)
        self.assertIsInstance(default_model.get_submodel("aero.base"), DummyGPAeroBase)
        self.assertIsInstance(
            changed_model.get_submodel("aero.base"), DummyLinearAeroBase
        )
        self.assertNotIn("weights", default_model.get_submodel("aero.base")._params)
        self.assertIn("weights", changed_model.get_submodel("aero.base")._params)

        pass

    def test_get_set_params(self):
        default_model_config = DummyRigidVehicle.get_recursive_default_model_config()
        default_model = DummyRigidVehicle(model_config=default_model_config)
        default_params = default_model.get_recursive_default_params()

        # FIXME: how does this work for tree?
        changed_params = deepcopy(default_params)

        # TODO: simplify parameter change syntax
        mass, cz_modifier, alpha, mux = 2000, 0.3, np.ones(128) * 3, 0.1

        changed_params.set_param("mass", mass)
        changed_params.set_param("aero.cz_modifier", cz_modifier)
        changed_params.set_param("aero.base.alpha", alpha)
        changed_params.set_param("tire.mux", mux)

        default_model.set_recursive_params(changed_params)
        self.assertEqual(default_model._params["mass"], mass)
        self.assertEqual(
            default_model.get_submodel("aero")._params["cz_modifier"], cz_modifier
        )
        np.testing.assert_allclose(
            default_model.get_submodel("aero.base")._params["alpha"],
            alpha,
        )
        self.assertEqual(default_model.get_submodel("tire")._params["mux"], mux)

        # Create new model from scratch
        new_model = DummyRigidVehicle(
            model_config=default_model_config, params=changed_params
        )
        self.assertEqual(new_model._params["mass"], mass)
        self.assertEqual(
            new_model.get_submodel("aero")._params["cz_modifier"], cz_modifier
        )
        np.testing.assert_allclose(
            new_model.get_submodel("aero.base")._params["alpha"],
            alpha,
        )
        self.assertEqual(new_model.get_submodel("tire")._params["mux"], mux)

        # Check get/set/get loop
        new_model.set_recursive_params(default_params)
        returned_params = new_model.get_recursive_params()
        self.assertEqual(
            str(default_params),
            str(returned_params),
            msg="Parameters did not stay the same in a get/set/get loop",
        )


class DummyRigidVehicle(CompositeModel):
    _submodel_names = ("aero", "tire")

    @classmethod
    def get_default_submodel_config(cls):
        return {"aero": "DummyAeroWithDRS", "tire": "DummyMF52"}

    @classmethod
    def get_default_params(cls):
        return {"mass": 1800, "power": 250000}


class DummyAeroWithDRS(CompositeModel):
    _submodel_names = ("base", "drs")

    @classmethod
    def get_default_submodel_config(cls):
        return {"base": "DummyGPAeroBase", "drs": "DummyConstDRS"}

    @classmethod
    def get_default_params(cls):
        return {"cz_modifier": 1.0, "cd_modifier": 1.2}


class DummyAeroWithoutDRS(CompositeModel):
    _submodel_names = ("base",)

    @classmethod
    def get_default_submodel_config(cls):
        return {"base": "DummyLinearAeroBase"}

    @classmethod
    def get_default_params(cls):
        return {"cz_modifier": 1.0, "cd_modifier": 1.2}


class DummyGPAeroBase(CompositeModel):
    """This is a concrete class that can be instantiated"""

    _submodel_names = ()

    @classmethod
    def get_default_params(cls):
        return {"alpha": np.ones(128)}


class DummyLinearAeroBase(CompositeModel):
    """This is a concrete class that can be instantiated"""

    _submodel_names = ()

    @classmethod
    def get_default_params(cls):
        return {"weights": np.zeros(7)}


class DummyConstDRS(CompositeModel):
    _submodel_names = ()

    @classmethod
    def get_default_params(cls):
        return {"cd_delta": -0.2, "cz_delta": -0.4}


class DummyMF52(CompositeModel):
    _submodel_names = ()

    @classmethod
    def get_default_params(cls):
        return {"mux": 0.96, "muy": 0.94}


class DummyMF62(CompositeModel):
    _submodel_names = ()

    @classmethod
    def get_default_params(cls):
        return {"mux": 0.96, "muy": 0.94, "thermal_coeff": 0.3}


ALL_TYPES = [
    DummyRigidVehicle,
    DummyMF52,
    DummyMF62,
    DummyAeroWithDRS,
    DummyAeroWithoutDRS,
    DummyGPAeroBase,
    DummyLinearAeroBase,
    DummyConstDRS,
]
