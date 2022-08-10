from __future__ import annotations  # Cyclic referencing of types

from copy import deepcopy
from typing import Any, Dict
from jax.tree_util import register_pytree_node_class

import numpy as np
import casadi as cas

"""
NOTE:
- we chose not to use existing 3rd party tree library yet, because it doesn't seem to
bring benefit for the current design. (maybe with a redesign, then it would be). For 
example, with anytree, the syntax isn't really much better.

from anytree import Resolver
resolver = Resolver("name")
resolver.get(changed_params, "aero/base").data["alpha"] = alpha

TODO:
- audit where we should copy and how to avoid redunddant copying. Also if it really
gets large, we need to find a way to improve efficiency.
- clean-up dispatch vs backend
"""


class Tree:
    def __init__(self, data, data_type: type, children: Dict[str, Tree] = {}):
        """General tree type data structure.

        Currently it is mainly used to represent two types of structure:

        ConfigTree: model configuration that specifies what submodel types a model
        contains. The leaf node data type is string (of the submodel type)

        ParameterTree: tree structure for parameters that specify the parameters of the
        model including its submodels. The leaf node data type is a flat dictionary
        of parameters.
        """
        # The dictionary actually holding the tree data
        self._data = data
        self._data_type = data_type
        self._children = {}

        for k, v in children.items():
            self.add_child(name=k, subtree=v)

    @property
    def data(self):
        return self._data

    def add_child(self, name: str, subtree: Tree):
        # FIXME: check name collision
        self._children[name] = subtree

    def get_child(self, name) -> Tree:
        return self._children[name]

    def _get_subtree(self, path, delimiter=".") -> Tree:
        if path:
            child_names = path.split(delimiter)
            t = self
            for n in child_names:
                t = t.get_child(n)
            return t
        else:
            return self

    def to_dict(self):

        # Ensure "children" key appears regardless whether a child exists
        d = {
            "data": self._data,
            "children": {},
        }

        if self._children:
            d["children"] = {k: v.to_dict() for k, v in self._children.items()}

        # Note that the dictionary will contain mutable items, so we deep copy
        # such that modifing the dict can't modify the tree.
        return deepcopy(d)

    @classmethod
    def from_dict(cls, d):
        # Build from a copy of the dict so that changing the dict won't change the tree
        d = deepcopy(d)
        tree = cls(d["data"])

        for k, v in d["children"].items():
            tree.add_child(name=k, subtree=cls.from_dict(v))

        return tree

    def _set_leaf(self, path, value, delimiter="."):
        if self._data_type == str:
            subtree = self._get_subtree(path, delimiter)
            subtree._data = value
        elif self._data_type == dict:
            *path_names, param_key = path.split(delimiter)
            subtree = self._get_subtree(delimiter.join(path_names))
            subtree._data[param_key] = value
        else:
            raise TypeError("Only str and dict supported for Tree at the moment")

    def replace_subtree(self, path, subtree: Tree, delimiter="."):
        """Replace the subtree (with its children) with the new subtree"""
        if not isinstance(subtree, Tree):
            raise TypeError(
                f"subtree input should be of type 'Tree', but got '{type(subtree)}'"
            )
        *path_to_parent, child_name = path.split(delimiter)
        path_to_parent = delimiter.join(path_to_parent)
        parent = self._get_subtree(path_to_parent)

        # Ensure the child to be replaced does actually exist
        if child_name in parent._children:
            parent._children[child_name] = subtree
        else:
            raise KeyError(f"{path_to_parent} does not contain a child: '{child_name}'")

    def to_flat_dict(self):
        return self._make_flat_dict(), self._make_tree_def()

    def _make_flat_dict(self, prefix="") -> Dict[str, Any]:
        # FIXME: This is not really very readable logic.
        # 1) on the first call, add_prefix returns elf.data itself, which is a dict,
        # which we later keep 'updating' -> so we need to deep copy when returning itself
        # 2) this works for config tree as well, but it's not realy very readable.

        if self._data_type == dict:
            flat_d = _add_prefix(self.data, prefix)
        else:
            # For str data type, the root would just add {"": root_data)
            # -> {"": root_data, "child1": child1_data, ...}
            flat_d = {prefix: self.data}

        for name, child in self._children.items():
            # NOTE: here add_prefix always operates on a dict
            flat_d.update(_add_prefix(child._make_flat_dict(prefix=name), prefix))

        return deepcopy(flat_d)

    def _make_tree_def(self, dummy_var="*"):
        flat_d = self._make_flat_dict()

        t = self.__class__.from_dict(self.to_dict())
        for k in flat_d:
            # NOTE: here we make the treedef bascially a tree with data replaced by some
            # arbitrary value
            t._set_leaf(k, dummy_var)
        return t.to_dict()

    @classmethod
    def from_flat_dict(cls, tree_def, flat_dict):
        # TODO: it should be acutally possible to build from flat_dict without tree_def
        # right?
        flat_dict = deepcopy(flat_dict)
        unflattened = cls.from_dict(tree_def)
        for k, v in flat_dict.items():
            unflattened._set_leaf(k, v)

        return unflattened

    def __repr__(self) -> str:
        return str(self.to_dict())


