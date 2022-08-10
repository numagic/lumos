from copy import deepcopy
from typing import Callable
from unittest import TestCase

import numpy as np
from casadi import MX

from lumos.models.tree_utils import ParameterTree, ConfigTree


class TestParameterTree(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        mass, power = 1800, 250000
        cz_modifier, cd_modifier = 1.2, 0.9
        alpha = np.random.randn(7)
        delta = -0.3
        mux, muy = 0.98, 0.87
        array_1d = np.random.randn(3)
        array_2d = np.random.randn(4, 4)
        cls.param_dict = {
            "data": {"mass": mass, "power": power},
            "children": {
                "aero": {
                    "data": {"cz_modifier": cz_modifier, "cd_modifier": cd_modifier},
                    "children": {
                        "base": {"data": {"alpha": alpha}, "children": {}},
                        "drs": {"data": {"delta": delta}, "children": {}},
                    },
                },
                "tire": {
                    "data": {
                        "mux": mux,
                        "muy": muy,
                        "array_1d": array_1d,
                        "array_2d": array_2d,
                    },
                    "children": {},
                },
            },
        }

        cls.expected_flat_dict = {
            "mass": mass,
            "power": power,
            "aero.cz_modifier": cz_modifier,
            "aero.cd_modifier": cd_modifier,
            "aero.base.alpha": alpha,
            "aero.drs.delta": delta,
            "tire.mux": mux,
            "tire.muy": muy,
            "tire.array_1d": array_1d,
            "tire.array_2d": array_2d,
        }

    def test_from_dict(self):

        # Test with a real-ish nested param
        pt = ParameterTree.from_dict(self.param_dict)

        self.assertAlmostEqual(pt.data["mass"], self.param_dict["data"]["mass"])
        np.testing.assert_allclose(
            pt.get_child("aero").get_child("base").data["alpha"],
            self.param_dict["children"]["aero"]["children"]["base"]["data"]["alpha"],
        )

    def test_to_dict(self):
        pt = ParameterTree.from_dict(self.param_dict)
        np.testing.assert_equal(pt.to_dict(), self.param_dict)

    def test_to_and_from_flat_dict(self):

        pt = ParameterTree.from_dict(self.param_dict)
        flat_dict, tree_def = pt.to_flat_dict()
        np.testing.assert_equal(flat_dict, self.expected_flat_dict)

        reconstructed_pt = ParameterTree.from_flat_dict(tree_def, flat_dict)

        # NOTE: we had a bug once where converting to flat_dict would modify the root
        # data for parameters (because it's a dict and we modified it in place). Hence
        # here we test against self.param_dict, because pt.to_dict() would also contain
        # modified dict, which is why we didn't catch the original bug
        np.testing.assert_equal(reconstructed_pt.to_dict(), self.param_dict)

    def test_jax_tree_flatten(self):
        """Methods required by jax for custom pytree

        We only check reconstruction gives the same results
        """
        # jax reconstruction
        pt = ParameterTree.from_dict(self.param_dict)
        children, aux = pt.tree_flatten()
        reconstructed = ParameterTree.tree_unflatten(aux, children)
        np.testing.assert_equal(reconstructed.to_dict(), pt.to_dict())

    def test_unravel_casadi_params_based_on_numpy_tree(self):
        """See models.base.StateSpaceModel._make_casadi_model_algebra_cons
        
        Models come with default parameters defined in numpy. To create the equivalent
        parameter tree in casadi, we currently:
        1) ravel the numpy TreeParam, get an unravel function, and flat numpy params
        2) create a casadi flat params, using the size of the numpy params
        3) unravel the casadi flat params to create a casadi Tree Params

        Since casadi only has 2d array types (1d arrays are made into column 2d arrays)
        the shapes would need some special treatment

        This test is added after we ran into bugs where if parameters contain 1d arrays,
        it won't work.
        """
        params = ParameterTree.from_dict(self.param_dict)
        flat_params, unravel = params.tree_ravel()

        cas_flat_params = MX.sym("params", len(flat_params))

        # We main just check that the unravel from a numpy TreeParam still works on
        # casadi flat params.
        cas_dict_params = unravel(cas_flat_params)

    def test_tree_ravel(self):
        pt = ParameterTree.from_dict(self.param_dict)
        flat_array, unravel = pt.tree_ravel()

        self.assertIsInstance(flat_array, np.ndarray)
        self.assertIsInstance(unravel, Callable)

        reconstructed = unravel(flat_array)

        np.testing.assert_equal(pt.to_dict(), reconstructed.to_dict())

    def test_modifying_dict_wont_modify_tree(self):
        pt = ParameterTree.from_dict(deepcopy(self.param_dict))

        original_mass = pt.get_param("mass")
        original_alpha = pt.get_param("aero.base.alpha")

        # check tree -> dict -> tree, and modify dict
        p_dict = pt.to_dict()
        new_pt = ParameterTree.from_dict(p_dict)

        p_dict["data"]["mass"] += 100
        p_dict["children"]["aero"]["children"]["base"]["data"][
            "alpha"
        ] = np.random.randn(10)

        self.assertAlmostEqual(pt.get_param("mass"), original_mass)
        np.testing.assert_allclose(pt.get_param("aero.base.alpha"), original_alpha)

        self.assertAlmostEqual(new_pt.get_param("mass"), original_mass)
        np.testing.assert_allclose(new_pt.get_param("aero.base.alpha"), original_alpha)

        # tree -> flat dict -> tree, and modify flat dict
        flat_dict, tree_def = pt.to_flat_dict()
        new_pt = ParameterTree.from_flat_dict(tree_def, flat_dict)

        flat_dict["mass"] += 100
        flat_dict["aero.base.alpha"] = np.random.randn(10)

        self.assertAlmostEqual(pt.get_param("mass"), original_mass)
        np.testing.assert_allclose(pt.get_param("aero.base.alpha"), original_alpha)

        self.assertAlmostEqual(new_pt.get_param("mass"), original_mass)
        np.testing.assert_allclose(new_pt.get_param("aero.base.alpha"), original_alpha)

    def test_modifying_tree_wont_modify_dict(self):
        p_dict = deepcopy(self.param_dict)

        original_mass = p_dict["data"]["mass"]
        original_alpha = p_dict["children"]["aero"]["children"]["base"]["data"]["alpha"]

        # check dict -> tree -> new dict, and modify tree
        pt = ParameterTree.from_dict(p_dict)
        new_p_dict = pt.to_dict()

        pt.set_param("mass", pt.get_param("mass") + 100)
        pt.set_param("aero.base.alpha", np.random.randn(10))

        self.assertAlmostEqual(p_dict["data"]["mass"], original_mass)
        np.testing.assert_allclose(
            p_dict["children"]["aero"]["children"]["base"]["data"]["alpha"],
            original_alpha,
        )

        self.assertAlmostEqual(new_p_dict["data"]["mass"], original_mass)
        np.testing.assert_allclose(
            new_p_dict["children"]["aero"]["children"]["base"]["data"]["alpha"],
            original_alpha,
        )

        flat_dict, tree_def = ParameterTree.from_dict(
            deepcopy(self.param_dict)
        ).to_flat_dict()
        # flat dict -> tree -> flat dict, and modify params

        new_pt = ParameterTree.from_flat_dict(tree_def, flat_dict)
        new_flat_dict, _ = new_pt.to_flat_dict()

        new_pt.set_param("mass", new_pt.get_param("mass") + 100)
        new_pt.set_param("aero.base.alpha", np.random.randn(10))

        self.assertAlmostEqual(flat_dict["mass"], original_mass)
        np.testing.assert_allclose(flat_dict["aero.base.alpha"], original_alpha)

        self.assertAlmostEqual(new_flat_dict["mass"], original_mass)
        np.testing.assert_allclose(new_flat_dict["aero.base.alpha"], original_alpha)

    def test_get_param(self):
        pt = ParameterTree.from_dict(self.param_dict)

        self.assertAlmostEqual(pt.get_param("mass"), pt.data["mass"])
        np.testing.assert_equal(
            pt.get_param("aero.base.alpha"),
            pt.get_child("aero").get_child("base").data["alpha"],
        )

    def test_set_param(self):
        new_mass = 2100
        new_alpha = np.linspace(0, 10, 7)
        pt = ParameterTree.from_dict(self.param_dict)

        pt.set_param("mass", new_mass)
        self.assertAlmostEqual(pt.get_param("mass"), new_mass)

        # NOTE: if the future, we might want to impose size check etc.
        pt.set_param("aero.base.alpha", new_alpha)
        np.testing.assert_array_almost_equal(pt.get_param("aero.base.alpha"), new_alpha)


# TODO: we don't test the config as verbose as the parameter, but maybe we should.
# Meanwhile, maybe some of the tests could be abstracted out? but the data types are
# different... Maybe we could test the parent class?
class TestConfigTree(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        vehicle_body = "RigidBody"
        tire = "RoundTire"
        aero = "FabulousAero"
        aero_base = "GP"
        aero_drs = "Wiggly"
        cls.config_dict = {
            "data": vehicle_body,
            "children": {
                "aero": {
                    "data": aero,
                    "children": {
                        "base": {"data": aero_base, "children": {}},
                        "drs": {"data": aero_drs, "children": {}},
                    },
                },
                "tire": {"data": tire, "children": {}},
            },
        }

        cls.expected_flat_dict = {
            "": vehicle_body,
            "tire": tire,
            "aero": aero,
            "aero.base": aero_base,
            "aero.drs": aero_drs,
        }

    def test_from_to_dict(self):
        ct = ConfigTree.from_dict(self.config_dict)

        self.assertEqual(ct.get_child("tire").data, self.expected_flat_dict["tire"])
        self.assertEqual(
            ct.get_child("aero").get_child("base").data,
            self.expected_flat_dict["aero.base"],
        )

        new_dict = ct.to_dict()

        np.testing.assert_equal(new_dict, self.config_dict)

    def test_to_from_flat_dict(self):
        ct = ConfigTree.from_dict(self.config_dict)

        flat_dict, tree_def = ct.to_flat_dict()

        self.assertDictEqual(flat_dict, self.expected_flat_dict)

        new_dict = ConfigTree.from_flat_dict(tree_def, flat_dict).to_dict()
        np.testing.assert_equal(new_dict, self.config_dict)

    def test_replace_subtree(self):
        ct = ConfigTree.from_dict(self.config_dict)

        new_aero = "NewAero"
        new_aero_base = "NewAeroBase"
        new_aero_drs = "NewAeroDRS"

        new_aero_config = {
            "data": new_aero,
            "children": {
                "base": {"data": new_aero_base, "children": {}},
                "drs": {"data": new_aero_drs, "children": {}},
            },
        }

        with self.assertRaises(TypeError):
            ct.replace_subtree("aero", new_aero_config)

        ct.replace_subtree("aero", ConfigTree.from_dict(new_aero_config))
        self.assertEqual(ct.get_child("aero").data, new_aero)
        self.assertEqual(ct.get_child("aero").get_child("base").data, new_aero_base)

        # Replace a child config that doesnt exist should throw an error instead of
        # replacing the dict value silently with the wrong child name
        with self.assertRaises(KeyError):
            ct.replace_subtree(
                "aero.bose", ConfigTree.from_dict({"data": "Bose", "children": {}})
            )

        self.assertEqual(ct.get_child("aero").get_child("base").data, new_aero_base)
