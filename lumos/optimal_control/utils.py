import logging
from collections import namedtuple
from enum import IntEnum
from typing import List, NamedTuple, Optional, Tuple, Union

import jax.numpy as jnp
import numpy as np

import lumos.numpy as lnp

logger = logging.getLogger(__name__)


def batch_conv1d(x, width, stride, backend: str = "numpy"):
    """Turn a N x (shape) tensor into a batch x width x (shape) tensor

    Effectively turning a tensor that will be convolved with some kernal into a batch
    tensor
    """
    length, *unit_shape = x.shape

    if not ((length - width) % stride == 0):
        raise ValueError(
            f"Cannot divide length {length} equally into width {width} with stride {stride} "
        )
    batch = (length - width) // stride + 1

    overlap = width - stride

    with lnp.use_backend(backend):
        # jax.numpy split does NOT work with -ve indices
        # NOTE: scatter and gather could be very slow here, so better use matrix and vector
        # operations.
        a, b = lnp.split(x, [length - overlap])
        a = lnp.reshape(a, (batch, stride, *unit_shape))
        b = lnp.expand_dims(b, axis=0)

        overlapped = lnp.vstack([a[1:, :overlap], b])
        return lnp.concatenate([a, overlapped], axis=1)


class DecVarOperator:
    """Operatur for manipulating decision variables from/to different forms.

    Requirements:
    - construct a vector (for IPOPT) from matrices of values (states, inputs, etc)
        use cases: construct bounds, construct initial guess
    - construct interval variable matrices from a vector
        use cases: call interval functions
    - split interval variable array into matrices (states, inputs) and scalar (interval_length)
        use cases: inside interval function, call on each stages.

    TODO: should we make the global vars individual scalars as it is now, or should we make it
    a group of vectors? (just like states, inputs, outputs)

    """

    _stage_var_enum: IntEnum  # enum used to index flattend variables in a stage.
    _global_var_enum: IntEnum  # enum used to index global var from the decision var vector

    def __init__(
        self,
        model_var_names: NamedTuple,  # TODO: more concrete classes?
        num_intervals: int,
        num_stages_per_interval: int,
        stage_var_groups: Tuple[
            str, ...
        ],  # defines which model var groups are used as decision variables
        global_var_names: Tuple[str, ...],  # define global variables
    ):
        """[summary]
        model_var_names: to tell the operator:
        1) which groups exist in the model
        2) what are the names and order of the variables in each group

        """
        self._model_var_names = model_var_names
        self._stage_var_groups = stage_var_groups
        self._global_var_names = global_var_names

        self.num_intervals = num_intervals
        self.num_stages_per_interval = num_stages_per_interval

        self._construct_stage_var_enum()
        self._construct_global_var_enum()

    @property
    def num_var_stage(self):
        return sum(self.get_stage_var_size(g) for g in self._stage_var_groups)

    @property
    def num_var_interval_without_global(self):
        return self.num_var_stage * self.num_stages_per_interval

    @property
    def num_var_interval_with_global(self):
        return self.num_var_interval_without_global + self.num_global_var

    @property
    def num_stages(self):
        return self.num_intervals * (self.num_stages_per_interval - 1) + 1

    @property
    def num_all_stage_var(self):
        return self.num_stages * self.num_var_stage

    @property
    def num_global_var(self):
        return len(self._global_var_names)

    @property
    def num_dec(self):
        return self.num_all_stage_var + self.num_global_var

    @property
    def global_var_indices(self) -> List[int]:
        return [self._global_var_enum[n] for n in self._global_var_names]

    def has_global_var(self) -> bool:
        return self.num_global_var > 0

    def get_stage_var_size(self, group: str) -> int:
        return len(getattr(self._model_var_names, group))

    def _build_group_split_indices(self) -> np.ndarray:
        """Return an index set that can be used to split stage var into groups"""
        size_list = [self.get_stage_var_size(g) for g in self._stage_var_groups]

        # To split, we only need the cumsum up to the penultimate one.
        # See np.split
        return np.cumsum(size_list[:-1])

    def _make_decision_varialbes(self, values: List[lnp.ndarray]) -> NamedTuple:
        """
        FIXME: Values must be in the same order as _dec_var_groups
        """
        return namedtuple(
            "DecisionVariables", self._stage_var_groups + self._global_var_names
        )(*values)

    def flatten_var(self, **kwargs) -> lnp.ndarray:
        # Build an list with order of group defined in _dec_var_groups
        global_vars = np.array([kwargs.pop(name) for name in self._global_var_names])
        stage_vars = [kwargs[g] for g in self._stage_var_groups]
        vec = np.concatenate(stage_vars, axis=-1).flatten()

        # Append global vars to the end
        # FIXME: here an order of the vector is also assumed.
        return np.append(vec, global_vars)

    def split_stage_var(self, vec: lnp.ndarray) -> List[lnp.ndarray]:
        """Split the vector representing one stage into its groups"""
        var_groups = np.split(vec, self._build_group_split_indices(), axis=-1)
        return var_groups

    def unflatten_var(self, vec: lnp.ndarray) -> NamedTuple:
        # Use negative indexing because the stage_var size will be different depending on
        # whether we call this function on global_vars or on interval_vars
        if self.has_global_var():
            stage_vars, global_vars = (
                vec[: -self.num_global_var],
                vec[-self.num_global_var :],
            )
        else:
            stage_vars = vec

        # Reshape the vector to a matrix where each row is a stage var vector
        if len(stage_vars) > self.num_var_stage:
            # We call this on 1d array as well as 2d matrices, for 1d array, we don't
            # need to make it a matrix, just keep it as is.
            stage_vars = stage_vars.reshape((-1, self.num_var_stage))

        var_groups = np.split(stage_vars, self._build_group_split_indices(), axis=-1)

        if self.has_global_var():
            var_groups += list(global_vars)

        # FIXME: this make decision variable using a list of var group is dangerous.
        return self._make_decision_varialbes(var_groups)

    def get_interval_tensor(self, x: lnp.ndarray, group_name: str):
        """Return the interval tensor for a given group

        The interval tensor has shape:
        [num_intervals, num_stages_per_interval, num_var_in_group]
        """

        structured_vars = self.unflatten_var(x)
        return batch_conv1d(
            getattr(structured_vars, group_name),
            width=self.num_stages_per_interval,
            stride=self.num_stages_per_interval - 1,
        )

    def build_interval_var_tensor(self, x: lnp.ndarray) -> lnp.ndarray:
        """Build a 2d matrix of interval variables.

        This combines the stages in one interval into a flat vector, and append the
        global variables to the end.
        """
        if self.has_global_var():
            stage_vars, global_vars = (
                x[: -self.num_global_var],
                x[-self.num_global_var :],
            )
        else:
            stage_vars = x
        stage_vars = jnp.reshape(stage_vars, (self.num_stages, self.num_var_stage))

        all_interval_vars_no_last_stage = jnp.reshape(
            stage_vars[:-1, :],
            (self.num_intervals, self.num_stages_per_interval - 1, self.num_var_stage,),
        )

        # last stage of each interval that need to be concatenated.
        last_stage_vars = jnp.expand_dims(
            stage_vars[
                self.num_stages_per_interval - 1 :: self.num_stages_per_interval - 1, :,
            ],
            axis=1,
        )

        # Concatenate to create the intervals, with the point shared between two
        # intervals appearing twice.
        all_interval_vars = jnp.concatenate(
            [all_interval_vars_no_last_stage, last_stage_vars], axis=1
        )

        # reshape [num_intervals, num_stage_per_interval, num_var_stage] ->
        #         [num_intervals, num_var_per_interval]
        all_interval_vars = jnp.reshape(
            all_interval_vars,
            (self.num_intervals, self.num_var_interval_without_global),
        )

        # append global vars to interval vars
        if self.has_global_var():
            all_interval_vars = jnp.hstack(
                (all_interval_vars, jnp.tile(global_vars, (self.num_intervals, 1)),)
            )

        return all_interval_vars

    def build_stage_var_tensor(self, x):
        """Stage var augmented with global var at every stage"""
        if self.has_global_var():
            all_stage_vars, global_vars = (
                x[: -self.num_global_var],
                x[-self.num_global_var :],
            )
        else:
            all_stage_vars = x
        all_stage_vars = jnp.reshape(
            all_stage_vars, (self.num_stages, self.num_var_stage)
        )

        # append global vars to stage vars
        if self.has_global_var():
            all_stage_vars = jnp.hstack(
                (all_stage_vars, jnp.tile(global_vars, (self.num_stages, 1)),)
            )

        return all_stage_vars

    def _make_stage_var_name(self, group: str, name: str) -> str:
        return group + "." + name

    @property
    def stage_var_names(self):
        var_names = []
        for group in self._stage_var_groups:
            var_names += [
                self._make_stage_var_name(group=group, name=n)
                for n in getattr(self._model_var_names, group)
            ]
        return var_names

    def _construct_stage_var_enum(self):
        self._stage_var_enum = IntEnum("StageVarEnum", self.stage_var_names, start=0)

    def _construct_global_var_enum(self):
        self._global_var_enum = IntEnum(
            "GlobalVarEnum", self._global_var_names, start=self.num_all_stage_var,
        )

    def get_var_index_in_group(self, group: str, name: str) -> int:
        """Return the position of a varialbe in its group

        NOTE: this is a duplicate of Model's method with the same name. Can/should we
        unify them?
        """
        return getattr(self._model_var_names, group).index(name)

    def get_global_var_index(self, name: str) -> int:
        return self._global_var_enum[name]

    def get_global_var(self, x, name: str) -> float:
        return x[self.get_global_var_index(name)]

    def get_var_index_in_dec(
        self, group: str, name: str, stage: Optional[int] = None
    ) -> Union[int, List[int]]:
        """Return the index of a variable in the decision var vector.
        
        When the stage is given, returns a float, when a the stage is not given, return
        an array of the all the corresponding decision variables.
        """

        if stage is None:
            # Stage not given, then provide it for all stages.

            return (
                self._stage_var_enum[self._make_stage_var_name(group=group, name=name)]
                + np.arange(self.num_stages) * self.num_var_stage
            )

        else:
            if stage > self.num_stages - 1 or stage < -self.num_stages:
                raise ValueError(
                    (
                        f"stage must be bewteen [{-self.num_stages}, {self.num_stages-1}], "
                        f"but got {stage}"
                    )
                )
            # allow negative index like python list
            stage %= self.num_stages

            return (
                self._stage_var_enum[self._make_stage_var_name(group=group, name=name)]
                + stage * self.num_var_stage
            )

    def get_group_indices_at_stage(self, group: str, stage: int) -> np.ndarray:
        """Return the index of a group of variable in the decision var vector."""
        if stage > self.num_stages - 1 or stage < -self.num_stages:
            raise ValueError(
                (
                    f"stage must be bewteen [{-self.num_stages}, {self.num_stages-1}], "
                    f"but got {stage}"
                )
            )

        # allow negative index like python list
        stage %= self.num_stages

        return (
            np.array(
                [
                    self._stage_var_enum[self._make_stage_var_name(group=group, name=n)]
                    for n in getattr(self._model_var_names, group)
                ]
            )
            + stage * self.num_var_stage
        )

    def get_group_indcies_in_dec(self, group: str) -> np.ndarray:
        """Return the indices of all variables of a group in the decision variable."""
        return np.concatenate(
            [
                self.get_group_indices_at_stage(group=group, stage=ii)
                for ii in range(self.num_stages)
            ]
        )

    def get_var(
        self, x: lnp.ndarray, group: str, name: str, stage: Optional[int] = None
    ) -> Union[float, lnp.ndarray]:
        return x[self.get_var_index_in_dec(group=group, name=name, stage=stage)]


