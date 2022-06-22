import numpy as np
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Union


@dataclass
class BoundConfig:
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
class ScaleConfig:
    """Config for the scale on variables
    
    TODO: check all values are postiive!
    """

    group: str
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
class LoggingConfig:
    """Controls if and where the results as well as debug info are written to"""

    sim_name: str = "simulation"
    results_dir: str = "results"
    log_every_nth_iter: int = 0


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
    bounds: Tuple[BoundConfig] = ()
    scales: Tuple[ScaleConfig] = ()
    con_output_names: Tuple[str] = ()
    logging_config: Optional[LoggingConfig] = None

    def __post_init__(self):
        # We allow a single string argument (with no additional arugments or relying on
        # default arguments) for transcription definition, eg "LGR", ("LGR", ) and
        # ("LGR", {"num_stages": 3}}) are all valid
        # It almost feels like that the SimConfig needs to be a tree as well, where
        # transcription can have its own config.
        if isinstance(self.transcription, str):
            self.transcription = (self.transcription,)

        # Additional operations for desrialization for config fields
        if self.bounds and isinstance(self.bounds[0], dict):
            self.bounds = tuple(BoundConfig(**d) for d in self.bounds)

        if self.scales and isinstance(self.scales[0], dict):
            self.scales = tuple(ScaleConfig(**d) for d in self.scales)

        if self.boundary_conditions and isinstance(self.boundary_conditions[0], dict):
            self.boundary_conditions = tuple(
                BoundaryConditionConfig(**d) for d in self.boundary_conditions
            )

    def to_dict(self) -> Dict[str, Any]:
        """Convert a nested config to a dictionary."""
        return asdict(self)
