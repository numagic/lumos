import unittest

import jax.numpy as jnp
import numpy as np
from casadi import SX


import lumos.numpy as lnp


class TestBasics(unittest.TestCase):
    def setUp(self):
        self._backend = lnp.get_backend()

    def test_set_and_get_backend(self):
        """
        IF switched to a correct backend
        THEN create the backend is set and compute return type is correct.
        """
        np_input = np.random.randn(10, 3)

        # numpy backend
        lnp.set_backend("numpy")
        self.assertEqual(lnp.get_backend(), "numpy")
        np_out = lnp.sin(np_input)
        self.assertFalse(lnp.is_jax_array(np_out))

        # Test jax backend
        lnp.set_backend("jax")
        self.assertEqual(lnp.get_backend(), "jax")
        jax_out = lnp.sin(np_input)
        self.assertTrue(lnp.is_jax_array(jax_out))

        # casadi backend
        lnp.set_backend("casadi")
        self.assertEqual(lnp.get_backend(), "casadi")
        casadi_out = lnp.sin(SX(np_input))
        self.assertTrue(isinstance(casadi_out, SX))

    def tearDown(self):
        lnp.set_backend(self._backend)


class TestUtils(unittest.TestCase):
    def setUp(self):
        self._backend = lnp.get_backend()

    def test_is_jax_array(self):
        np_array = np.zeros((10, 3))
        self.assertFalse(lnp.is_jax_array(np_array))
        self.assertFalse(lnp.is_jax_array(SX(np_array)))
        self.assertTrue(lnp.is_jax_array(jnp.array(np_array)))

    def test_vector_concat(self):
        num_arrays, array_size = 5, 10
        expected_vector_size = num_arrays * array_size
        np_arrays = [np.random.randn(array_size) for _ in range(num_arrays)]
        casadi_arrays = [SX(a) for a in np_arrays]
        jax_arrays = [jnp.array(a) for a in np_arrays]

        lnp.set_backend("jax")
        self.assertEqual(lnp.vector_concat(jax_arrays).shape, (expected_vector_size,))

        lnp.set_backend("numpy")
        self.assertEqual(lnp.vector_concat(np_arrays).shape, (expected_vector_size,))

        # Casadi uses column vectors!
        lnp.set_backend("casadi")
        self.assertEqual(
            lnp.vector_concat(casadi_arrays).shape, (expected_vector_size, 1)
        )

    def test_lmap_with_arrays(self):
        """lmap should work with array outputs, with different in_axes mapping"""

        def fn(a, b):
            return a + b

        # Mapping all inputs
        a_array, b_array = np.ones(10), np.ones(10) * 2
        c_array = lnp.lmap(fn)(a_array, b_array)
        np.testing.assert_allclose(c_array, a_array + b_array)

        # Without mapping the last input
        a_array, b = np.ones(10), 2
        c_array = lnp.lmap(fn, in_axes=[0, None])(a_array, b)
        np.testing.assert_allclose(c_array, a_array + b)

    def test_lmap_with_tuples(self):
        """lmap should work with tuple or namedtuple outputs, with different in_axes mapping"""

        def fn(a, b):
            return a + b, a - b

        # Mapping all inputs
        a_array, b_array = np.ones(10), np.ones(10) * 2
        output = lnp.lmap(fn)(a_array, b_array)
        np.testing.assert_allclose(output, (a_array + b_array, a_array - b_array))

        # Without mapping the last input
        a_array, b = np.ones(10), 2
        actual = lnp.lmap(fn, in_axes=[0, None])(a_array, b)
        expected = (a_array + b, a_array - b)

        for act, exp in zip(actual, expected):
            np.testing.assert_allclose(act, exp)

    def tearDown(self):
        lnp.set_backend(self._backend)


if __name__ == "__name__":
    unittest.main()
