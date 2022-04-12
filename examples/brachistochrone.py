import logging
import numpy as np

from typing import Any, Dict
from scipy.optimize import newton


import lumos.numpy as lnp
from lumos.models.base import StateSpaceModel, StateSpaceModelReturn, state_space_io
from lumos.optimal_control.config import (
    BoundaryConditionConfig,
    BoundConfig,
)
from lumos.optimal_control.scaled_mesh_ocp import ScaledMeshOCP
from lumos.optimal_control.fixed_mesh_ocp import FixedMeshOCP

logger = logging.getLogger(__name__)


def cycloid(dx, dy, N=100, g=9.81):
    """Return the path of Brachistochrone curve from (0,0) to (x2, y2).

    The Brachistochrone curve is the path down which a bead will fall without
    friction between two points in the least time (an arc of a cycloid).
    It is returned as an array of N values of (x,y) between (0,0) and (x2,y2).


    taken from: https://scipython.com/blog/the-brachistochrone-problem/
    need to invert sign of y
    """

    # First find theta2 from (x2, y2) numerically (by Newton-Rapheson).
    def f(theta):
        return -dy / dx - (1 - np.cos(theta)) / (theta - np.sin(theta))

    theta2 = newton(f, np.pi / 2)

    # The radius of the circle generating the cycloid.
    R = -dy / (1 - np.cos(theta2))

    theta = np.linspace(0, theta2, N)
    x = R * (theta - np.sin(theta))
    y = R * (1 - np.cos(theta))

    # The time of travel
    T = theta2 * np.sqrt(R / g)
    print("T(cycloid) = {:.3f}".format(T))
    return x, -y, T


@state_space_io(states=("v", "x", "y"), inputs=("theta",), outputs=("theta",))
class TimeModel(StateSpaceModel):
    """The Brachistochrone model formulatd in the time domain"""

    def __init__(
        self, model_config: Dict[str, Any] = {}, params: Dict[str, Any] = {},
    ):
        super().__init__(model_config=model_config, params=params)

    def forward(
        self,
        states: lnp.ndarray,
        inputs: lnp.ndarray,
        mesh: float = 0.0,  # time invariant model
    ) -> StateSpaceModelReturn:
        params = self._params
        theta = self.get_input(inputs, "theta")
        v = self.get_state(states, "v")
        v_dot = -params["gravity"] * lnp.sin(theta)

        dx_dt = lnp.cos(theta) * v
        dy_dt = lnp.sin(theta) * v

        # Assemble result
        states_dot = self.make_vector(
            group="states_dot", v_dot=v_dot, x_dot=dx_dt, y_dot=dy_dt,
        )
        outputs = self.make_vector(group="outputs", theta=theta)
        return self.make_state_space_model_return(
            states_dot=states_dot, outputs=outputs
        )

    @classmethod
    def get_default_params(self) -> Dict[str, Any]:
        return {"gravity": 9.81}


