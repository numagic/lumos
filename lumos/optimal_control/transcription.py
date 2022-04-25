from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple

import numpy as np
from scipy.sparse import diags

import lumos.numpy as lnp

from lumos.optimal_control.collocation import (
    build_lagrange_differential_matrix,
    build_lagrange_integration_matrix,
    CollocationEnum,
    get_collocation_points,
)


class Transcription(ABC):
    """Transcription method turning a continuous time problem into a discrete one.


    # TODO: should we eturn this into A*x + B*x_dot to make it more conventional?
    It constructs the linear continuity constraints: A*x - B*x_dot*T = 0

    assuming an m-stage interval, and d states


    A and B are both [m-1, m], while x and x_dot are both [m, d]. (m-stage interval, d
    states) T is a constant of the interval time. This is natural for integration scheme
    , but for differential schemes usually the interval time is combined with A in the
    form of 1/T.
    
    We unify it here to:
    - make the interface consistent for differential and integration schcheme
    - ensure the continuity constraint is in the order of the states instead of swtching
    between states and state derivatives.
    """

    num_stages_per_interval: int
    num_constraints_per_interval: int

    @property
    def _cont_matrix_shape(self) -> Tuple[int, int]:
        return self.num_constraints_per_interval, self.num_stages_per_interval

    def get_continuity_matrices(self) -> Tuple[np.ndarray, np.ndarray]:
        return self._get_A_matrix(), self._get_B_matrix()

    def continuity_con(
        self, x: lnp.ndarray, x_dot: lnp.ndarray, interval_length: float
    ) -> lnp.ndarray:
        A, B = self.get_continuity_matrices()
        continuity_con = A @ x - B @ x_dot * interval_length

        return continuity_con

    @abstractmethod
    def _get_A_matrix(self) -> np.ndarray:
        pass

    @abstractmethod
    def _get_B_matrix(self) -> np.ndarray:
        pass


class ForwardEuler(Transcription):
    """x_{i+1} - x_{i} - x_dot_{i}*dt = 0"""

    num_stages_per_interval: int = 2
    num_constraints_per_interval: int = 1

    def _get_A_matrix(self):
        return diags([-1, 1], [0, 1], shape=self._cont_matrix_shape).toarray()

    def _get_B_matrix(self):
        return diags([1], [0], shape=self._cont_matrix_shape).toarray()


class Trapezoidal(Transcription):
    """x_{i+1} - x_{i} - (x_dot_{i+1} + x_dot_{i}) * dt/2 = 0"""

    num_stages_per_interval: int = 2
    num_constraints_per_interval: int = 1

    def _get_A_matrix(self):
        return diags([-1, 1], [0, 1], shape=self._cont_matrix_shape).toarray()

    def _get_B_matrix(self):
        return diags([0.5, 0.5], [0, 1], shape=self._cont_matrix_shape).toarray()


class Collocation(Transcription):
    """Transcription with Legendre collocation

    Interval of collocation is converted to [0, 1] from the standard of [-1, 1] to make
    downstream computations easier.

    More details, refer to: AN OVERVIEW OF THREE PSEUDOSPECTRAL METHODS FOR THE
    NUMERICAL SOLUTION OF OPTIMAL CONTROL PROBLEMS
    https://hal.archives-ouvertes.fr/hal-01615132/document

    """

    interp_points: np.ndarray
    collocation_points: np.ndarray

    def __init__(self, num_stages: int):
        self.num_stages_per_interval: int = num_stages

        self._set_collocation_points(num_stages)
        self._set_interp_points()

        self.d_matrix: np.ndarray = build_lagrange_differential_matrix(
            support=self.interp_points, evaluation_points=self.collocation_points
        )

    @property
    def num_constraints_per_interval(self):
        return len(self.collocation_points)

    @abstractmethod
    def _set_collocation_points(self, num_stages: int) -> None:
        pass

    @abstractmethod
    def _set_interp_points(self) -> None:
        pass

    def _get_A_matrix(self) -> np.ndarray:
        # multiply by two because collocation is in the domain of [-1, 1],
        # so to map to [0, 1] (easy to scale to interval time), we first need to multiply
        # by two.
        return self.d_matrix

    def _get_B_matrix(self) -> np.ndarray:
        return diags([1], [1], shape=self._cont_matrix_shape).toarray()


class LGR(Collocation):
    """Transcription with LGR collocation"""

    def __init__(self, num_stages: int = 3):
        super().__init__(num_stages=num_stages)

    def _set_collocation_points(self, num_stages: int) -> None:
        # map collocation points from [-1, 1] to [0, 1]
        self.collocation_points = (
            get_collocation_points(
                num_points=num_stages - 1, scheme=CollocationEnum.LGR
            )
            + 1
        ) / 2

    def _set_interp_points(self) -> None:
        # Add the 0 to the interp_points
        self.interp_points = np.insert(self.collocation_points, 0, 0)


class LGRIntegral(LGR):
    """Integral variant of the LGR scheme"""

    def __init__(self, num_stages: int = 3):
        super().__init__(num_stages=num_stages)

        # Now we fit the polynomial on the derivatives (so on collocaiton points)
        # And then evaluate the ingral at the interpretation points (except for the 1st
        # point)
        self.i_matrix = build_lagrange_integration_matrix(
            support=self.interp_points, evaluation_points=self.collocation_points,
        )

    def _get_A_matrix(self) -> np.ndarray:
        return np.hstack(
            [
                -np.ones((self.num_stages_per_interval - 1, 1)),
                np.eye(self.num_stages_per_interval - 1),
            ]
        )

    def _get_B_matrix(self) -> np.ndarray:
        return self.i_matrix


TRANSCRIPTION_OPTIONS = {
    t.__name__: t for t in (ForwardEuler, Trapezoidal, LGR, LGRIntegral)
}


def get_transcription_options() -> List[str]:
    """Return names of available transcription classes.

    Returns:
        List[str]: a list of names of the available Transcription classes.
    """
    return [n for n in TRANSCRIPTION_OPTIONS.keys()]


def make_transcription(name: str, kwargs: Dict[str, Any] = None) -> Transcription:
    """Create a Transcription object from name and keyword arguments.

    Args:
        name (str): name of the transcription class.
        kwargs (Dict[str, Any], optional): additional kwargs to be passed to the
        transcription constructtor. Defaults to None, which will be set to empty.

    Raises:
        RuntimeError: if the transcription required is not a valid option.

    Returns:
        Transcription: Transcription object that defines a descritization scheme.
    """
    if not kwargs:
        kwargs = {}

    if name in TRANSCRIPTION_OPTIONS:
        return TRANSCRIPTION_OPTIONS[name](**kwargs)
    else:
        raise RuntimeError(
            "name is not a valid transcription type. "
            f"Valid options are {get_transcription_options()}"
        )
