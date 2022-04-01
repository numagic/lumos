import logging
from typing import Any, Dict

import numpy as np

from lumos.models.base import StateSpaceModel
from lumos.optimal_control.nlp import (
    LinearConstraints,
    BaseObjective,
)
from lumos.optimal_control.scaled_mesh_ocp import ScaledMeshOCP


logger = logging.getLogger(__name__)


class FixedMeshOCP(ScaledMeshOCP):
    """Laptime simulation type of problem
    - fixed grid
    - distance grid instead of time

    TODO: we could consider the following solutoin:
    - a fixed mesh problem is just like a scaled_mesh_ocp, but with the bounds on the
    mesh_scale varaible fixed.
    - of course we would waste some computes as we have to compute more derivatives etc
    for which we know actually would just be sparse (or actually not sparse but the
    corresponding decision variable has no freedom.)
    """

    # No Global variables
    global_var_names = []

    def __init__(
        self,
        model: StateSpaceModel,
        sim_config: Dict[str, Any] = None,
        mesh_scale: float = 1.0,
    ):

        # NOTE: we choose to make mesh_scale a variable instead of a config to make the
        # distinction of fixed_grid clearer!
        assert mesh_scale > 0.0, "mesh_scale must be a positive scalar!"
        self._mesh_scale = mesh_scale

        super().__init__(model=model, sim_config=sim_config)

    def _get_mesh_scale(self, x):
        return self._mesh_scale

    def _time_objective(self, x):
        idx_end = self.dec_var_operator.get_var_index_in_dec(
            group="states", name="time", stage=-1
        )

        idx_start = self.dec_var_operator.get_var_index_in_dec(
            group="states", name="time", stage=0
        )
        return x[idx_end] - x[idx_start]

    def _time_gradient(self, x):
        idx_end = self.dec_var_operator.get_var_index_in_dec(
            group="states", name="time", stage=-1
        )

        idx_start = self.dec_var_operator.get_var_index_in_dec(
            group="states", name="time", stage=0
        )
        grad = np.zeros_like(x)
        grad[idx_end] = 1
        grad[idx_start] = -1
        return grad

    def _build_continuity_cons(self):
        # Since for fixed grid, the continuity is just a linear constraint, we don't
        # actually need an input to get the jacobian. But we pass in one dummy here to
        # adhere to the signature of the parent method
        # NOTE: since the jacobian value is cached, then if the problem changes
        # (for example, when the mesh_scale changes), this continuity jacobian is no
        # longer valid!
        continuity_cons = LinearConstraints(
            constraints=self._continuity_constraints,
            num_in=self.num_dec,
            num_con=self.num_total_con_interval,
            jacobian_value=self._continuity_jacobian(np.ones(self.num_dec)),
            jacobian_structure=self._continuity_jacobianstructure(),
        )

        self.add_constraints("continuity", continuity_cons)

    def _build_objective(self):
        # Common objective regardless of the problem
        time_objective = BaseObjective(
            objective=lambda x: self._time_objective(x),
            gradient=lambda x: self._time_gradient(x),
            hessian=lambda x: np.array([]),
            hessian_structure=(np.array([]), np.array([])),
        )
        self.add_objective("time", time_objective)