from collections import namedtuple
import unittest

import numpy as np
from parameterized import parameterized_class

from lumos.optimal_control.utils import (
    DecVarOperator,
    batch_conv1d,
    stack_and_increment,
)


class TestBatchConv1d(unittest.TestCase):
    def test_1d(self):
        """Correct batch matrix for 1d input"""

        width, stride, batch = 5, 4, 100
        length = stride * (batch - 1) + width

        x = np.arange(length)
        y = batch_conv1d(x, width=width, stride=stride)

        self.assertEqual(y.shape, (batch, width))
        np.testing.assert_equal(y[0], x[:width])
        np.testing.assert_equal(y[1], [4, 5, 6, 7, 8])
        np.testing.assert_equal(y[-1], x[-width:])

    def test_1d_wrong_shape(self):

        width, stride, batch = 5, 4, 100
        # Deliverately making the shape wrong
        length = stride * (batch - 1) + width + 3

        x = np.arange(length)
        with self.assertRaises(ValueError):
            y = batch_conv1d(x, width=width, stride=stride)

    def test_2d(self):
        width, stride, channels, batch = 5, 4, 11, 100
        length = stride * (batch - 1) + width

        x = np.tile(np.arange(length), (channels, 1)).T
        y = batch_conv1d(x, width=width, stride=stride)

        self.assertEqual(y.shape, (batch, width, channels))
        np.testing.assert_equal(y[0], x[:width])
        np.testing.assert_equal(y[1], np.tile([4, 5, 6, 7, 8], (channels, 1)).T)
        np.testing.assert_equal(y[-1], x[-width:])


class TestStackAndIncrement(unittest.TestCase):
    def test_stack_and_increment(self):

        # Test with lead axis
        base = np.array([1, 2, 3, 4])
        axis, num_repeat, num_increment = 0, 2, 3
        expected = np.array([[1, 2, 3, 4], [4, 5, 6, 7]])

        np.testing.assert_array_equal(
            stack_and_increment(base, axis, num_repeat, num_increment), expected
        )

        # Test with final axis
        base = np.array([1, 2, 3, 4])
        axis, num_repeat, num_increment = -1, 2, 3
        expected = np.array([[1, 2, 3, 4], [4, 5, 6, 7]]).T

        np.testing.assert_array_equal(
            stack_and_increment(base, axis, num_repeat, num_increment), expected
        )

        # Test by checking deltas
        base = np.arange(12).reshape((3, 4))
        axis, num_repeat, num_increment = 0, 2, 3
        out = stack_and_increment(base, axis, num_repeat, num_increment)

        # Check size is correct
        np.testing.assert_array_equal(out.shape, [num_repeat, *base.shape])

        # Check increment is correct
        delta = np.diff(out, axis=axis)
        self.assertTrue(np.all(delta == num_increment))


