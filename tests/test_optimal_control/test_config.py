import numpy as np
from unittest import TestCase

from lumos.optimal_control.config import (
    BoundaryConditionConfig,
    GlobalVarBoundConfig,
    GlobalVarScaleConfig,
    SimConfig,
    StageVarBoundConfig,
    StageVarScaleConfig,
)


class TestStageVarBoundConfig(TestCase):
    def test_construction(self):
        """Test both correct and incorrect constructions of StageVarBoundConfig"""
        # both scalars, should work
        kwargs = {"group": "states", "name": "x", "values": (1.0, 2.0)}
        bounds = StageVarBoundConfig(**kwargs)
        for k, v in kwargs.items():
            self.assertEqual(getattr(bounds, k), v)

        # both arrays, should work
        kwargs = {
            "group": "states",
            "name": "x",
            "values": (np.ones(3), np.ones(3) * 2),
        }
        bounds = StageVarBoundConfig(**kwargs)
        for k, v in kwargs.items():
            self.assertEqual(getattr(bounds, k), v)

        # one scalar, one array, should fail
        with self.assertRaises(TypeError):
            bounds = StageVarBoundConfig("states", "x", (1.0, np.ones(10)))
        with self.assertRaises(TypeError):
            bounds = StageVarBoundConfig("states", "x", (np.ones(10), 1.0))

        # 2d array, should fail
        with self.assertRaises(AssertionError):
            bounds = StageVarBoundConfig("states", "x", (np.ones((10, 1)), np.ones(10)))

        # arrays of different sizes, should fail
        with self.assertRaises(AssertionError):
            bounds = StageVarBoundConfig("states", "x", (np.ones(10), np.ones(11)))

        # scalar incorrect range, should fail
        with self.assertRaises(AssertionError):
            bounds = StageVarBoundConfig("states", "x", (1.0, 0.0))

        # scalar incorrect range, should fail
        with self.assertRaises(AssertionError):
            bounds = StageVarBoundConfig(
                "states", "x", (np.array([1.0, 2.0, 3.0]), np.array([2.0, 1.0, 2.0]))
            )


class TestGlobalVarBoundConfig(TestCase):
    def test_construction(self):
        """Test both correct and incorrect constructions of TestGlobalVarBoundConfig"""
        # both scalars, should work
        kwargs = {"name": "mesh_scale", "values": (1.0, 2.0)}
        bounds = GlobalVarBoundConfig(**kwargs)
        for k, v in kwargs.items():
            self.assertEqual(getattr(bounds, k), v)

        # both arrays, should fail
        with self.assertRaises(TypeError):
            bounds = GlobalVarBoundConfig(
                "mesh_scale", (np.array([1.0, 2.0, 3.0]), np.array([2.0, 1.0, 2.0]))
            )

        # scalar incorrect range, should fail
        with self.assertRaises(AssertionError):
            bounds = GlobalVarBoundConfig("mesh_scale", (1.0, 0.0))


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
                StageVarBoundConfig("states", "x", (0.0, 2.0)),
                GlobalVarBoundConfig("mesh_scale", (0.0, 2.0)),
            ),
            scales=(
                StageVarScaleConfig("states", "x", 2.0),
                GlobalVarScaleConfig("mesh_scale", 10.0),
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
