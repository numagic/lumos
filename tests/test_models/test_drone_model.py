import logging
import os
import unittest
from parameterized import parameterized, parameterized_class

from lumos.models.drone_model import DroneModel
from lumos.models.test_utils import BaseStateSpaceModelTest

logger = logging.getLogger(__name__)


class TestDroneModel(BaseStateSpaceModelTest, unittest.TestCase):
    ModelClass: type = DroneModel


if __name__ == "__name__":
    unittest.main()