class TimeModelWithCustomDerivatives(TimeModel):
    """The Brachistochrone model formulatd in the time domain, with custom derivatives."""

    def __init__(
        self, model_config: Dict[str, Any] = {}, params: Dict[str, Any] = {},
    ):
        super().__init__(model_config=model_config, params=params)

    def _implicit_jac(self, flat_vars, mesh, params):
        """Custom implementation of the implicit jacobian using numpy"""
        self.set_recursive_params(params)
        vars = self._split_flat_vars(flat_vars)

        # The derivatives the f(x, u) part of f(x, u) - x_dot = 0
        theta = self.get_input(vars["inputs"], "theta")
        v = self.get_state(vars["states"], "v")

        dvdot_dtheta = -self._params["gravity"] * np.cos(theta)
        ddxdt_dtheta = -np.sin(theta) * v
        ddxdt_dv = np.cos(theta)
        ddydt_dtheta = np.cos(theta) * v
        ddydt_dv = np.sin(theta)

        # vals and indices must align
        model_vals = np.array(
            [dvdot_dtheta, ddxdt_dtheta, ddxdt_dv, ddydt_dtheta, ddydt_dv]
        )

        # NOTE: it just happens that this model only has state_dot residual constraints,
        # so the constraint ordering is the same as the states
        # The derivatives the x_dot part of f(x, u) - x_dot = 0
        states_dot_vals = -np.ones(self.num_states)

        vals = np.concatenate([model_vals, states_dot_vals])
        return vals

    def _implicit_jacobianstructure(self):
        """Custom implementation of the implicit jacobian structure using numpy.

        The ordering of the indices must match those of the values (triplet form)
        """
        model_rows = np.array(
            [
                self.get_var_index(group="states", name="v"),
                self.get_var_index(group="states", name="x"),
                self.get_var_index(group="states", name="x"),
                self.get_var_index(group="states", name="y"),
                self.get_var_index(group="states", name="y"),
            ]
        )
        model_cols = np.array(
            [
                self.get_var_index_in_flat(group="inputs", name="theta"),
                self.get_var_index_in_flat(group="inputs", name="theta"),
                self.get_var_index_in_flat(group="states", name="v"),
                self.get_var_index_in_flat(group="inputs", name="theta"),
                self.get_var_index_in_flat(group="states", name="v"),
            ]
        )

        states_dot_rows = np.arange(self.num_states)
        states_dot_cols = np.array(
            [
                self.get_var_index_in_flat(group="states_dot", name=n)
                for n in self.get_group_names("states_dot")
            ]
        )

        rows = np.concatenate([model_rows, states_dot_rows])
        cols = np.concatenate([model_cols, states_dot_cols])
        return rows, cols

    def _implicit_hess(self, flat_vars, mesh, params, mult):
        """Custom implementation of the lagrangian hessian of the implicit constraints.

        Only states forward equation part has non-zero hessian
        """
        self.set_recursive_params(params)
        vars = self._split_flat_vars(flat_vars)

        theta = self.get_input(vars["inputs"], "theta")
        v = self.get_state(vars["states"], "v")

        d2vdot_dtheta2 = self._params["gravity"] * np.sin(theta)
        d2dxdt_dtheta2 = -np.cos(theta) * v
        d2dxdt_dtheta_dv = -np.sin(theta)
        d2dydt_dtheta2 = -np.sin(theta) * v
        d2dydt_dtheta_dv = np.cos(theta)

        # We only have dtheta_dv, dv_dtheta terms and dtheta_2 terms, and note that
        # d2dydt_dtheta_dv and d2dydt_dv_dtheta are the same!
        def _get_mult(state_name):
            """Get multiplier for state derivative residuals"""
            return mult[self.get_var_index(group="states", name=state_name)]

        d2l_dtheta2 = (
            d2vdot_dtheta2 * _get_mult("v")
            + d2dxdt_dtheta2 * _get_mult("x")
            + d2dydt_dtheta2 * _get_mult("y")
        )
        d2l_dtheta_dv = d2dxdt_dtheta_dv * _get_mult(
            "x"
        ) + d2dydt_dtheta_dv * _get_mult("y")

        # We pass in both the upper and lower triangular (symmetric) terms, so that we
        # don't have to compare indices and worry about which ones to keep here. The
        # upper triangular filtering will happen automatically downstream
        vals = np.array([d2l_dtheta2, d2l_dtheta_dv, d2l_dtheta_dv])
        return vals

    def _implicit_hessianstructure(self):
        """Custom implementation of the lagrangian hessian jacobian structure.

        The ordering of the indices must match those of the values (triplet form)
        """
        rows = np.array(
            [
                self.get_var_index_in_flat(group="inputs", name="theta"),
                self.get_var_index_in_flat(group="inputs", name="theta"),
                self.get_var_index_in_flat(group="states", name="v"),
            ]
        )
        cols = np.array(
            [
                self.get_var_index_in_flat(group="inputs", name="theta"),
                self.get_var_index_in_flat(group="states", name="v"),
                self.get_var_index_in_flat(group="inputs", name="theta"),
            ]
        )
        return rows, cols

    @classmethod
    def get_default_params(self) -> Dict[str, Any]:
        return {"gravity": 9.81}


