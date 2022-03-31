import logging
import os
from abc import abstractmethod
from typing import Any, Dict

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class Track:
    @abstractmethod
    def heading_at(self, s: float) -> float:
        """Heading function"""
        pass

    @abstractmethod
    def curvature_at(self, s: float) -> float:
        pass

    @abstractmethod
    def left_distance_at(self, s: float) -> float:
        """Distance to left bound."""
        pass

    @abstractmethod
    def right_distance_at(self, s: float) -> float:
        """Distance to right bound."""
        pass


def _trapz(y, x):
    dx = np.diff(x)
    deltas = (y[:-1] + y[1:]) / 2 * dx
    return np.cumsum(np.insert(deltas, 0, 0.0))


def cartesian_to_curvilinear(x, y):
    ds = np.sqrt(np.diff(x) ** 2 + np.diff(y) ** 2)
    s = np.cumsum(np.insert(ds, 0, 0.0))

    # first derivative
    dx = np.gradient(x, s)
    dy = np.gradient(y, s)

    # second derivatives
    d2x = np.gradient(dx, s)
    d2y = np.gradient(dy, s)

    # calculation of curvature from the typical formula
    curvature = (dx * d2y - d2x * dy) / (dx * dx + dy * dy) ** 1.5

    initial_heading = np.arctan2(dy[0], dx[0])
    heading = _trapz(curvature, s) + initial_heading
    return s, curvature, heading


def curvilinear_to_cartesian(
    s, curvature, x0: float = 0, y0: float = 0, heading0: float = 0
):
    heading = _trapz(curvature, s) + heading0
    x = _trapz(np.cos(heading), s) + x0
    y = _trapz(np.sin(heading), s) + y0

    return x, y, heading


class RaceTrack(Track):
    def __init__(
        self,
        x: np.ndarray,
        y: np.ndarray,
        s: np.ndarray,
        curvature: np.ndarray,
        heading: np.ndarray,
        left_distance: np.ndarray = None,
        right_distance: np.ndarray = None,
    ):
        # Create constant distance to the sides if unspecified
        # FIXME: 5m is arbitrary, should we make these values compulsory?
        if left_distance is None:
            left_distance = np.ones_like(s) * 5
        if right_distance is None:
            right_distance = np.ones_like(s) * 5

        # Check if the left distance and right distance are incompatible with what the
        # curvature allows.
        # if curvature * distance from centerline > 1 -> the boundary will fold on itself.
        # this is valid for both +ve and -ve distance from centerline
        # NOTE: we just check, but don't do any modifications yet.
        b_violate_left = curvature * left_distance > 1
        b_violate_right = curvature * -right_distance > 1

        logger.info(f"left distance violation: {np.sum(b_violate_left)}")
        logger.info(f"right distance violation: {np.sum(b_violate_right)}")

        self._track_data = {
            "s": s,
            "curvature": curvature,
            "heading": heading,
            "x": x,
            "y": y,
            "left_distance": left_distance,
            "right_distance": right_distance,
        }

        # Offset distance to always start at 0
        self._track_data["s"] = self._track_data["s"] - self._track_data["s"][0]

    @staticmethod
    def from_cartesian(x, y, left_distance=None, right_distance=None):
        s, curvature, heading = cartesian_to_curvilinear(x, y)
        return RaceTrack(
            x=x,
            y=y,
            s=s,
            curvature=curvature,
            heading=heading,
            left_distance=left_distance,
            right_distance=right_distance,
        )

    @staticmethod
    def from_curvilinear(
        s, curvature, heading0=0, left_distance=None, right_distance=None
    ):
        x, y, heading = curvilinear_to_cartesian(s, curvature, heading0=heading0)
        return RaceTrack(
            x=x,
            y=y,
            s=s,
            curvature=curvature,
            heading=heading,
            left_distance=left_distance,
            right_distance=right_distance,
        )

    @staticmethod
    def from_tum_csv(track_file):
        """Create track from TUM track data format

        see:https://github.com/TUMFTM/racetrack-database
        """
        df = pd.read_csv(track_file)
        return RaceTrack.from_cartesian(
            x=df["# x_m"],
            y=df["y_m"],
            left_distance=df["w_tr_left_m"],
            right_distance=df["w_tr_right_m"],
        )

    def curvature_at(self, s: float) -> float:
        """Return the curvature of the track at given distance"""
        return np.interp(s, self._track_data["s"], self._track_data["curvature"])

    def heading_at(self, s: float) -> float:
        """Return the heading angle of the track at given distance"""
        return np.interp(s, self._track_data["s"], self._track_data["heading"])

    def left_distance_at(self, s: float) -> float:
        """Constant halfwidth for now"""
        return np.interp(s, self._track_data["s"], self._track_data["left_distance"])

    def right_distance_at(self, s: float) -> float:
        """Constant halfwidth for now"""
        return np.interp(s, self._track_data["s"], self._track_data["right_distance"])

    @property
    def total_distance(self):
        return self._track_data["s"][-1]


class ConstCurvTrack(Track):
    _curvature: float
    _start_heading: float

    def __init__(
        self, curvature: float = 0.01, start_heading: float = 0.0, half_width: float = 2
    ):
        self._curvature = curvature
        self._start_heading = start_heading
        self._half_wdith = half_width

    def heading_at(self, s: float) -> float:
        """Heading function

        dtheta/ds = k

        For constant k
        theta = start_heading + k*s

        """
        return self._start_heading + self._curvature * s

    def curvature_at(self, s: float) -> float:
        return self._curvature

    def half_width_at(self, s: float) -> float:
        """Constant halfwidth for now"""
        return self._half_wdith
