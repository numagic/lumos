import logging
from collections import namedtuple
from enum import IntEnum
from typing import Dict, List, NamedTuple, Optional, Tuple, Union

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

    _stage_var_enum: IntEnum  # enum used to index flattend variables in a stage.
    _global_var_enum: IntEnum  # enum used to index global var from the decision var vector

    def __init__(
        self,
        model_var_names: NamedTuple,
        num_intervals: int,
        num_stages_per_interval: int,
        stage_var_groups: Tuple[str, ...],
        global_var_names: Tuple[str, ...],
    ):
        """A helper class to construct and manipulate the decision variables.

        Args:
            model_var_names (NamedTuple): the NamedTuple describing all the I/O of a
                model
            num_intervals (int): number of intervals of the problem.
            num_stages_per_interval (int): number of stages per interval.
            stage_var_groups (Tuple[str, ...]): the groups of variables (from the model)
                that are used in the problem construction.
            global_var_names (Tuple[str, ...]): global variables of the problem, that do
                not exist at each stage, but only as single scalars for the whole
                problem. eg: some global variable to scale the mesh.
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
    def num_var_interval(self):
        return self.num_var_stage * self.num_stages_per_interval

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

    def split_stage_and_global_vars(
        self, x: lnp.ndarray
    ) -> Tuple[lnp.ndarray, lnp.ndarray]:
        return lnp.split(x, (self.num_all_stage_var,))

    def merge_stage_and_global_vars(
        self, stage_vars: lnp.ndarray, global_vars: lnp.ndarray
    ) -> lnp.ndarray:

        assert (
            stage_vars.ndim == 1 and global_vars.ndim == 1
        ), "inputs must be 1d arrays."

        return np.append(stage_vars, global_vars)

    def _make_decision_varialbes(self, **kwargs: Dict[str, lnp.ndarray]) -> NamedTuple:
        return namedtuple(
            "DecisionVariables", self._stage_var_groups + self._global_var_names
        )(**kwargs)

    def flatten_var(self, **kwargs) -> lnp.ndarray:
        global_vars = np.array([kwargs.pop(name) for name in self._global_var_names])
        stage_vars = [kwargs[g] for g in self._stage_var_groups]
        vec = np.concatenate(stage_vars, axis=-1).flatten()

        return self.merge_stage_and_global_vars(vec, global_vars)

    def unflatten_var(self, vec: lnp.ndarray) -> NamedTuple:
        stage_vars, global_vars = self.split_stage_and_global_vars(vec)

        # Reshape into 2d array, split into groups
        stage_vars = stage_vars.reshape((-1, self.num_var_stage))
        stage_vars = np.split(stage_vars, self._build_group_split_indices(), axis=-1)

        # Create inputs for making decision variable namedtuple
        vars = {k: v for k, v in zip(self._stage_var_groups, stage_vars)}
        vars.update({k: v for k, v in zip(self._global_var_names, global_vars)})

        return self._make_decision_varialbes(**vars)

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
        if group == "global":
            return self._global_var_enum[name] - self.num_all_stage_var
        else:
            return getattr(self._model_var_names, group).index(name)

    def get_var_index_in_dec(
        self, group: str, name: str, stage: Optional[int] = None
    ) -> Union[int, List[int]]:
        """Return the index/indices of a variable.

        Args:
            group (str): the group of the variable. eg: "states", "inputs", "global"
            name (str): the name of the variable in the group.
            stage (Optional[int], optional): the stage at which to get the variable.
                For stage variables, if not given, then return an indices for all
                stages. For global variables, stage is not required. Works with -ve
                indexing as well Defaults to None.

        Raises:
            ValueError: when the stage defined is outside of the range of the problem.

        Returns:
            Union[int, List[int]]: the index of a variable at a given stage,
                                or the index of a global variable
                                or the indices of a variable at all stages.
        """

        if group == "global":
            if stage is not None:
                logger.warning("stage is ignored for group == 'global'")
            return self._global_var_enum[name]
        else:
            if stage is None:
                # Stage not given, then provide it for all stages.

                return (
                    self._stage_var_enum[
                        self._make_stage_var_name(group=group, name=name)
                    ]
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
                    self._stage_var_enum[
                        self._make_stage_var_name(group=group, name=name)
                    ]
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

    def get_stage_var_array(self, x):
        """Return an N x d array, for N stages and d variables per stage"""

        return np.reshape(
            x[: self.num_dec - self.num_global_var],
            (self.num_stages, self.num_var_stage),
        )


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
