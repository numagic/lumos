import unittest

import numpy as np

from lumos.optimal_control.utils import batch_conv1d, stack_and_increment


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
