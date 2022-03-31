from typing import Any, Callable, Dict

import numpy as np

from lumos.optimal_control.nlp import BaseConstraints, CasConstraints
from lumos.optimal_control.utils import (
    DecVarOperator,
    batch_conv1d,
    create_offset_structure,
)


class ConvConstraints(BaseConstraints):
    def __init__(
        self,
        unit_problem: BaseConstraints,
        dec_var_op: DecVarOperator,
        normalized_mesh: np.ndarray,
        mesh_scale_fn: Callable,
        params: Dict[str, Any],
        stage_or_interval: str = "stage",
    ):
        """An NLP problem formulated by convoluting some unit problems over the decision variable.

        To parallelize the convolution is done in a batched fashion, by transforming the
        inputs into a batched array, which is then evaluated by all the NLP functions in
        batches.

        The width of the convolution is defined by the unit_probem's number of inputs.

        Args:
            unit_problem (UnitProblem): The unit_problem that acts as a convolution kernel
            normalized mesh: the normalized mesh [0, 1] that is needed for the unit
            problem, with lead dimension = batch.
            mesh_scale_fn: a function that takes the decision variable and returns the
            mesh scale.

        FIXME: Currently for non-fixed grid problems, the derivative w.r.t. mesh is not
        taken into account! This means that it only works for 'time-invariant' ODE/DAE
        at the moment.
        """
        self._unit_problem = unit_problem
        self._normalized_mesh = normalized_mesh
        self._mesh_scale_fn = mesh_scale_fn
        self._op = dec_var_op
        if stage_or_interval == "stage":
            self._batch = dec_var_op.num_stages
            self._stride = dec_var_op.num_var_stage
        elif stage_or_interval == "interval":
            self._batch = dec_var_op.num_intervals
            self._stride = (
                dec_var_op.num_var_interval_with_global - dec_var_op.num_var_stage
            )
        self._width = unit_problem.num_in
        self.set_params(params)

    @property
    def num_con(self):
        return self._batch * self._unit_problem.num_con

    @property
    def num_in(self):
        return self._op.num_dec

    def set_params(self, params):
        # Casadi functions requires flat array as inputs.
        # TODO: perhaps we should move this into another wrapper on CasConstraints and
        # leave ConvConstraints backend-agnostic. The advantage of doing it like now is
        # to 1) use minimum code in CasConstraints and 2) only run this parameter
        # flattening once, instead of everytime a function is called.
        if isinstance(self._unit_problem, CasConstraints):
            self._params, _ = params.tree_ravel()
        else:
            self._params = params

    def _transform_inputs(self, x):
        # FIXME: This should probably come from the dec_var_operator
        if not (self._op.num_global_var == 0):
            x = x[: -self._op.num_global_var]

        return batch_conv1d(
            x,
            width=self._width,
            stride=self._stride,
        )

    def _get_mesh(self, x):
        return self._normalized_mesh * self._mesh_scale_fn(x)

    # NOTE: here for the constraints, jacobian and hessian, we deliberately leave out
    # the unravelling because it would be handled at the next stage in CompositeProblem.
    # This is to avoid having backend confusion for the 'ravel' op.
    def _constraints_with_params(self, x, params):
        transformed_vars = self._transform_inputs(x)
        return self._unit_problem.mapped_constraints(
            transformed_vars, self._get_mesh(x), params
        )

    # NOTE: the extra level of factoring is so that we can jit the inner level call
    # and keep params a non-static arguments for jit
    def constraints(self, x):
        return self._constraints_with_params(x, self._params)

    def _jacobian_with_params(self, x, params):
        transformed_vars = self._transform_inputs(x)
        jac = self._unit_problem.mapped_jacobian(
            transformed_vars, self._get_mesh(x), params
        )
        return jac

    def jacobian(self, x):
        return self._jacobian_with_params(x, self._params)

    def _hessian_with_params(self, x, lagrange, params):
        transformed_vars = self._transform_inputs(x)

        # Reshape lagrange to get ready for vmap
        shape = (self._batch, self._unit_problem.num_con)
        if np.prod(shape) != len(lagrange):
            raise ValueError(
                f"wrong length of lagrangian. Expect {np.prod(shape)}, but got {len(lagrange)}"
            )
        lagrange = np.reshape(lagrange, shape)

        hh = self._unit_problem.mapped_hessian(
            transformed_vars, self._get_mesh(x), params, lagrange
        )

        return hh

    def hessian(self, x, lagrange):
        return self._hessian_with_params(x, lagrange, self._params)

    def jacobianstructure(self):

        unit_rows, unit_cols = self._unit_problem.jacobianstructure()

        rows, cols = create_offset_structure(
            base_rows=np.ravel(unit_rows),
            base_cols=np.ravel(unit_cols),
            row_offset=self._unit_problem.num_con,
            col_offset=self._stride,
            num_blocks=self._batch,
        )

        return rows, cols

    def hessianstructure(self):

        unit_rows, unit_cols = self._unit_problem.hessianstructure()

        rows, cols = create_offset_structure(
            base_rows=np.ravel(unit_rows),
            base_cols=np.ravel(unit_cols),
            row_offset=self._stride,
            col_offset=self._stride,
            num_blocks=self._batch,
        )

        return rows, cols
