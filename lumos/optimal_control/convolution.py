from typing import Any, Callable, Dict

import numpy as np

from lumos.optimal_control.nlp import MappedConstraints, CasMappedConstraints
from lumos.optimal_control.utils import (
    DecVarOperator,
    batch_conv1d,
    create_offset_structure,
)
from lumos.models.tree_utils import ParameterTree


class ConvConstraints(MappedConstraints):
    def __init__(
        self,
        unit_problem: MappedConstraints,
        dec_var_op: DecVarOperator,
        normalized_mesh: np.ndarray,
        mesh_scale_fn: Callable,
        params: Dict[str, Any],
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

        NOTE: we could create set_con_scales method here that just repeats the scales of
        the unit problem. However since that would require the unit problem to be set
        already at the construction of the ConvProblem, it is tricky to do.
        """

        self._unit_problem = unit_problem
        self._normalized_mesh = normalized_mesh
        self._mesh_scale_fn = mesh_scale_fn
        self._op = dec_var_op
        self._batch = dec_var_op.num_stages
        self._stride = dec_var_op.num_var_stage

        self._width = unit_problem.num_in
        self.set_params(params)

        def _constraints(x):
            transformed_vars = self._transform_inputs(x)
            return np.ravel(
                unit_problem.mapped_constraints(
                    transformed_vars, self._get_mesh(x), self._params
                )
            )

        def _jacobian(x):
            transformed_vars = self._transform_inputs(x)
            return np.ravel(
                unit_problem.mapped_jacobian(
                    transformed_vars, self._get_mesh(x), self._params
                )
            )

        def _hessian(x, lagrange):
            transformed_vars = self._transform_inputs(x)

            # Reshape lagrange to get ready for vmap
            shape = (self._batch, unit_problem.num_con)
            if np.prod(shape) != len(lagrange):
                raise ValueError(
                    f"wrong length of lagrangian. Expect {np.prod(shape)}, "
                    f"but got {len(lagrange)}"
                )
            lagrange = np.reshape(lagrange, shape)

            hess = unit_problem.mapped_hessian(
                transformed_vars, lagrange, self._get_mesh(x), self._params
            )

            return np.ravel(hess)

        jac_struct, hess_struct = self._build_jac_and_hess_struct(unit_problem)

        super().__init__(
            num_in=dec_var_op.num_dec,
            num_con=self._batch * unit_problem.num_con,
            constraints=_constraints,
            jacobian=_jacobian,
            hessian=_hessian,
            jacobian_structure=jac_struct,
            hessian_structure=hess_struct,
        )

    def set_params(self, params):
        # Casadi functions requires flat array as inputs.
        # TODO: perhaps we should move this into another wrapper on CasMappedConstraints and
        # leave ConvConstraints backend-agnostic. The advantage of doing it like now is
        # to 1) use minimum code in CasMappedConstraints and 2) only run this parameter
        # flattening once, instead of everytime a function is called.
        if isinstance(self._unit_problem, CasMappedConstraints):
            self._params, _ = params.tree_ravel()
        else:
            self._params = params

    def _transform_inputs(self, x):
        stage_vars, _ = self._op.split_stage_and_global_vars(x)

        return batch_conv1d(stage_vars, width=self._width, stride=self._stride,)

    def _get_mesh(self, x):
        return self._normalized_mesh * self._mesh_scale_fn(x)

    def _build_jac_and_hess_struct(self, unit_problem):

        # Jacobian
        unit_rows, unit_cols = unit_problem.jacobianstructure()

        jac_struct = create_offset_structure(
            base_rows=np.ravel(unit_rows),
            base_cols=np.ravel(unit_cols),
            row_offset=unit_problem.num_con,
            col_offset=self._stride,
            num_blocks=self._batch,
        )

        # Hessian
        unit_rows, unit_cols = unit_problem.hessianstructure()

        hess_struct = create_offset_structure(
            base_rows=np.ravel(unit_rows),
            base_cols=np.ravel(unit_cols),
            row_offset=self._stride,
            col_offset=self._stride,
            num_blocks=self._batch,
        )

        return jac_struct, hess_struct
