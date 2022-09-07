from typing import Any, List, Tuple, Union
from enum import IntEnum

import numpy as np
from lumos.models.base import Model

from lumos.optimal_control.nlp import BaseConstraints, BaseObjective, CompositeProblem


class ModelSolver(CompositeProblem):
    def __init__(self, model: Model, backend: str, con_outputs: List[str] = []):
        """ModelSolver solves algebraic constraints on models.
        
        TODO: currently only works on StateSpaceModel, but we should make it work
        on any standard models.
        """

        # set constraint outputs
        # TODO: now we have two places using constraint outputs, so maybe this should be
        # a model property?
        # TODO: this is also used in scaled_mesh_ocp
        model.names = model.names._replace(con_outputs=con_outputs)

        # TODO: can/should we get away with not storing the model?
        self._model = model

        # Create the model algebra constraints
        super().__init__(num_in=model.num_implicit_var)

        # Construct variable enum for easier indexing
        self._input_enum = IntEnum("InputEnum", self.input_names, start=0)

        implicit_functions = model.make_model_algebra_cons(backend=backend)

        # TODO: move these somewhere else
        def _jacobian(*args):
            return np.array(implicit_functions["jacobian"](*args).nonzeros())

        def _hessian(*args):
            return np.array(implicit_functions["_hessian"](*args).nonzeros())

        # TODO: model algebra scales, maybe this should be unified with
        # scaled_mesh_ocp.set_scales, and move to higher level?
        # TODO: currently hard-coded all scales to 1
        # model.model_algebra.set_con_scales(np.ones(model.num_implicit_res))

        # FIXME: need to wrap model_algebra to remove mesh and params
        # FIXME: we create CasMappedConstraints (839 in base.py), but it actually is NOT
        # a Constriant that can be executed with its .constraints method, as it requires
        # extra inputs ! (mesh, params)
        # FIXME: mapped constraints are really only called on their mapped methods!
        # So is there any point that they inherit from base_constraints?
        flat_params, unravel = model.get_recursive_params().tree_ravel()
        x0 = np.ones(model.model_algebra.num_in)

        # breakpoint()
        # jac = model.model_algebra.mapped_jacobian(x0, 0.0, flat_params)
        # jac = model.model_algebra.jacobian(x0, 0.0, flat_params)
        # breakpoint()
        model_algebra_con = BaseConstraints(
            num_in=model.model_algebra.num_in,
            num_con=model.model_algebra.num_con,
            constraints=lambda x: model.model_algebra.constraints(x, 0.0, flat_params),
            jacobian=lambda x: _jacobian(x, 0.0, flat_params),
            hessian=lambda x, lagrange: _hessian(x, lagrange, 0.0, flat_params),
            jacobian_structure=model.model_algebra.jacobianstructure(),
            hessian_structure=model.model_algebra.hessianstructure(),
        )

        # Add model algebra constraints
        self.add_constraints("model_algebra", model_algebra_con)

        # Add a constant objective function of 0 (by default, only solving for
        # feasibility)
        # TODO: maybe this should jsut exist in composite problem by default?
        const_obj = BaseObjective(
            num_in=model.num_implicit_var,
            objective=lambda x: 0,
            gradient=lambda x: np.zeros(model.num_implicit_var),
            hessian=lambda x: [],
            hessian_structure=([], []),
        )
        self.add_objective("const_obj", const_obj)

        # Set all constarint values (here all to 0, for equality, or 0 residual)
        self.set_cons()

        # Set default scales of the variables
        self._set_default_var_scales()

    def _construct_name(self, group, name):
        return group + "." + name

    @property
    def input_groups(self):
        """The groups of inputs used in the implicit model algebra call"""
        return self._model.implicit_inputs

    @property
    def input_names(self):
        """TODO: this shares a lot with utils.DecVarOperator"""
        var_names = []
        for group in self.input_groups:
            var_names += [
                self._construct_name(group, n)
                for n in getattr(self._model.names, group)
            ]
        return var_names

    def get_var_idx(self, group, name):
        return self._input_enum[self._construct_name(group, name)]

    def set_cons(self):
        # TODO: this ought to be set in CompositeProblem as well
        # Set all constriants to equality
        self.cl = np.zeros(self.num_con)
        self.cu = np.zeros(self.num_con)

    def set_bounds(
        self, group: str, name: str, bounds: Union[float, Tuple[float, float]]
    ):
        idx = self.get_var_idx(group, name)

        if isinstance(bounds, tuple):
            lb, ub = bounds
        else:
            lb = ub = bounds

        assert (
            lb <= ub
        ), f"lower bounds must be smaller than upper bounds, but got ({lb}, {ub}) for {group}.{name}"

        self.lb[idx] = lb
        self.ub[idx] = ub

    def get_bounds(self, group, name):
        idx = self.get_var_idx(group, name)

        return self.lb[idx], self.ub[idx]

    def _set_default_var_scales(self):
        """Create the default scale storage.
        
        This should also trigger the corresponding updates of the input and output
        scales in the constraints.
        """

        self._var_scales = {
            g: {n: 1.0 for n in getattr(self._model.names, g)}
            for g in self.input_groups
        }

        self._update_problem_scales()

    def _update_problem_scales(self):
        # TODO: construct the actual constraint scales

        # HACK: hard-coded order here needs to correspond to order of model_algebra.
        # scaled_mesh_ocp.py has exactly the same issue
        states_dot_scales = np.array(
            [self._var_scales["states"][n] for n in self._model.names.states]
        )
        con_output_scales = np.array(
            [self._var_scales["con_outputs"][n] for n in self._model.names.con_outputs]
        )

        # For residuals, the user can set them in the model when forming the residuals
        # as they are supposed to be 0 anyway.
        residual_scales = np.ones(self._model.num_residuals)

        model_algebra_scales = np.concatenate(
            [states_dot_scales, con_output_scales, residual_scales]
        )

        self._constraints["model_algebra"].set_con_scales(model_algebra_scales)

        # TODO: update objective function scale?

        # TODO: udpate decision variable scale
        # TODO: this could need some tidy-up, across the NLP classes
        for g in self.input_groups:
            for n in getattr(self._model.names, g):
                self._dec_var_scales[
                    self._model.get_var_index_in_flat(g, n)
                ] = self._var_scales[g][n]

        for _, c in self._constraints.items():
            c.set_input_scales(self._dec_var_scales)

    def set_var_scale(self, group, name, val):
        """Set the scale for one variable
        
        These variable scales are then used to construct the scales of the constraints
        and decision variables

        Groups that can have their scales set are: states, inputs and con_outputs.
        """
        assert val > 0, "scale must be positive!"
        _allowed_groups = ["states", "inputs", "con_outputs"]
        if group not in _allowed_groups:
            raise KeyError(
                f"{group} is not a valid group. Allowed groups are {_allowed_groups}"
            )

        if name not in self._var_scales[group]:
            raise KeyError(
                f"{name} is not a valid variable in the group {group}, valid names are: {list(self._var_scales[group].keys())}"
            )

        # We need to update the following:
        # 1) input scales to the objective and constraints
        # 2) output scales of the constraints
        # 3) decision variable scales (Is this a duplicate? if we scale overall dec var
        # then we don't have to scale each individual constraints, and we can just leave
        # them as unscaled?) -> in scaled_mesh_ocp, we don't do overall problem scaling
        # but just pass the scaling to sub problems, which probably makes sense

        self._var_scales[group][name] = val

        self._update_problem_scales()

    def get_var(self, x, group, name):
        idx = self.get_var_idx(group, name)
        return x[idx]

    def print_result(self, x):

        for idx, name in enumerate(self.input_names):
            print(f"{name}: {x[idx]}")
