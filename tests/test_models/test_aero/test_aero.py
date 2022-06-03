import logging
import unittest

import numpy as np

from lumos.models.aero.aero import ConstAero, GPAero, MLPAero
from lumos.models.test_utils import BaseModelTest

logger = logging.getLogger(__name__)


class TestConstAero(BaseModelTest, unittest.TestCase):
    ModelClass: type = ConstAero

    def test_outputs_are_correct(self):
        inputs = dict(
            zip(self.model.names.inputs, self.model.make_random_vector("inputs"))
        )
        model_return = self.model.forward(inputs)

        # Check constant values are the same as in the params
        for k, v in model_return.outputs.items():
            self.assertAlmostEqual(v, self.model._params[k])


class TestGPAero(BaseModelTest, unittest.TestCase):
    ModelClass: type = GPAero


class TestMLPAero(BaseModelTest, unittest.TestCase):
    ModelClass: type = MLPAero


if __name__ == "__name__":
    unittest.main()