# We test both with and without global variables
@parameterized_class(
    [
        {"global_var_names": ("mesh_scale", "another_global_var")},
        {"global_var_names": ()},
    ]
)
class TestDecVarOperator(unittest.TestCase):
    num_intervals: int = 99
    num_stages_per_interval: int = 3

    def setUp(self):
        self.num_stages = self.num_intervals * (self.num_stages_per_interval - 1) + 1

        NameTuple = namedtuple(
            "ModelIO", ["states", "inputs", "con_outputs", "residuals"]
        )
        model_var_names = NameTuple(
            states=["x", "y", "z"],
            inputs=["throttle", "steer"],
            con_outputs=["stability", "temperature"],
            residuals=["res0"],
        )

        self.op = DecVarOperator(
            model_var_names=model_var_names,
            num_intervals=self.num_intervals,
            num_stages_per_interval=self.num_stages_per_interval,
            stage_var_groups=("states", "inputs", "con_outputs", "residuals"),
            global_var_names=self.global_var_names,
        )

    def test_get_var_index_in_dec(self):
        """Test getting the index of a variable at one stage or all stages."""

        # Test positive stage
        idx = self.op.get_var_index_in_dec("states", "y", stage=2)
        expected_idx = 2 * 8 + 1
        self.assertEqual(idx, expected_idx)

        # Test negative stage
        idx = self.op.get_var_index_in_dec("inputs", "steer", stage=-3)
        expected_idx = (self.num_stages - 3) * 8 + 4
        self.assertEqual(idx, expected_idx)

        # Test wrong index
        with self.assertRaises(ValueError):
            idx = self.op.get_var_index_in_dec(
                "inputs", "steer", stage=-self.num_stages - 1
            )
        with self.assertRaises(ValueError):
            idx = self.op.get_var_index_in_dec("inputs", "steer", stage=self.num_stages)

        # Test getting all stages
        idx = self.op.get_var_index_in_dec("residuals", "res0")
        expected_idx = 7 + np.arange(self.num_stages) * 8
        np.testing.assert_array_equal(idx, expected_idx)

        if self.op.has_global_var():
            # Test global index without giving stage
            idx = self.op.get_var_index_in_dec("global", "mesh_scale")
            expected_idx = self.op.num_dec - 2
            self.assertEqual(idx, expected_idx)

            # Test global index with stage (but it should be just ignored)
            idx = self.op.get_var_index_in_dec("global", "another_global_var", stage=10)
            expected_idx = self.op.num_dec - 1
            self.assertEqual(idx, expected_idx)

    def test_get_var_index_in_group(self):
        # Test a state
        idx = self.op.get_var_index_in_group("states", "y")
        expected_idx = 1
        self.assertEqual(idx, expected_idx)

        # Test a con_outputs
        idx = self.op.get_var_index_in_group("con_outputs", "stability")
        expected_idx = 0
        self.assertEqual(idx, expected_idx)

        # Test a global var
        if self.op.has_global_var():
            idx = self.op.get_var_index_in_group("global", "mesh_scale")
            expected_idx = 0
            self.assertEqual(idx, expected_idx)

    def test_split_stage_and_global_vars(self):
        x = np.arange(self.op.num_dec)
        stage_vars, global_vars = self.op.split_stage_and_global_vars(x)

        np.testing.assert_array_almost_equal(
            stage_vars, x[: self.op.num_dec - self.op.num_global_var]
        )
        np.testing.assert_array_almost_equal(
            global_vars, x[self.op.num_dec - self.op.num_global_var :]
        )

    def _compare_flattened_and_unflattened(self, flattened, unflattened):
        """Check values are euivalent in flattened and unflattend decision variables"""
        for stage, group, name in (
            (10, "states", "y"),
            (0, "inputs", "throttle"),
            (-1, "con_outputs", "temperature"),
            (21, "residuals", "res0"),
        ):
            self.assertAlmostEqual(
                self.op.get_var(flattened, group, name, stage),
                getattr(unflattened, group)[
                    stage, self.op.get_var_index_in_group(group, name)
                ],
            )

        if self.op.has_global_var():
            for name in self.global_var_names:
                self.assertAlmostEqual(
                    self.op.get_var(flattened, "global", name),
                    getattr(unflattened, name),
                )

    def test_flatten(self):
        x = np.random.randn(self.op.num_dec)
        unflattened = self.op.unflatten_var(x)
        flattened = self.op.flatten_var(**unflattened._asdict())

        self._compare_flattened_and_unflattened(flattened, unflattened)

    def test_unflatten(self):
        flattened = np.random.randn(self.op.num_dec)
        unflattened = self.op.unflatten_var(flattened)

        # Check the sizes are correct
        for group in self.op._stage_var_groups:
            num_stages, num_var = getattr(unflattened, group).shape
            self.assertEqual(num_stages, self.num_stages)
            self.assertEqual(num_var, self.op.get_stage_var_size(group))

        self._compare_flattened_and_unflattened(flattened, unflattened)