def create_offset_structure(
    base_rows: List[int],
    base_cols: List[int],
    row_offset: int,
    col_offset: int,
    num_blocks: int,
) -> Tuple[np.ndarray, np.ndarray]:

    # Construct the indices stage by stage for readibility
    idx_row, idx_col = [], []
    for interval in range(num_blocks):
        new_idx_row = base_rows + interval * row_offset
        new_idx_col = base_cols + interval * col_offset

        idx_row.append(new_idx_row)
        idx_col.append(new_idx_col)

    return np.hstack(idx_row), np.hstack(idx_col)


def stack_and_increment(x: np.ndarray, axis: int, num_repeat: int, num_increment: int):
    """Repeat and stack an array and increment the repeats.

    Args:
        x (np.ndarray): The base array to be stacked and incremented.
        axis: the axis for stacking.
        num_repeat (int): the number of time the base array is repeated
        num_increment (int): the increment between each repeat of the base array
    """

    stacked = np.stack([x] * num_repeat, axis=axis)

    # Create a 1d array increment, and then make it broadcastable by reshaping the array
    shape_for_broadcast = np.ones(len(stacked.shape), dtype=int)
    shape_for_broadcast[axis] = -1
    increment = np.arange(num_repeat).reshape(shape_for_broadcast) * num_increment
    return stacked + increment