# FIXME: for FixedMeshOCP, time obejctive requries states: time
@state_space_io(states=("time", "v", "y"), inputs=("theta",))
class DistanceModel(StateSpaceModel):
    """The Brachistochrone model formulatd in the x domain.

    Note that the distance domain formulation could be numerically ill-formed, eg:
    1) when the speed is zero, then dt/dx becomes infinite.
    2) when the angle theta is -pi/2, then the slope is vertical and the tangent dy/dx
    becomes -inf.
    """

    def __init__(
        self, model_config: Dict[str, Any] = {}, params: Dict[str, Any] = {},
    ):
        super().__init__(model_config=model_config, params=params)

    def forward(
        self,
        states: lnp.ndarray,
        inputs: lnp.ndarray,
        mesh: float = 0.0,  # time invariant model
    ) -> StateSpaceModelReturn:
        params = self._params
        theta = self.get_input(inputs, "theta")
        dv_dt = -params["gravity"] * lnp.sin(theta)
        v = self.get_state(states, "v")
        vx = v * lnp.cos(theta)

        # dvx_dt = dv_dt * lnp.cos(theta)
        # d(vx^2)/dx = 2*vx*dvx/dx = 2*dx/dt*(dvx/dx) = 2*dvx/dt
        v_dot = dv_dt / (vx + 1e-9)
        time_dot = 1 / (vx + 1e-9)
        y_dot = lnp.tan(theta)
        # Assemble result
        states_dot = self.make_vector(
            group="states_dot", time_dot=time_dot, v_dot=v_dot, y_dot=y_dot,
        )

        return self.make_state_space_model_return(states_dot=states_dot)

    @classmethod
    def get_default_params(self) -> Dict[str, Any]:
        return {"gravity": 9.81}


def solve_brachistochrone(
    dx: float,
    dy: float,
    time_domain: bool = True,
    backend="jax",
    is_condensed: bool = True,
):
    if time_domain:
        model = TimeModelWithCustomDerivatives()
        sim_config = ScaledMeshOCP.get_sim_config(
            boundary_conditions=(
                BoundaryConditionConfig(0, "states", "x", 0.0),
                BoundaryConditionConfig(0, "states", "y", 0.0),
                BoundaryConditionConfig(0, "states", "v", 0.0),
                BoundaryConditionConfig(-1, "states", "x", dx),
                BoundaryConditionConfig(-1, "states", "y", dy),
            ),
            bounds=(
                BoundConfig("global", "mesh_scale", (0.01, 10.0)),
                BoundConfig("inputs", "theta", (-np.pi / 2, np.pi / 2)),
            ),
            num_intervals=49,
            hessian_approximation="exact",
            # backend=backend,
            # transcription="LGR",
        )
        ocp = ScaledMeshOCP(model=model, sim_config=sim_config)
    else:
        model = DistanceModel()
        sim_config = FixedMeshOCP.get_sim_config(
            boundary_conditions=(
                BoundaryConditionConfig(0, "states", "time", 0.0),
                BoundaryConditionConfig(0, "states", "v", 1e-3),
                BoundaryConditionConfig(0, "states", "y", 0.0),
                BoundaryConditionConfig(-1, "states", "y", dy),
            ),
            bounds=(
                BoundConfig("states", "v", (1e-3, 100)),
                BoundConfig("states", "y", (-5, 0)),
                BoundConfig("inputs", "theta", (-np.pi / 2.01, np.pi / 2.01)),
            ),
            num_intervals=49,
            hessian_approximation="exact",
            backend="casadi",
            transcription="LGR",
            is_condensed=False,
        )
        ocp = FixedMeshOCP(model=model, sim_config=sim_config, mesh_scale=dx)

    # Very casual initial guess -- just all zeros.
    x0 = np.zeros(ocp.num_dec)
    solution, info = ocp.solve(
        x0,
        max_iter=200,
        print_level=1,
        print_timing_statistics="no",
        derivative_test="none",
    )
    vars = ocp.dec_var_operator.unflatten_var(solution)
    op = ocp.dec_var_operator
    final_t = ocp.objective(solution)
    y = vars.states[:, op.get_var_index_in_group("states", "y")]
    min_y = np.min(y)
    logger.info(f"minimum height {min_y:.3f}")
    logger.info(f"final time {final_t:.3f}")

    return final_t


def main():
    dx = 1.0
    dy = -0.65
    x, y, expected_time = cycloid(dx, dy)
    print(f"expected time: {expected_time:.3f}")
    print(f"expected minimum y: {np.min(y):.3f}")

    # solve_distance_domain(dx, dy)
    solve_brachistochrone(dx, dy, backend="jax")
    solve_brachistochrone(dx, dy, backend="casadi")
    solve_brachistochrone(dx, dy, backend="custom")
    solve_brachistochrone(dx, dy, time_domain=False, backend="jax")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