@register_pytree_node_class
class ParameterTree(Tree):
    def __init__(self, data, children: Dict[str, ConfigTree] = {}):
        super().__init__(data, data_type=dict, children=children)

    def get_param(self, path, delimiter="."):
        *path_names, param_key = path.split(delimiter)
        t = self._get_subtree(delimiter.join(path_names))
        return t._data[param_key]

    def set_param(self, path, value, delimiter="."):
        self._set_leaf(path, value, delimiter)

    # Methods required to register jax pytree
    def tree_flatten(self):
        flat_dict, tree_def = self.to_flat_dict()
        # NOTE: the aux variables must support equality comparison. Otherwise we would have
        # lots of recompilation due to cache-miss
        return list(flat_dict.values()), (tree_def, list(flat_dict.keys()))

    @classmethod
    def tree_unflatten(cls, aux, children):
        tree_def, flat_keys = aux
        flat_dict = dict(zip(flat_keys, children))
        return cls.from_flat_dict(tree_def, flat_dict)

    def tree_ravel(self):
        flat_list, aux = self.tree_flatten()

        tree_def, flat_keys = aux

        # FIXME: we could directly use the flat_list here, but we use flat_dict for now
        # because we know it works
        flat_dict = dict(zip(flat_keys, flat_list))

        flat, unravel = _ravel_flat_dict(flat_dict)
        unravel_pytree = lambda flat: self.__class__.tree_unflatten(
            aux, list(unravel(flat).values())
        )

        return flat, unravel_pytree


class ConfigTree(Tree):
    def __init__(self, data, children: Dict[str, ConfigTree] = {}):
        super().__init__(data, data_type=str, children=children)


def _add_prefix(d: Dict[str, Any], prefix: str, delimiter: str = "."):
    """add prefix to keys"""
    assert isinstance(d, dict)
    if prefix:
        return {prefix + delimiter + n: v for n, v in d.items()}
    else:
        # We use a deepcopy here so add_prefix would alwasy return a new dictionary
        # which we could safely modify
        return deepcopy(d)


def _is_casadi_instance(x):
    return isinstance(x, (cas.SX, cas.MX, cas.DM))


def _size(x):
    # This is more like a dispatch rather (so operation depending on data type)
    # rather than backend selection
    if _is_casadi_instance(x):
        return x.numel()
    else:
        return np.size(x)


def _shape(x):
    if _is_casadi_instance(x):
        return x.shape
    else:
        return np.shape(x)


def _size_and_shape(x):
    return _size(x), _shape(x)


def _ravel(x):
    if _is_casadi_instance(x):
        return x.reshape((x.numel(), 1))
    else:
        return np.ravel(x)


def _split(arr, indices):
    if _is_casadi_instance(arr):
        indices = [0, *indices, arr.numel()]
        return cas.vertsplit(arr, indices)
    else:
        return np.split(arr, indices)


def _concat(lst):
    if _is_casadi_instance(lst[0]):
        return cas.vertcat(*lst)
    else:
        return np.hstack(lst)


def _unzip2(xys):
    xs = []
    ys = []
    for x, y in xys:
        xs.append(x)
        ys.append(y)
    return tuple(xs), tuple(ys)


def _ravel_flat_dict(flat_tree):
    if not flat_tree:
        return np.array([], np.double), lambda _: {}

    keys, values = flat_tree.keys(), flat_tree.values()
    sizes, shapes = _unzip2(_size_and_shape(x) for x in values)

    indices = np.cumsum(sizes)

    def unravel(arr):
        chunks = _split(arr, indices[:-1])
        if _is_casadi_instance(arr):
            # For casadi backend, we need to create casadi flat and TreeParams form
            # numpy TreeParams. As such as we need the unravel able to handle casadi
            # varialbs when casadi represents 1d arrays as 2d column arrays.
            # See models.base.StateSpaceModel._make_casadi_model_algebra_cons
            new_shapes = []
            for shape in shapes:
                if len(shape) == 1:
                    # Make it a 2d shape of column vector for casadi
                    shape = (shape[0], 1)
                new_shapes.append(shape)

        else:
            new_shapes = shapes

        reconstructed_values = [
            chunk.reshape(shape) if _size(chunk) > 1 else chunk[0]
            for chunk, shape in zip(chunks, new_shapes)
        ]
        return dict(zip(keys, reconstructed_values))

    raveled = _concat([_ravel(e) for e in values])

    return raveled, unravel
