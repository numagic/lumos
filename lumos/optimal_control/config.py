import numpy as np
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Union


@dataclass
class BoundConfig:
    """Config for variable bounds.
    
    Mainly used for two purposes:
    - typehint to cover all children classes
    - factory function to create subclass from staticmethod
    """

    @staticmethod
    def from_dict(input_dict):
        # FIXME: this is an ugly workaround, using number of inputs to determine type
        if len(input_dict) == 2:
            return GlobalVarBoundConfig(**input_dict)
        elif len(input_dict) == 3:
            return StageVarBoundConfig(**input_dict)
        else:
            raise ValueError(
                "input dict should either be from GlobalVarBoundConfig or StageVarBoundConfig"
            )


@dataclass
class StageVarBoundConfig(BoundConfig):
    """Config for the bounds on a stage variable
    
    The bound values must be a tuple of floats or a tuple of 1d numpy arrays. The upper
    bounds must be greater than or equal to the lower bounds.
    """

    group: str
    name: str
    values: Union[Tuple[float, float], Tuple[np.ndarray, np.ndarray]]

    def __post_init__(self):
        """Perform checks on bounds.
        
        1) bounds should be both scalars or both 1d np.ndarray
        2) upper bounds should be larger than or equal to lower bounds.
        """
        lb, ub = self.values

        pretext = f"Failed to set bounds for {self.group}:{self.name}. "
        if np.isscalar(lb) and np.isscalar(ub):
            assert ub >= lb, pretext + "lower bounds larger than upper bounds"
        elif isinstance(lb, np.ndarray) and isinstance(ub, np.ndarray):
            assert lb.ndim == 1 and ub.ndim == 1, pretext + "Bound arrays must be 1d."
            assert len(lb) == len(ub), pretext + "Bound arrays must have the same size."
            assert np.all(ub >= lb), (
                pretext
                + f"lower bounds larger than upper bounds at stage {np.where(lb > ub)}"
            )

        else:
            raise TypeError(
                pretext + "lower and upper bounds must be both scalars or "
                "both 1d numpy arrays of the same size."
            )


@dataclass
class GlobalVarBoundConfig(BoundConfig):
    """Config for the bounds on global variables.
    
    The bound values must be a tuple of floats, where the upper bound is larger than or
    equal to the lower bound.
    """

    name: str
    values: Tuple[float, float]

    def __post_init__(self):
        """Perform checks on bounds.
        
        1) bounds should be both scalars.
        2) upper bound should be larger than or equal to lower bound.
        """
        lb, ub = self.values

        pretext = f"Failed to set bounds for {self.name}. "
        if np.isscalar(lb) and np.isscalar(ub):
            assert ub >= lb, pretext + "lower bounds larger than upper bounds"
        else:
            raise TypeError(
                pretext + "lower and upper bounds must be both scalars or "
                "both 1d numpy arrays of the same size."
            )


@dataclass
class ScaleConfig:
    """Config for setting the scaling of constraints and decisvariables.

    TODO: The design follows BoundConfig closely. Maybe we can unite them? Key diffs:
    - Scales are only scalars, not tuples, and never vectors (so the scales for all
    stages are the same.)

    """

    @staticmethod
    def from_dict(input_dict):
        # FIXME: this is an ugly workaround, using number of inputs to determine type
        if len(input_dict) == 2:
            return GlobalVarScaleConfig(**input_dict)
        elif len(input_dict) == 3:
            return StageVarScaleConfig(**input_dict)
        else:
            raise ValueError(
                "input dict should either be from GlobalVarScaleConfig or StageVarScaleConfig"
            )


@dataclass
class StageVarScaleConfig(BoundConfig):
    """Config for the scale on a stage variable
    
    TODO: check all values are postiive!
    """

    group: str
    name: str
    value: float


@dataclass
class GlobalVarScaleConfig(BoundConfig):
    """Config for the scale on global variables."""

    name: str
    value: float


@dataclass
class BoundaryConditionConfig:
    """Boundary condition config to constraint a stage variable to a given value."""

    stage: int
    group: str
    name: str
    value: float


@dataclass
class TranscriptionConfig:
    pass


@dataclass
class SimConfig:
    """Simulation Configuraration for Optimal Control"""

    num_intervals: int = 99
    transcription: Union[str, Tuple[str, Optional[Dict[str, Any]]]] = "Trapezoidal"
    is_cyclic: bool = False
    non_cyclic_vars: List[str] = field(default_factory=list)
    is_condensed: bool = False
    backend: str = "jax"
    hessian_approximation: str = "exact"
    boundary_conditions: Tuple[BoundaryConditionConfig] = ()
    bounds: Tuple[StageVarBoundConfig] = ()
    scales: Tuple[ScaleConfig] = ()
    logging_config: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        # We allow a single string argument (with no additional arugments or relying on
        # default arguments) for transcription definition, eg "LGR", ("LGR", ) and
        # ("LGR", {"num_stages": 3}}) are all valid
        # It almost feels like that the SimConfig needs to be a tree as well, where
        # transcription can have its own config.
        if isinstance(self.transcription, str):
            self.transcription = (self.transcription,)

        if not self.logging_config:
            self.logging_config = {
                "results_dir": "results",  # store in a new directory at current directory
                "sim_name": None,
                "log_final_iter": False,
                "log_metrics_history": False,
                "log_every_nth_iter": 0,
            }  # if 0, logging is off

        # Additional operations for desrialization for config fields
        if self.bounds and isinstance(self.bounds[0], dict):
            self.bounds = tuple(BoundConfig.from_dict(d) for d in self.bounds)

        if self.scales and isinstance(self.scales[0], dict):
            self.scales = tuple(ScaleConfig.from_dict(d) for d in self.scales)

        if self.boundary_conditions and isinstance(self.boundary_conditions[0], dict):
            self.boundary_conditions = tuple(
                BoundaryConditionConfig(**d) for d in self.boundary_conditions
            )

    def to_dict(self) -> Dict[str, Any]:
        """Convert a nested config to a dictionary."""
        return asdict(self)
