import logging
import unittest
from typing import Dict

import numpy as np

from lumos.models.tires.perantoni import PerantoniTire
from lumos.models.test_utils import BaseModelTest

logger = logging.getLogger(__name__)


class TestPerantoniTire(BaseModelTest, unittest.TestCase):
    ModelClass: type = PerantoniTire

    def _get_fx_from_kappa(self, kappa: float, input_dict: Dict[str, float]) -> float:
        """Helper to perform longitudinal sweep"""
        input_dict["kappa"] = kappa
        inputs = self.model.make_vector(group="inputs", **input_dict)
        outputs, *_ = self.model.forward(inputs=inputs)

        return self.model.get_output(outputs, "Fx")

    def _get_fy_from_alpha(self, alpha: float, input_dict: Dict[str, float]) -> float:
        input_dict["alpha"] = alpha
        inputs = self.model.make_vector(group="inputs", **input_dict)
        outputs, *_ = self.model.forward(inputs=inputs)

        return self.model.get_output(outputs, "Fy")

    def test_pure_longitudinal(self):
        """Test characteristics in pure longitudinal load

        WHEN: load is pure longitudinal
        THEN: zero force at zero slip
            and force is monotonically increasing between the peaks
        """
        vx = 10.0
        input_dict = {
            "Fz": 2000.0,
            "kappa": 0.0,
            "alpha": 0.0,
            "vx": vx,
            "gamma": 0.0,
        }

        # No force at zero slip
        fx0 = self._get_fx_from_kappa(0.0, input_dict=input_dict)
        self.assertAlmostEqual(fx0, 0, msg="Longitudinal Force non-zero at 0 slip")

        # Longitudianl force and slip are the same sign
        # Ensure the force is monotonically increasing between the -ve and +ve peaks
        kappa_sweep = np.linspace(-0.3, 0.3, 101)
        fx_sweep = np.array(
            [self._get_fx_from_kappa(k, input_dict=input_dict) for k in kappa_sweep]
        )
        idx_min = np.argmin(fx_sweep)
        idx_max = np.argmax(fx_sweep)
        fx_should_be_monotonic = fx_sweep[idx_min : idx_max + 1]
        self.assertGreater(len(fx_should_be_monotonic), 0)
        self.assertTrue(
            np.all(np.diff(fx_should_be_monotonic) > 0),
            msg="Longitudinal force should be monotonically increasing between the two peaks",
        )

    def test_pure_lateral(self):
        """Test characteristics in pure lateral load

        WHEN: load is pure lateral
        THEN: zero force at zero slip
            and force is monotonically increasing between the peaks
        """
        vx = 10.0
        input_dict = {
            "Fz": 2000.0,
            "kappa": 0.0,
            "alpha": 0.0,
            "vx": vx,
            "gamma": 0.0,
        }

        # No force at zero slip
        fy0 = self._get_fy_from_alpha(0.0, input_dict=input_dict)
        self.assertAlmostEqual(fy0, 0, msg="Lateral Force non-zero at 0 slip")

        # lateral slip and force are opposite signs
        # Ensure the force is monotonically decreasing between the -ve and +ve peaks
        alpha_sweep = np.linspace(-0.3, 0.3, 101)
        fy_sweep = np.array(
            [self._get_fy_from_alpha(a, input_dict=input_dict) for a in alpha_sweep]
        )
        idx_min = np.argmin(fy_sweep)
        idx_max = np.argmax(fy_sweep)
        fy_should_be_monotonic = fy_sweep[idx_max : idx_min + 1]
        # Must also ensure the array is not empty!
        self.assertGreater(len(fy_should_be_monotonic), 0)
        self.assertTrue(
            np.all(np.diff(fy_should_be_monotonic) < 0),
            msg="Lateral force should be monotonically decreasing between the two peaks",
        )

    def test_combined(self):
        """Test combined load characteristics
        WHEN combined slip is introduced
        THEN longitudinal force in combined is smaller than in pure
            and lateral force in combined is smaller than in pure
        """
        vx = 10.0
        base_input_dict = {
            "Fz": 2000.0,
            "kappa": 0.0,
            "alpha": 0.0,
            "vx": vx,
            "gamma": 0.0,
        }

        # check pure longitudinal load is larger than that in combined.
        kappa = 0.02
        alpha_sweep = np.linspace(-0.3, 0.3, 20)
        input_dict = base_input_dict.copy()
        fx_in_pure = self._get_fx_from_kappa(kappa, input_dict)
        fx_in_combined = np.array(
            [
                self._get_fx_from_kappa(kappa, dict(input_dict, alpha=alpha))
                for alpha in alpha_sweep
            ]
        )
        self.assertTrue(
            np.all((fx_in_pure - fx_in_combined) >= 0),
            "Longitudinal load should be greater in pure longitudinal load than combined.",
        )

        # check pure lateral load magnitude is larger than that in combined.
        # For positive slip, this means the force is smaller (more negative)
        alpha = 0.02
        kappa_sweep = np.linspace(-0.3, 0.3, 20)
        input_dict = base_input_dict.copy()
        fy_in_pure = self._get_fy_from_alpha(alpha, input_dict)
        fy_in_combined = np.array(
            [
                self._get_fy_from_alpha(alpha, dict(input_dict, kappa=kappa))
                for kappa in kappa_sweep
            ]
        )
        self.assertTrue(
            np.all((fy_in_pure - fy_in_combined) <= 0),
            "Lateral load should be greater in pure lateral load than combined.",
        )


if __name__ == "__name__":
    unittest.main()
