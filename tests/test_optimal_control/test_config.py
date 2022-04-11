import numpy as np
from unittest import TestCase

from lumos.optimal_control.config import (
    BoundaryConditionConfig,
    BoundConfig,
    ScaleConfig,
    SimConfig,
)


class TestBoundConfig(TestCase):
    def test_stage_var_bound_construction(self):
        """Test both correct and incorrect constructions of BoundConfig for stage vars"""
        # both scalars, should work
        kwargs = {"group": "states", "name": "x", "values": (1.0, 2.0)}
        bounds = BoundConfig(**kwargs)
        for k, v in kwargs.items():
            self.assertEqual(getattr(bounds, k), v)

        # both arrays, should work
        kwargs = {
            "group": "states",
            "name": "x",
            "values": (np.ones(3), np.ones(3) * 2),
        }
        bounds = BoundConfig(**kwargs)
        for k, v in kwargs.items():
            self.assertEqual(getattr(bounds, k), v)

        # one scalar, one array, should fail
        with self.assertRaises(TypeError):
            bounds = BoundConfig("states", "x", (1.0, np.ones(10)))
        with self.assertRaises(TypeError):
            bounds = BoundConfig("states", "x", (np.ones(10), 1.0))

        # 2d array, should fail
        with self.assertRaises(AssertionError):
            bounds = BoundConfig("states", "x", (np.ones((10, 1)), np.ones(10)))

        # arrays of different sizes, should fail
        with self.assertRaises(AssertionError):
            bounds = BoundConfig("states", "x", (np.ones(10), np.ones(11)))

        # scalar incorrect range, should fail
        with self.assertRaises(AssertionError):
            bounds = BoundConfig("states", "x", (1.0, 0.0))

        # scalar incorrect range, should fail
        with self.assertRaises(AssertionError):
            bounds = BoundConfig(
                "states", "x", (np.array([1.0, 2.0, 3.0]), np.array([2.0, 1.0, 2.0]))
            )

    def test_global_var_bound_construction(self):
        """Test both correct and incorrect constructions of BoundConfig for global vars"""
        # both scalars, should work
        kwargs = {"group": "global", "name": "mesh_scale", "values": (1.0, 2.0)}
        bounds = BoundConfig(**kwargs)
        for k, v in kwargs.items():
            self.assertEqual(getattr(bounds, k), v)

        # both arrays, should fail
        with self.assertRaises(TypeError):
            bounds = BoundConfig(
                "mesh_scale", (np.array([1.0, 2.0, 3.0]), np.array([2.0, 1.0, 2.0]))
            )

        # scalar incorrect range, should fail
        with self.assertRaises(AssertionError):
            bounds = BoundConfig("global", "mesh_scale", (1.0, 0.0))


class TestSimConfig(TestCase):
    def test_mutable_fields_are_not_shared(self):
        """Ensure that mutable fields don't use shared memory across objects"""
        config1 = SimConfig()
        config2 = SimConfig()

        config1.non_cyclic_vars += ["a", "b"]

        # Check config2 is not affected
        self.assertFalse(config2.non_cyclic_vars)

    def test_to_dict_and_back(self):
        """Test values remain the same when converting to dictionary and back"""
        sim_config = SimConfig(
            num_intervals=39,
            transcription=("LGR", {"num_stages": 3}),
            is_cyclic=True,
            non_cyclic_vars=["a", "b"],
            bounds=(
                BoundConfig("states", "x", (0.0, 2.0)),
                BoundConfig("global", "mesh_scale", (0.0, 2.0)),
            ),
            scales=(
                ScaleConfig("states", "x", 2.0),
                ScaleConfig("global", "mesh_scale", 10.0),
            ),
            boundary_conditions=(
                BoundaryConditionConfig(0, "states", "x", 1.0),
                BoundaryConditionConfig(0, "states", "y", 1.0),
            ),
        )

        # config -> dict -> config -> dict reproduces the same dict
        sim_dict = sim_config.to_dict()
        self.assertEqual(sim_config, SimConfig(**sim_dict))
        self.assertDictEqual(sim_dict, SimConfig(**sim_dict).to_dict())
