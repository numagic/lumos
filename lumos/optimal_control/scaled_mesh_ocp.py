import glob
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
import pyarrow as pa
from pyarrow import parquet as pq
from scipy import sparse

from lumos.models.base import StateSpaceModel
from lumos.optimal_control.nlp import (
    BaseConstraints,
    LinearConstraints,
    BaseObjective,
    CompositeProblem,
)
from lumos.optimal_control.config import (
    BoundaryConditionConfig,
    ScaleConfig,
    BoundConfig,
    SimConfig,
)
from lumos.optimal_control.convolution import ConvConstraints
from lumos.optimal_control.transcription import LGR, make_transcription, Transcription
from lumos.optimal_control.utils import (
    DecVarOperator,
    batch_conv1d,
    stack_and_increment,
)

logger = logging.getLogger(__name__)


def _build_full_name(group: str, name: str) -> str:
    return group + "." + name


def _split_full_name(group_and_name: str) -> Tuple[str, str]:
    return group_and_name.split(".")


class ScaledMeshOCP(CompositeProblem):
    """Generic Optimal Control Problem"""

    # Class for the corresponding config
    ConfigClass: type = SimConfig

    # No Global variables
    global_var_names: List[str] = ["mesh_scale"]

    # see: https://cyipopt.readthedocs.io/en/stable/reference.html
    # for callback arguments
    _metric_names: List[str] = [
        "alg_mod",
        "iter_count",
        "obj_value",
        "inf_pr",
        "inf_du",
        "mu",
        "d_norm",
        "regularization_size",
        "alpha_du",
        "alpha_pr",
        "ls_trials",
    ]

    # TODO: move param out of jit, and observe for any change
    def __init__(self, model: StateSpaceModel, sim_config: Dict[str, Any] = None):

        self.model = model

        # Storing modle parameter (or maybe we should instantiate the model inside)
        # TODO: we need to handle parameters better
        self._params = self.model.get_recursive_params()

        # TODO: what should be in sim_config, and how do we manage them?
        if sim_config is None:
            sim_config = self.get_sim_config()

        self.hessian_approximation: str = sim_config.hessian_approximation
        self.num_intervals: int = sim_config.num_intervals
        self.transcription: Transcription = make_transcription(
            *sim_config.transcription
        )
        self.is_condensed: bool = sim_config.is_condensed
        self.backend: str = sim_config.backend
        # TODO: accessing private attribute
        self.stage_var_groups = list(self.model._implicit_inputs)

        # Create a decision variable operator
        # NOTE: we factor this out of OCP to simplify and to seperate responsibility
        self.dec_var_operator = DecVarOperator(
            model_var_names=self.model.names,
            num_intervals=self.num_intervals,
            num_stages_per_interval=self.transcription.num_stages_per_interval,
            stage_var_groups=self.stage_var_groups,
            global_var_names=self.global_var_names,
        )

        self._create_mesh()

        self.logging_config = sim_config.logging_config

        # Properties for logging
        self._logging_dir: str = None
        self._initialize_logging()

        self.model.make_model_algebra_cons(self.backend)

        # NOTE: here it is mega dangerous that if we keep appending ConvProlbme to the
        # composite problem, then it could be
        super().__init__(num_in=self.num_dec)
        self._build_objective()

        self._build_model_algebra()
        self._build_continuity_cons()
        if sim_config.is_cyclic:
            self._build_cyclic_cons(sim_config.non_cyclic_vars)

        if self.is_condensed:
            self._build_condensed_model_algebra()
            # The states_dot decision variables are un-used, so we set it to
            # 0, and IPOPT will take them out of the NLP depending the settings.
            sim_config.bounds += tuple(
                BoundConfig("states_dot", n, (0, 0))
                for n in self.model.get_group_names("states_dot")
            )

        # Set default varaible bounds and constraint bounds
        self.set_default_bounds()
        self.update_bounds(sim_config.bounds)

        # Set initial and final boundary conditions
        self.set_boundary_conditions(sim_config.boundary_conditions)

        # Set the constraint upper and lower bounds.
        self.set_cons()

        # Set up scaling
        self.set_scales(sim_config.scales)

    @classmethod
    def get_sim_config(cls, *args, **kwargs) -> SimConfig:
        """Need to nuke this and do proper config class"""

        return cls.ConfigClass(*args, **kwargs)

    def _set_model_params(self, model_params):
        self._params = model_params
        self.model.set_recursive_params(model_params)
        # FIXME: using interal attributes. At the moment only model_algebra constraints
        # need the parameters (and we put all model-related computation there)
        # We could make the entire 'CompositeProblem' parameterized, but that might
        # be an over-complication.
        self._constraints["model_algebra"].set_params(model_params)

    def modify_model_param(self, path, value):
        self._params.set_param(path, value)
        # FIXME: using self._params as an argument feels a bit odd..
        self._set_model_params(self._params)

    def _build_cyclic_vars(self, non_cyclic_vars: List[str]):
        """Build a list of cyclic variables, removing those that are non-cyclic."""
        self._cyclic_vars = []
        # by default, make all states and inputs cyclic
        for group in ["states", "inputs"]:
            self._cyclic_vars += [
                _build_full_name(group, n) for n in self.model.get_group_names(group)
            ]

        # remove those that are required to be non-cyclic
        for group_and_name in non_cyclic_vars:
            if group_and_name in self._cyclic_vars:
                self._cyclic_vars.remove(group_and_name)
            else:
                raise ValueError(
                    f"required non cyclic variable {group_and_name} is not an cyclic "
                    "constraint variablem, existing ones are {self._cyclic_vars}"
                )

    def solve(self, *args, **kwargs):
        """Overwrite to add the logging of last iteration"""
        # Do some timing
        x0 = self.get_init_guess()
        # If jax backend, do one call to invoke jit first
        if self.backend == "jax":
            logger.info("Triggering jax JIT")
            self.profile(x0, repeat=1, hessian=self.hessian_approximation == "exact")
            logger.info("Triggering jax JIT completed")
        logger.info("Time NLP execution")
        self.profile(x0, repeat=10, hessian=self.hessian_approximation == "exact")
        # Then solve.
        out = super().solve(*args, **kwargs)
        # TODO: perhaps a better way is to register pre-solve and post-solve tasks.
        self._log_final_iter()

        return out

    def _condensed_constraints(self, x):
        op = self.dec_var_operator
        vars = op.unflatten_var(x)
        idx_states_dot = op.get_group_indcies_in_dec("states_dot")
        # HACK: somehow the unflattened vars are still mutable, and can be affected by
        # changes to the original vector!
        new_x = np.copy(x)
        new_x[idx_states_dot] = 0

        algebraic_con = self._con_storage["model_algebra"].constraints(new_x)

        # Reshape algebraic_con to (num_stages, num_con_per_stage) to make indexing
        # easier
        algebraic_con = np.reshape(algebraic_con, (self.num_stages, -1))
        # HACK: here we rely on the states_dot constraints being the first ones
        states_dot = algebraic_con[:, : self.model.num_states]

        # Compute condensed constraints
        A, B = self.transcription.get_continuity_matrices()
        interval_length = self._normalized_interval_length * self._get_mesh_scale(x)

        states = batch_conv1d(
            vars.states,
            width=op.num_stages_per_interval,
            stride=op.num_stages_per_interval - 1,
        )
        states_dot = batch_conv1d(
            states_dot,
            width=op.num_stages_per_interval,
            stride=op.num_stages_per_interval - 1,
        )

        # A@x - B@x_dot*t == 0
        # (batch, num_stages_per_interval -1, num)
        condensed_con = np.einsum("ijk,lj->ilk", states, A) - np.einsum(
            "ijk,lj->ilk", (states_dot.T * interval_length).T, B
        )

        return np.hstack(
            [
                np.ravel(condensed_con),
                np.ravel(algebraic_con[:, self.model.num_states :]),
            ]
        )

    def _make_chainrule_condensed_jacobian(self, continuity_jac, algebraic_jac):
        op = self.dec_var_operator
        idx_states_dot = op.get_group_indcies_in_dec("states_dot")

        # Use chain rule to 'transfer' derivatives w.r.t x_dot to other variables
        # And remove the deriatives w.r.t. x_dot in the end.

        # HACK: relies on hard-coded constraint orders
        idx_xdot_eqs = stack_and_increment(
            np.arange(self.model.num_states),
            axis=0,
            num_repeat=self.num_stages,
            num_increment=self.model.num_implicit_res,
        )
        # FIXME: dxdot_dvar has undesired x_dot entry with value -1 in it.
        dxdot_dvar = algebraic_jac[idx_xdot_eqs.ravel(), :]
        dcont_dxdot = continuity_jac[:, idx_states_dot]

        dcont_dvar_from_xdot = dcont_dxdot @ dxdot_dvar
        # FIXME: continuity_jac has undesired x_dot entry in it
        # NOTE: but somehow the unwanted entries in the two seem to cancel each other out
        # which doesn't seem to be a coincidence because it still holds if we change
        # the number of intervals! (so it's not a coincidence of coefficient matching
        # when we have a certain scheme with a certain interval length)
        #
        # dcont_dvar_from_xdot is actually: dcont/dxdot @ d(f - x_dot)/dvar
        # and the extra term we didn't remove (dxdot/dvar) is like an identity matrix in
        # the x_dot part of the continuity jacobian -> this cancels out the part that
        # we need to remove from the continuity jacobian
        dcont_dvar = continuity_jac + dcont_dvar_from_xdot

        # For algebraic jac, we only keep the rows not related to x_dot
        b_not_states_dot_eq = np.full((algebraic_jac.shape[0],), True)
        b_not_states_dot_eq[idx_xdot_eqs.ravel()] = False
        pure_algebraic_jac = algebraic_jac[b_not_states_dot_eq, :]

        condensed_jac = sparse.vstack([dcont_dvar, pure_algebraic_jac])
        return condensed_jac

    def _condensed_jacobian(self, x):
        """Condensed jacobian formulation using direct chain rule"""
        algebraic_jac = self._con_storage["model_algebra"].get_csc_jacobian(x)

        op = self.dec_var_operator
        if "mesh_scale" in op._global_var_names:
            # The continuity constraints' derivative with respect to mesh_scale needs
            # to see the actual states_dot used in the continuity equations, which is
            # why we need to replace the decision variable's states_dot entries with
            # the real states_dot before they are passed into the continuity jacobian
            # function.
            vars = op.unflatten_var(x)
            model_return = self.model.batched_forward(
                vars.states,
                vars.inputs,
                self._flat_normalized_mesh * self._get_mesh_scale(x),
                self._params,
            )

            x = op.flatten_var(
                states=vars.states,
                inputs=vars.inputs,
                con_outputs=vars.con_outputs,
                mesh_scale=vars.mesh_scale,
                states_dot=model_return.states_dot,
            )

        continuity_jac = self._con_storage["continuity"].get_csc_jacobian(x)

        big_jac = self._make_chainrule_condensed_jacobian(continuity_jac, algebraic_jac)
        rows, cols = self._condensed_jac_structure
        logger.debug(f"data/structure nnz: {len(big_jac.data)}/{len(rows)}")

        # Extra conversion needed as indedxing csc returns a numpy.matrix
        # The indexing is necessary as we can't use big_jac.data because it might be
        # shorter than the actual sparsity vals when scipy.sparse take out explicit
        # zeros
        return np.squeeze(np.asarray(big_jac.tocsc()[rows, cols]))

    def _condensed_jacobianstructure(self):
        """Return jacobian structure by a pessimistic estimate"""
        # We estimate the sparsity by passing in a random vecotr. There is the risk
        # that the sparse library would actually remove explicit zeros (opposite to
        # structural zeros, these are values that happen to be zero at this point of
        # calculation and make the estimation more optimistic/sparser). But the risk
        # is pretty low when we're using float, and it's probably very very small
        # probability that float computations will become 'zero' accidentally.
        #
        # If we want to be conservative, we could create the algebraic and continuity
        # jacobians with no explicit zeros, which would probably give a more
        # pessimistic estimate.
        x0 = np.random.randn(self.num_dec)
        algebraic_jac = self._con_storage["model_algebra"].get_csc_jacobian(x0)
        continuity_jac = self._con_storage["continuity"].get_csc_jacobian(x0)
        # This jac should have a pessimistic structure: the least possible sparsity
        structure_jac = self._make_chainrule_condensed_jacobian(
            continuity_jac, algebraic_jac
        )

        return structure_jac.nonzero()

    def _condensed_hessian(self, x, lagrange):
        """Compute the condensed hessian values.

        We take advantage of the observation that:
        - the hessian is always the same shape, regardless of how many constraints there
        are
        - the hessian is just the sum of all constraints, weighed by the lagrangian
        multipliers. (although when we compute the hessian, we do the sum first to save
        cost)

        As such, we can compute the condensed hessian using the same model_algebra and
        continuity hessian function calls, but feeding them with equivalent lagrangian
        multiliers. So the real taks is to find the conversion of lagrangian multipliers
        from the old constraints to the new condensed constraints.
        """
        op = self.dec_var_operator

        num_condensed_continuity_cons = (
            self.num_intervals
            * (op.num_stages_per_interval - 1)
            * self.model.num_states
        )

        # new lagrange: [all_condensed_continuity, algebraic arranaged in stages]
        lagrange_for_continuity, lagrange_for_algebraic = np.split(
            lagrange, [num_condensed_continuity_cons]
        )

        # HACK: somehow the unflattened vars are still mutable, and can be affected by
        # changes to the original vector!
        idx_states_dot = op.get_group_indcies_in_dec("states_dot")

        A, B = self.transcription.get_continuity_matrices()
        interval_length = self._normalized_interval_length * self._get_mesh_scale(x)

        lagrange_for_continuity = lagrange_for_continuity.reshape(
            self.num_intervals, op.num_stages_per_interval - 1, self.model.num_states
        )

        # Work out the equivalent lagrangian multiplier to pass to the algebraic hessian
        lagrange_condensed_converted = np.einsum(
            "ijk,jl->ilk", lagrange_for_continuity, -B
        ) * interval_length.reshape(self.num_intervals, 1, 1)

        # NOTE: when converting from interval to stages, there is one stage shared
        # between two intervals
        lagrange_condensed_converted[:-1, -1, :] += lagrange_condensed_converted[
            1:, 0, :
        ]

        lagrange_condensed_converted = np.vstack(
            [
                lagrange_condensed_converted[0, 0, :],
                lagrange_condensed_converted[:, 1:, :].reshape(
                    -1, self.model.num_states
                ),
            ]
        )

        # The state_dot constraints in model algebra is: f(x, u) - x_dot_hat
        # So the second term is linear, so the hessian of that is the same as what we
        # want: hessian of f(x, u). The lagrnagian mutliplier therefore has to be in the
        # shape of flattened (num_stages, num_var_stage)
        lagrange_equivalent = np.hstack(
            [
                lagrange_condensed_converted,
                lagrange_for_algebraic.reshape(self.num_stages, -1),
            ]
        ).ravel()

        model_algebra_hess = self._con_storage["model_algebra"].hessian(
            x, lagrange_equivalent
        )

        op = self.dec_var_operator
        if "mesh_scale" in op._global_var_names:
            # If mesh_scale is a variable, then the continuity constraints also has
            # non-zero hessian entries.
            continuity_hess = self._con_storage["continuity"].get_csc_hessian(
                x, lagrange_for_continuity.ravel()
            )
            algebraic_jac = self._con_storage["model_algebra"].get_csc_jacobian(x)
            idx_xdot_eqs = stack_and_increment(
                np.arange(self.model.num_states),
                axis=0,
                num_repeat=self.num_stages,
                num_increment=self.model.num_implicit_res,
            )
            dxdot_dvar = algebraic_jac[idx_xdot_eqs.ravel(), :]

            # Use chain rule on x_dot to get the continuity hessian w.r.t. all variables
            # and the mesh_scale
            # L = lagrangian of continuity
            # d2L/dvar/dmesh = d2L/xdot/dmesh @ dxdot/dvar
            new_vals = (
                dxdot_dvar.T @ continuity_hess[idx_states_dot, -1].toarray().ravel()
            )
            # set all deriviatives w.r.t. x_dot to 0. This is because dxdot_dvar is
            # taken from algebraic_jac, which has the f(x, u) - x_dot entry. We could
            # also remove the x_dot elements in dxdot_dvar, but it's more efficient to
            # do it here than do it in dxdot_dvar, whcih is a sparse matrix.
            new_vals[idx_states_dot] = 0
            return np.hstack([model_algebra_hess.ravel(), new_vals])
        else:
            return model_algebra_hess

    def _condensed_hessianstructure(self):
        # Same structure as model algebra
        rows, cols = self._con_storage["model_algebra"].hessianstructure()

        op = self.dec_var_operator
        if "mesh_scale" in op._global_var_names:
            # If mesh_scale is a variable, then the continuity constraints also has
            # non-zero hessian entries.
            cont_rows = np.arange(self.num_dec)
            cont_cols = np.ones(self.num_dec) * (self.num_dec - 1)
            rows = np.hstack([rows.ravel(), cont_rows])
            cols = np.hstack([cols.ravel(), cont_cols])
        return rows, cols

    def _create_mesh(self):
        """Creates a normalized mesh for the given transcription."""
        # Normalized mesh [0, 1]
        interval_length = 1 / self.num_intervals
        all_interval_mesh = []
        for interval in range(self.num_intervals):
            # FIXME: need to handle getting interval points better
            if isinstance(self.transcription, LGR):
                interval_mesh = (
                    interval * interval_length
                    + (self.transcription.interp_points + 1) / 2 * interval_length
                )
            else:
                interval_mesh = np.array([interval, interval + 1]) * interval_length

            all_interval_mesh.append(interval_mesh)

            # full 1d mesh, by linking all interval together without the duplicate
            if interval == 0:
                _flat_normalized_mesh = interval_mesh
            else:
                _flat_normalized_mesh = np.hstack(
                    [_flat_normalized_mesh, interval_mesh[1:]]
                )

        self._matrix_normalized_mesh = np.vstack(all_interval_mesh)
        self._flat_normalized_mesh = _flat_normalized_mesh
        self._normalized_interval_length = (
            self._matrix_normalized_mesh[:, -1] - self._matrix_normalized_mesh[:, 0]
        )

    def _get_mesh_scale(self, x):
        return self.dec_var_operator.get_var(x, "global", "mesh_scale")

    def get_mesh_from_scale(self, mesh_scale):
        """Get the unnormalized mesh as a flat array

        TODO: is this method a bit redundant?
        """
        return self._flat_normalized_mesh * mesh_scale

    # FIXME: here we're just piping some of the DecVarOperator properties to the parent class
    # Should we keep this or just directly use self.dec_var_operator.xxx?
    @property
    def num_stages(self):
        return self.dec_var_operator.num_stages

    @property
    def num_dec(self):
        return self.dec_var_operator.num_dec

    @property
    def num_continuity_cons(self):
        return (
            self.model.num_states
            * self.transcription.num_constraints_per_interval
            * self.num_intervals
        )

    def _stage_hessianstructure(self):
        """states_dot and con_outputs are only linear, so no hessian

        NOTE: for truely implicit equations where states_dot or con_outputs are
        algebraic variables they could become nonlinear! But in those case, the
        condensed approach also won't work. (because it has no explicit ODE to work on)
        """
        op = self.dec_var_operator
        rows, cols = np.nonzero(np.ones((op.num_var_stage, op.num_var_stage)))

        # remove those related to states_dot and con_outputs
        idx_remove = np.hstack(
            [
                op.get_group_indices_at_stage("states_dot", stage=0),
                op.get_group_indices_at_stage("con_outputs", stage=0),
            ]
        )

        keep_rows = np.array([r not in idx_remove for r in rows])
        keep_cols = np.array([c not in idx_remove for c in cols])
        keep = keep_rows & keep_cols

        return rows[keep], cols[keep]

    def set_default_bounds(self):
        """Set default bounds of decision variables without external configs.
        
        For the base class, the default is set to be unbounded.
        """

        # Create default (-inf, inf) bounds
        self.lb = -np.inf * np.ones(self.num_dec)
        self.ub = np.inf * np.ones(self.num_dec)

    def update_bounds(self, bounds: Tuple[BoundConfig]):
        """Update variable bounds using bound configs.
        
        If bounds on the same varialbe are defined more than once, the later ones will
        overwrite the earlier ones, so that only the last one will remain in effect.
        """

        # Overwrite with external bound settings
        op = self.dec_var_operator
        for b in bounds:
            lb, ub = b.values
            idx = op.get_var_index_in_dec(group=b.group, name=b.name)
            # Convert scalar to array. Only need to check one bound as the
            # BoundConfig ensure both are the same type
            if not (np.isscalar(idx)) and not (np.isscalar(lb)):
                assert len(lb) == self.num_stages, (
                    f"OCP has {self.num_stages} stages, but got bounds for "
                    f"{b.group}.{b.name} with size {len(lb)}"
                )
            self.lb[idx] = lb
            self.ub[idx] = ub

    def set_scales(self, scale_configs: Tuple[ScaleConfig]):
        """Construct variable scales

        The scale of a variable represents qualitatively how 'large' a varialbe is.
        Using scales of variables, we construct the scaling factors for constraints and
        decision variables.

        Constraints:
        - g_hat = g/g_scale
        - The constraint scaling are applied by modifying the NLP function constraints,
        this is done so that the convergence criteria will be determined on scaled
        constraint values.

        Decision variables:
        - x_hat = x*x_scale
        - The decision variable scaling is done directly via IPOPT settings, in order to
        minimize the changes required to NLP functions.
        """

        op = self.dec_var_operator

        # First we create a dictioinary to summarise all scales in one place, with
        # default values of 1 (unscaled)
        var_scales = {
            g: self.model.make_const_vector(g, 1.0) for g in self.model._implicit_inputs
        }
        var_scales["global"] = np.ones(op.num_global_var)

        # create default decision variable scales
        self._dec_var_scales = np.ones(self.num_dec)

        # Overwrite with scales from configs and update decision variable scales
        for sc in scale_configs:
            var_scales[sc.group][
                op.get_var_index_in_group(sc.group, sc.name)
            ] = sc.value
            self._dec_var_scales[op.get_var_index_in_dec(sc.group, sc.name)] = (
                1 / sc.value
            )

        # Set constarint scales
        continuity_scales = np.ravel(
            np.tile(
                var_scales["states"],
                (self.num_intervals, op.num_stages_per_interval - 1, 1),
            )
        )

        if self.is_condensed:
            # For condensed problem, the constraints are ordered as: all condensed
            # continuity con, con_outputs and residuals arranged stage by stage.
            # NOTE: here we scale the residuals with unity because:
            # 1) they are not decision, we don't necessarily need to set their scales
            # 2) the user are free to set the scales of the residual in the model.
            condensed_model_algebra_scales = np.concatenate(
                [continuity_scales]
                + [var_scales["con_outputs"], np.ones(self.model.num_residuals),]
                * self.num_stages
            )
            self._constraints["model_algebra"].set_con_scales(
                condensed_model_algebra_scales
            )

        else:
            # HACK: hard-coded order here needs to correspond to order of model_algebra. How
            # do we make it more robust? (same for condensed)
            model_algebra_scales = np.concatenate(
                [
                    var_scales["states"],
                    var_scales["con_outputs"],
                    np.ones(self.model.num_residuals),
                ]
                * self.num_stages
            )

            self._constraints["model_algebra"].set_con_scales(model_algebra_scales)
            self._constraints["continuity"].set_con_scales(continuity_scales)

    def set_boundary_conditions(
        self, boundary_conditions: Tuple[BoundaryConditionConfig]
    ):
        for bc in boundary_conditions:
            self._set_var_bounds(
                group=bc.group, name=bc.name, stage=bc.stage, bounds=bc.value
            )

    def _set_var_bounds(
        self,
        group: str,
        name: str,
        stage: int,
        bounds: Union[float, Tuple[float, float]],
    ):

        idx_var = self.dec_var_operator.get_var_index_in_dec(
            group=group, name=name, stage=stage
        )

        if isinstance(bounds, tuple):
            lb, ub = bounds
        else:
            lb = ub = bounds

        assert lb <= ub, "lower bound must be no larger than the upper bound"

        self.lb[idx_var] = lb
        self.ub[idx_var] = ub

    # TODO: maybe this can be done with just a 'partial'?
    def set_state_bounds(
        self, name: str, stage: int, bounds: Union[float, Tuple[float, float]]
    ):
        self._set_var_bounds(group="states", name=name, stage=stage, bounds=bounds)

    def set_input_bounds(
        self, name: str, stage: int, bounds: Union[float, Tuple[float, float]]
    ):
        self._set_var_bounds(group="inputs", name=name, stage=stage, bounds=bounds)

    def set_con_output_bounds(
        self, name: str, stage: int, bounds: Union[float, Tuple[float, float]]
    ):
        self._set_var_bounds(group="con_outputs", name=name, stage=stage, bounds=bounds)

    def set_cons(self):
        # Set all constriants to equality
        self.cl = np.zeros(self.num_con)
        self.cu = np.zeros(self.num_con)

    def get_lb(self, group: str, name: str):
        return self.dec_var_operator.get_var(self.lb, group=group, name=name)

    def get_ub(self, group: str, name: str):
        return self.dec_var_operator.get_var(self.ub, group=group, name=name)

    def _initialize_logging(self):
        """Create directory and storage for logging"""
        config = self.logging_config

        if (
            config["log_final_iter"]
            or config["log_metrics_history"]
            or config["log_every_nth_iter"] > 0
        ):
            # Create unique name (not guaranteed unique, but that would depend on sim_id or name in the future)
            if config["sim_name"] is None:
                name_suffix = ""
            else:
                name_suffix = "_" + config["sim_name"]
            subdir_name = datetime.now().strftime("%Y%m%d-%H%M%S") + name_suffix
            self._logging_dir = os.path.join(config["results_dir"], subdir_name)
            Path(self._logging_dir).mkdir(parents=True, exist_ok=True)

        if config["log_metrics_history"]:
            # Create initial dataframe for the history
            self._metrics_history_df = pd.DataFrame(data=[], columns=self._metric_names)

    @property
    def logging_dir(self):
        return self._logging_dir

    def _log(self, metrics: Dict[str, Any]):
        """Log an iteration

        metrics: intermediate call arguments turned into a dictionary
        """
        config = self.logging_config
        iter_num = metrics["iter_count"]

        if config["log_metrics_history"]:
            self._metrics_history_df = self._metrics_history_df.append(
                metrics, ignore_index=True
            )

        if (
            config["log_every_nth_iter"] > 0
            and iter_num % config["log_every_nth_iter"] == 0
        ):
            # NOTE: we could choose not to write out here and keep the dfs in memory,
            # but this will most likely cause us to run out of memory when the prolbem
            # gets big. Although we combine the df in any case...
            self._create_result_df(
                self._last_iter_dec_var,
                file_path=os.path.join(self._logging_dir, f"iter_{iter_num}.csv"),
                iter_num=iter_num,
            )

            if config["log_metrics_history"]:
                # We also write this out at every iteration so we can see the results
                # before the optimization finisehs
                self._metrics_history_df.to_csv(
                    os.path.join(self._logging_dir, "metrics_history.csv"), index=False
                )

    def _log_final_iter(self):
        # TODO: we should be able to do better than these hard-coded names everywhere.
        config = self.logging_config

        if config["log_every_nth_iter"] > 0:
            # Combine all iteration results
            iter_files = glob.glob(os.path.join(self._logging_dir, "iter*.csv"))
            df_list = [pd.read_csv(f) for f in iter_files]
            all_iters_df = (
                pd.concat(df_list, axis=0)
                .sort_values(["iter", "distance"])
                .reset_index(drop=True)
            )

            # Remove all the iteration files, and dump the combined one.
            pq.write_table(
                pa.Table.from_pandas(all_iters_df),
                os.path.join(self._logging_dir, "all_iters.parquet"),
            )
            for file in iter_files:
                os.remove(file)

            # Compute what causes the max violation at each iteration
            con_names = [c for c in df_list[0].columns if "_con." in c]
            # Initialize storage, watchout for datatype
            self._metrics_history_df["max_violation_con_name"] = "null"
            self._metrics_history_df["max_violation_distance"] = -1.0
            # NOTE: here the file list will not be arranged according to iter number.
            for iter_df in df_list:
                idx, column = iter_df[con_names].abs().stack().idxmax()
                iter_num = iter_df["iter"][0]
                self._metrics_history_df.loc[
                    iter_num, "max_violation_con_name"
                ] = column
                self._metrics_history_df.loc[
                    iter_num, "max_violation_distance"
                ] = iter_df["distance"][idx]

        if config["log_metrics_history"]:
            self._metrics_history_df.to_csv(
                os.path.join(self._logging_dir, "metrics_history.csv"), index=False
            )

        if config["log_final_iter"]:
            self._create_result_df(
                self._last_iter_dec_var,
                file_path=os.path.join(self._logging_dir, f"final_iter.csv"),
                iter_num=self._num_iter,  # TODO: unify num_iter and iter_num?
            )

    def _create_result_df(self, dec_var: np.ndarray, file_path: str, iter_num: int):
        logger.debug("Creating iteration result dataframe")
        structured_vars = self.dec_var_operator.unflatten_var(dec_var)
        model_return = self.model.batched_forward(
            structured_vars.states,
            structured_vars.inputs,
            self._flat_normalized_mesh * self._get_mesh_scale(dec_var),
            self._params,
        )

        cons = self.constraints(dec_var)
        # split into interval con and stage con (for lifted problem)
        # FIXME: this assumes ordering of constraints, which would break easily
        if self.is_condensed:
            cons = self.split_constraints(cons)
            interval_cons = cons["model_algebra"]
            interval_con_shape = (
                self.num_stages - 1,
                self.model.num_states
                + self.model.num_con_outputs
                + self.model.num_residuals,
            )
            interval_con_columns = (
                ["interval_con." + n for n in self.model.get_group_names("con_outputs")]
                + ["interval_con." + n for n in self.model.get_group_names("residuals")]
                + ["interval_con." + n for n in self.model.get_group_names("states")]
            )
        else:
            cons = self.split_constraints(cons)
            interval_cons = cons["continuity"]
            stage_cons = cons["model_algebra"]
            interval_con_shape = (self.num_stages - 1, self.model.num_states)
            interval_con_columns = [
                "interval_con." + n for n in self.model.get_group_names("states")
            ]

        # each interval provides (num_stages_per_interval -1) x num_states constraints
        # for LGR collocation and for quadrature schemes
        # FIXME: not valid for LGL or LG schemes
        # so in total it provides (num_stages - 1)*num_states constraints
        # (there is always one stage shared between two intervals)
        interval_cons = np.reshape(interval_cons, interval_con_shape)

        # Append a zero row at the top -> so num of rows is num_stages
        interval_cons = np.vstack([np.zeros(interval_con_shape[1]), interval_cons])
        # create interval con df
        interval_cons_df = pd.DataFrame(
            data=interval_cons, columns=interval_con_columns,
        )

        if not self.is_condensed:
            # Stage constraints are concatenated as [states_dot, outputs]
            stage_cons = np.reshape(
                stage_cons, (self.num_stages, self.model.num_implicit_res)
            )
            stage_cons_df = pd.DataFrame(
                data=stage_cons,
                columns=[
                    "stage_con." + n for n in self.model.get_group_names("states_dot")
                ]
                + ["stage_con." + n for n in self.model.get_group_names("con_outputs")]
                + ["stage_con." + n for n in self.model.get_group_names("residuals")],
            )

        dec_var_df = pd.DataFrame(
            data=np.reshape(
                dec_var, (self.num_stages, self.dec_var_operator.num_var_stage)
            ),
            columns=self.dec_var_operator.stage_var_names,
        )

        outputs_df = pd.DataFrame(
            model_return.outputs,
            columns=["outputs." + n for n in self.model.get_group_names("outputs")],
        )

        if self.is_condensed:
            df_list = [dec_var_df, outputs_df, interval_cons_df]
        else:
            df_list = [dec_var_df, outputs_df, interval_cons_df, stage_cons_df]

        # combine dfs
        result_df = pd.concat(df_list, axis=1)
        # add distance
        result_df["distance"] = self._flat_normalized_mesh * self._get_mesh_scale(
            dec_var
        )
        # add iteration number
        result_df["iter"] = iter_num
        logger.debug("Iteration result dataframe created")
        result_df.to_csv(file_path, index=False)
        logger.debug(f"Iteration result dataframe written to {file_path}")

    def intermediate(self, *args):
        """Overwrite parent class method to provide more detailed logging"""

        # See _metric_names for the order of the arguments
        # turn args into dictionary
        metrics = dict(zip(self._metric_names, args))

        # When first going into restoration phase, intermedaite is called again
        # with the same iteration number (and also same decision var and infeasibillty etc)
        # So we ignore the logging there
        if metrics["alg_mod"] == 0 and metrics["iter_count"] == self._num_iter:
            pass
        else:
            self._log(metrics)
            self._num_iter = metrics["iter_count"]

    def _get_cyclic_indices(self) -> Tuple[np.ndarray, np.ndarray]:
        """Return the initial and final variable indices that need to be cyclic."""

        idx_initial, idx_final = [], []
        op = self.dec_var_operator

        for group_and_name in self._cyclic_vars:
            group, name = _split_full_name(group_and_name)
            idx_initial.append(op.get_var_index_in_dec(group, name, stage=0))
            idx_final.append(op.get_var_index_in_dec(group, name, stage=-1))

        return np.hstack(idx_initial), np.hstack(idx_final)

    def _cyclic_constraint(self, x):
        idx_initial, idx_final = self._get_cyclic_indices()
        return x[idx_initial] - x[idx_final]

    def _cyclic_jacobian(self, x):
        idx_initial, idx_final = self._get_cyclic_indices()
        return np.hstack([np.ones_like(idx_initial), -np.ones_like(idx_final)])

    def _cyclic_jacobianstructure(self):
        idx_initial, idx_final = self._get_cyclic_indices()
        num_var = len(idx_initial)
        rows = np.hstack([np.arange(num_var), np.arange(num_var)])
        cols = np.hstack([idx_initial, idx_final])

        return rows, cols

    def _time_objective(self, x):
        structured_var = self.dec_var_operator.unflatten_var(x)
        return structured_var.mesh_scale

    def _time_gradient(self, x):
        grad = np.zeros_like(x)
        grad[self.dec_var_operator.get_var_index_in_dec("global", "mesh_scale")] = 1
        return grad

    def _continuity_constraints(self, x):
        op = self.dec_var_operator
        interval_length = self._normalized_interval_length * self._get_mesh_scale(x)

        states = op.get_interval_tensor(x, group_name="states")
        states_dot = op.get_interval_tensor(x, group_name="states_dot")

        A, B = self.transcription.get_continuity_matrices()

        # A@x - B@x_dot*t == 0
        con = np.einsum("ijk,lj->ilk", states, A) - np.einsum(
            "ijk,lj->ilk", (states_dot.T * interval_length).T, B
        )

        return np.ravel(con)

    def _continuity_jacobian(self, x):
        """Bilinear constraints for continuity

        When the mesh can be scaled, it is a bilinear constraint; when the mesh is fixed
        it is a linear constraint.

        NOTE: we could potentially take advatange of the sparsity further by noting the
        sparsity in the A, B matrices. (typically one of them is sparse. For
        differential schemes, B is sparse, and for integration scheme, A is sparse.)
        """
        op = self.dec_var_operator
        interval_length = self._normalized_interval_length * self._get_mesh_scale(x)

        # Constraints are constructed as (interval, stages-1, state)
        # decision variables are constructed as (interval, stages, state)
        # So we expect in total (interval, stages-1, stages, state) non-zero entries,
        # which is the (stages-1, stages) base linear constraints replicated across all
        # intervals and states.
        # For the same state in an interval:
        # - two consecutive equations are num_states apart
        # - the indices of two consecutive entries are num_var_stage apart.

        # First: construct the rows and cols for one state in one interval
        A_matrix, B_matrix = self.transcription.get_continuity_matrices()

        # Recplicate to all intervals
        A_vals = np.stack([A_matrix] * self.num_intervals, axis=0)
        B_vals = np.stack([B_matrix] * self.num_intervals, axis=0)
        B_vals = -B_vals * interval_length.reshape([-1, 1, 1])

        # Replicate to all states
        A_vals = np.stack([A_vals] * self.model.num_states, axis=-1)
        B_vals = np.stack([B_vals] * self.model.num_states, axis=-1)
        vals = [A_vals.ravel(), B_vals.ravel()]

        if "mesh_scale" in op._global_var_names:
            states_dot_interval_tensor = op.get_interval_tensor(
                x, group_name="states_dot"
            )

            mesh_scale_der = (
                -B_matrix
                @ states_dot_interval_tensor
                * self._normalized_interval_length.reshape([-1, 1, 1])
            )

            vals.append(mesh_scale_der.ravel())

        return np.concatenate(vals)

    def _continuity_jacobianstructure(self):
        # Structure computation
        # Base row and column structure corresponding to one state over one interval
        # So the rows and cols matrices have the same shape as A and B

        op = self.dec_var_operator
        # FIXME: here we rely on the statse and states_dot are ordered in the same way!
        first_state = self.model.get_group_names("states")[0]
        first_state_idx = op.get_var_index_in_dec("states", first_state, stage=0)
        first_state_dot = self.model.get_group_names("states_dot")[0]
        states_to_states_dot_offset = (
            op.get_var_index_in_dec("states_dot", first_state_dot, stage=0)
            - first_state_idx
        )

        # indexing for equations
        A_rows = np.vstack(
            [np.arange(op.num_stages_per_interval - 1) * self.model.num_states]
            * op.num_stages_per_interval
        ).T
        # indexing for variables
        A_cols = np.vstack(
            [first_state_idx + np.arange(op.num_stages_per_interval) * op.num_var_stage]
            * (op.num_stages_per_interval - 1)
        )

        # First stack and increment along the interval axis
        A_rows = stack_and_increment(
            A_rows,
            axis=0,
            num_repeat=self.num_intervals,
            num_increment=(op.num_stages_per_interval - 1) * self.model.num_states,
        )

        A_cols = stack_and_increment(
            A_cols,
            axis=0,
            num_repeat=self.num_intervals,
            num_increment=op.num_var_interval - op.num_var_stage,
        )

        # Then stack and increment along the interval axis
        A_rows = stack_and_increment(
            A_rows, axis=-1, num_repeat=self.model.num_states, num_increment=1,
        )

        A_cols = stack_and_increment(
            A_cols, axis=-1, num_repeat=self.model.num_states, num_increment=1
        )

        # The structure for B is very similar to that of A:
        # - the rows are the same (they contribute to the same equations)
        # - the column is offset by a constant (the index offset between states and
        # states_dot in the same stage)
        B_rows = A_rows
        B_cols = A_cols + states_to_states_dot_offset

        rows = [A_rows.ravel(), B_rows.ravel()]
        cols = [A_cols.ravel(), B_cols.ravel()]

        if "mesh_scale" in op._global_var_names:
            mesh_scale_rows = A_rows[:, :, 0, :]
            mesh_scale_cols = op.get_var_index_in_dec(
                "global", "mesh_scale"
            ) * np.ones_like(mesh_scale_rows)
            rows.append(mesh_scale_rows.ravel())
            cols.append(mesh_scale_cols.ravel())
        return np.concatenate(rows), np.concatenate(cols)

    def _continuity_hessian(self, x, lagrange):

        # NOTE: hessian is constant w.r.t. input x, but NOT constant w.r.t. to the
        # lagrangian multiplier, so we cannot use a cached versio of it for all
        # iterations.
        # A@x - B@x_dot*t = 0
        # The only 2nd order entries are the bilinear terms of the scale and the
        # B@x_dot*t, at the columns for the x_dot*t. And this should be a constant B
        # multiplied by the lagrangian multipliers

        # reshape multiplier to (num_interval, num_con_interval, num_states)
        op = self.dec_var_operator
        new_shape = (
            self.num_intervals,
            op.num_stages_per_interval - 1,
            self.model.num_states,
        )
        lagrange = lagrange.reshape(new_shape)

        # broadcast multiply on the interval dimension by interval length
        lagrange = lagrange * self._normalized_interval_length.reshape([-1, 1, 1])

        A, B = self.transcription.get_continuity_matrices()
        vals = np.einsum("ijk,jl->ilk", lagrange, -B)

        return vals

    def _continuity_hessianstructure(self):
        # We need upper triangular matrix indices.
        # base row for one stage in one interval
        op = self.dec_var_operator
        rows = op.get_group_indices_at_stage(group="states_dot", stage=0)

        # replicate over the stages dimension for one interval
        rows = np.stack([rows] * op.num_stages_per_interval, axis=0)
        rows += (np.arange(op.num_stages_per_interval) * op.num_var_stage).reshape(
            (-1, 1)
        )

        # replicate over the interval dimension. Note the overlap of one stage
        # between the intervals
        rows = np.stack([rows] * self.num_intervals, axis=0)
        rows += (
            np.arange(op.num_intervals) * (op.num_var_interval - op.num_var_stage)
        ).reshape((-1, 1, 1))

        # col is easy, just the mesh_scale
        cols = np.ones_like(rows) * op.get_var_index_in_dec("global", "mesh_scale")
        return rows, cols

    def _build_continuity_cons(self):
        continuity_cons = BaseConstraints(
            constraints=self._continuity_constraints,
            num_in=self.num_dec,
            num_con=self.num_continuity_cons,
            jacobian=self._continuity_jacobian,
            jacobian_structure=self._continuity_jacobianstructure(),
            hessian=self._continuity_hessian,
            hessian_structure=self._continuity_hessianstructure(),
        )

        self.add_constraints("continuity", continuity_cons)

    def _build_condensed_model_algebra(self):
        # HACK: storage for cons
        self._con_storage = {
            "model_algebra": self._constraints["model_algebra"],
            "continuity": self._constraints["continuity"],
        }
        self._condensed_jac_structure = self._condensed_jacobianstructure()

        self.delete_constraints("model_algebra")
        self.delete_constraints("continuity")

        op = self.dec_var_operator
        num_con = self.num_intervals * (
            op.num_stages_per_interval - 1
        ) * self.model.num_states + self.num_stages * (
            self.model.num_implicit_res - self.model.num_states
        )

        condensed_cons = BaseConstraints(
            num_in=self.num_dec,
            num_con=num_con,
            constraints=self._condensed_constraints,
            jacobian=self._condensed_jacobian,
            jacobian_structure=self._condensed_jac_structure,
            hessian=self._condensed_hessian,
            hessian_structure=self._condensed_hessianstructure(),
        )

        self.add_constraints("model_algebra", condensed_cons)

    def _build_model_algebra(self):
        # NOTE: we must call map directly on a casadi function objecte.
        # map doesn't work on a 'partial' object
        # This means the mapped function container must be the one that passes in
        # the parameters!
        # This also means mapping dictionary to flat must also happen at top level
        # The casadi function must be left untouched to be mapped
        stage_cons = ConvConstraints(
            unit_problem=self.model.model_algebra,
            dec_var_op=self.dec_var_operator,
            normalized_mesh=self._flat_normalized_mesh,
            mesh_scale_fn=self._get_mesh_scale,
            params=self._params,
        )

        # FIXME: currently the unpacking in interval con relies on the order here
        self.add_constraints("model_algebra", stage_cons)

    def _build_cyclic_cons(self, non_cyclic_vars: List[str]):
        self._build_cyclic_vars(non_cyclic_vars)
        cyclic_con = LinearConstraints(
            num_in=self.num_dec,
            num_con=len(self._cyclic_vars),
            constraints=self._cyclic_constraint,
            jacobian=self._cyclic_jacobian,
            jacobian_structure=self._cyclic_jacobianstructure(),
        )
        self.add_constraints("cyclic", cyclic_con)

    def _build_objective(self):
        # Common objective regardless of the problem
        time_objective = BaseObjective(
            objective=lambda x: self._time_objective(x),
            gradient=lambda x: self._time_gradient(x),
            hessian=lambda x: np.array([]),
            hessian_structure=(np.array([]), np.array([])),
        )
        self.add_objective("time", time_objective)

    def get_init_guess(self):
        return np.random.randn(self.num_dec)
