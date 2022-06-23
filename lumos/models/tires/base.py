from abc import abstractmethod
from typing import Any, Dict, Optional, Tuple

import lumos.numpy as lnp
from lumos.models.base import Model, ModelReturn


class BaseTire(Model):
    """Abstract description of a tire model.

    Args:
        params (Dict[str, Any], optional): Tire model parameters. Defaults to None.
        model_config (Dict[str, Any], optional): Model configuration data. Defaults to None.
    """

    def __init__(self, params: Dict[str, Any] = {}, model_config: Dict[str, Any] = {}):
        super().__init__(model_config=model_config, params=params)

    @abstractmethod
    def forward(
        self,
        inputs: Dict[str, float],
        params: Optional[Dict[str, Any]] = None,
    ) -> ModelReturn:
        """Common tire model interface.

        The ISO sign convention is used, see page 29 of
        https://functionbay.com/documentation/onlinehelp/Documents/Tire/MFTyre-MFSwift_Help.pdf

        Args:
            inputs (lnp.ndarray): The inputs to the model.
                gamma:       camber angle of the tire [rad]
                vx:       long. wheel centre velocity in the tire coordinate frame [m/s]
                alpha:       slip angle [rad] Opposite sign as force.
                kappa:      slip ratio [-] Same sign as force
                Fz:         normal load on the tire [N]
            params (Optional[Dict[str, Any]], optional): Defaults to None.
                Overwrite model parameters with user specified ones. If not
                provided, the parameters in the model attribute will be used.
        Returns:
            ModelReturn: with the 'outputs' field a vector containing:
                Fx:         long. tire force [N]
                Fy:         lat. tire force [N]
                Mx:         overturning moment [Nm]
                My:         rolling resistance moment [Nm]
                Mz:         self-aligning moment [Nm]
        """
        pass
