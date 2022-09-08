import logging
from typing import Any, Dict, Tuple

import numpy as np

from lumos.models.base import StateSpaceModel
from lumos.optimal_control.nlp import (
    LinearConstraints,
    BaseObjective,
)
from lumos.optimal_control.scaled_mesh_ocp import ScaledMeshOCP


logger = logging.getLogger(__name__)


class FixedMeshOCP(ScaledMeshOCP):
    """Optimal Control problem where the mesh is fixed"""

    # No Global variables
    global_var_names: Tuple[str] = ()

    def __init__(
        self,
        model: StateSpaceModel,
        sim_config: Dict[str, Any] = None,
        mesh_scale: float = 1.0,
    ):

        # NOTE: we choose to make mesh_scale a variable instead of a config to make the
        # distinction of fixed_grid clearer!
        assert mesh_scale > 0.0, "mesh_scale must be a positive scalar!"
        self.set_mesh_scale(mesh_scale)

        super().__init__(model=model, sim_config=sim_config)

    def set_mesh_scale(self, mesh_scale: float):
        """When we set the mesh_scale, some other properties must change"""

        # Currently we don't need to update anything else, but in the future we might.
        self._mesh_scale = mesh_scale

    def _get_mesh_scale(self, x):
        """Overwrite parent method since the mesh scale is now fixed."""
        return self._mesh_scale

    def get_mesh(self):
        """Helper method for FixedMesh as we don't need any input to get the mesh."""
        return self.get_mesh_from_scale(self._mesh_scale)

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
        """Overwrite base class to create linear constraints for continiuty.

        Since for fixed grid, the continuity is just a linear constraint.

        However here we do not cache the jacobian, because when the jacobian value is
        cached, then if the problem changes (for example, when the mesh_scale changes), this continuity jacobian is no
        longer valid!

        The performance cost is < 1ms per call for 250 intervals with 3 stages per
        interval, so pretty much negligible for any problem with a non-trivial model.
        """

        continuity_cons = LinearConstraints(
            constraints=self._continuity_constraints,
            num_in=self.num_dec,
            num_con=self.num_continuity_cons,
            jacobian=self._continuity_jacobian,
            jacobian_structure=self._continuity_jacobianstructure(),
            cache_jacobian=False,
        )

        self.add_constraints("continuity", continuity_cons)

    def _build_objective(self):
        # Common objective regardless of the problem
        time_objective = BaseObjective(
            num_in=self.num_dec,
            objective=lambda x: self._time_objective(x),
            gradient=lambda x: self._time_gradient(x),
            hessian=lambda x: np.array([]),
            hessian_structure=(
                np.array([], dtype=np.int32),
                np.array([], dtype=np.int32),
            ),
        )
        self.add_objective("time", time_objective)
