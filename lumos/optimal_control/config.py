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
    """Simulation Configuraration for Optimal Control
    
    This class is inheritted from dataclass, as such any customization to it need to be
    done in __post_init__

    required fields are:
        num_intervals (int): number of intervals for the OCP, default to 99.
        interval_points (Optional[np.ndarray]): when given, uses custon interval points
            to set up the normalized_mesh. The points must be in [0, 1] and covers both
            end points. They must also be monotonically increasing, and have a size of
            num_intervals + 1. Default to None, which uses uniform intervals. See also:
            ScaledMeshOCP.set_normalized_mesh
        transcription (str, Tuple[str, Dict[str, Any]]): the transcription method to use
        can be either a single string, and must be one of the following:
        ["ForwardEuler", "Trapezoidal", "LGR", "LGRIntegral"]. Optionally, one can pass
        in additional parameter, for example, 'num_stages' for LGR, which defines number
        of stages used in collocation. So all of the following are valid:
        - transcription="ForwardEuler" (use ForwardEuler, no configurable parameters)
        - transcirption="LGR" (use LGR, with default 3 stages per interval)
        - transcription = ("LGR", {"num_stages": 5}) (use LGR, with custom parameter of
            5 stages per interval)
        is_cyclic [bool]: true will set the problem as cyclic, default to False.
        non_cyclic_vars [List[str]]: when the problem is cyclic, the variables that can
            still be non-cyclic, default to empty.
        is_condensed [bool]: if True, will condense the problem to remove "states_dot"
            from decision variables, which would reduce IPOPT solve overhead, with
            potential cost on function call overhead and convergence. Default to False.
        backend [str]: numerical backend to use, must be "jax", "casadi" or "cuistom".
            if custom, the user must provide the derivatives calls
            (see examples/brachistochrone.py). Default to "jax"
        hessian_approximation [str]: "limited-memory" or "exact", default to "exact"
        boundary_conditions [Tuple[BoundaryConditionConfig]]: tuple of boundary cond
            configurations. Default to empty
        bounds [Tuple[BoundConfig]]: bounds all on variables, default to empty.
        scales [Tuple[ScaleConfig]]: custom scaling for all variables, defaul to empty,
            which uses a scale of 1
        con_output_names [Tuple[str]]: names of the outputs to be added to the dec vars,
            so that we can add bounds on them to constrain them.
        logging_config [Optional[LoggingConfig]]: logging configuration, default to None.

    """

    num_intervals: int = 99
    interval_points: Optional[np.ndarray] = None
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
