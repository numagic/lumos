from __future__ import annotations  # Model referencing Model

from typing import Any, Dict, List, Optional
from lumos.models.tree_utils import ParameterTree, ConfigTree

""" Summary notes
This is a very rough design for building trees of models, working with trees of configs
and trees of model parameterse. To see examples, it's best to look into the unit test:
lumos.models.test_models.test_model_composition.

Design:
- a global model registry is used which forces no model name clash.
- ConfigTree is the first object that needs to exist, because it defines what submodels
a model tree would include, by which it also defines what tree structure the parameters
should have.
- trees are not defined up front: the tree structure can be different for different
variant combinations. Eg, an Aero model can have a DRS child, but another aero model
might not have it. The vehicle model that has the aero as an input shouldh't care what
sub models an aero model has, it only cares that it has a child aero model itself. 
- a model should/can define its own one-level submodels, because it will be directly
calling them. But it shouldn't/doesn't need to know its grandchildrens
- a model should not need to access parameters other than those directly defined in it (
    not including those in its children)
- we allow model parameterization on construction (so one-line model construction and
parameterization) The model tree structure needs to be built first in init.

TODO:
- Currently it's very hard to debug when something fails... Since we use a dictionary,
most likely the user would just get a keyerror, or some other indexing error.
- we should probably allow other config arguments as inputs to the model instantiation,
eg, the number of layers of a NN aero model, opt=True for tyre models etc.
"""


class ModelMaker:
    _registry: Dict[str, type] = {}

    @classmethod
    def _check_exists(cls, type_name: str) -> bool:
        if type_name not in cls._registry:
            raise KeyError(f"registry does not contain a model type: '{type_name}'")

    @classmethod
    def get_model_class(cls, type_name: str) -> type:
        cls._check_exists(type_name)
        return cls._registry[type_name]

    @classmethod
    def make_config(cls, type_name: str) -> ConfigTree:
        return ModelMaker.get_model_class(
            type_name
        ).get_recursive_default_model_config()

    @classmethod
    def make_model_from_config(cls, model_config: ConfigTree) -> CompositeModel:
        ModelClass = cls.get_model_class(model_config.data)
        model = ModelClass(model_config=model_config)

        return model

    @classmethod
    def make_model_from_name(cls, type_name: str) -> CompositeModel:
        return cls.make_model_from_config(cls.make_config(type_name))

    @classmethod
    def add_to_registry(cls, variant: type):
        """add model to registry to allow instantiating with string

        TODO:
        - should we automatically add submodels to the registry?
        - eg, if we add Aero, then it should add the submodels required by it
        to the registry, to avoid having to add them 1 by 1

        """
        variant_name = variant.__name__

        if variant_name in cls._registry:
            raise ValueError(f"'{variant_name}' already exists in the registry.")
        cls._registry[variant_name] = variant

    @classmethod
    def remove_from_registry(cls, variant: type):
        variant_name = variant.__name__
        cls._check_exists(variant_name)
        cls._registry.pop(variant_name)


class CompositeModel:
    def __init__(
        self,
        model_config: Optional[ConfigTree] = None,
        params: Optional[ParameterTree] = None,
    ):
        self._submodels: Dict[str, CompositeModel] = {}
        self._params = {}  # here we only store direct model params

        if not model_config:
            model_config = self.get_recursive_default_model_config()

        # check the model config is called on the correct model
        expected_cls_str = type(self).__name__
        actual_cls_str = model_config.data
        if actual_cls_str != expected_cls_str:
            raise TypeError(
                f"Expects a config for {expected_cls_str} but got a config for {actual_cls_str}"
            )

        if not self.is_leaf():
            # FIXME: access private attribute
            self._build_submodels(model_config._children)

        if not params:
            params = self.get_recursive_default_params()

        self.set_recursive_params(params)

    @classmethod
    def get_submodel_names(cls) -> List[str]:
        """Return the names of the submodels.

        Returns:
            List[str]: names of the direct child submodels of the current model.
        """
        submodel_config = cls.get_default_submodel_config()
        return list(submodel_config.keys())

    @classmethod
    def is_leaf(cls):
        """A model is a leaf model if it doesn't have submodels."""
        return not (cls.get_submodel_names())

    @classmethod
    def get_default_submodel_config(cls) -> Dict[str, ConfigTree]:
        """Get the submodel config for the current submodel.

        This method needs to be implemented by the user for models with non-empty
        submodels.
        """
        return {}

    @classmethod
    def get_recursive_default_model_config(cls):

        submodel_config = cls.get_default_submodel_config()
        config_tree = ConfigTree(data=cls.__name__)
        if not cls.is_leaf():
            # FIXME: enforce submodel_config keys consistent with submodel_names
            for name, submodel_type in submodel_config.items():
                config_tree.add_child(
                    name=name, subtree=ModelMaker.make_config(submodel_type)
                )
        return config_tree

    def _build_submodels(self, submodel_config: Dict[str, ConfigTree]):
        """Build the direct submodels using given model configs."""
        for name in self.get_submodel_names():
            self._submodels[name] = ModelMaker.make_model_from_config(
                submodel_config[name]
            )

    def get_submodel(self, path, delimiter: str = ".") -> CompositeModel:
        """Retrieve a submodel at the given path.

        eg: model.get_submodel("aero.base") is equivalent to
        model._submodels["aero"]._submodels["base"]
        """

        path_to_submodel = path.split(delimiter)

        model = self
        for name in path_to_submodel:
            if name not in model._submodels:
                raise KeyError(
                    f"{name} is not a valid submodel of {type(model)}. "
                    "Valid ones are {model.get_submodel_names()}"
                )
            model = model._submodels[name]

        return model

    @classmethod
    def get_default_params(self) -> Dict[str, Any]:
        """Get the parameter for the current submodel.

        This method needs to be implemented by the user for models with non-empty
        parameters.

        This parameter should be a flat dictionary that represents the data of a model
        node. It does not include the parameters of the submodels.

        """
        return {}

    def get_recursive_default_params(self) -> ParameterTree:
        """Return the default parameter tree of the model

        This method must be called after the model is instantiated because it needs to
        know what submodels there are in the whole model tree.
        """
        param_tree = ParameterTree(data=self.get_default_params())
        if not self.is_leaf():
            for n, m in self._submodels.items():
                param_tree.add_child(name=n, subtree=m.get_recursive_default_params())
        return param_tree

    def set_recursive_params(self, params: ParameterTree):
        """Set the parameteres recursively including the children"""

        # The direct parameters of the model
        # NOTE: for the direct data at top level, we must copy, as it is a 1 level dict,
        # which if we don't copy, then we'll be making the new ParameterTree a mutable
        # copy of the old params!
        self._params = params.data.copy()

        # The parameters of the children
        if not self.is_leaf():
            for name, model in self._submodels.items():
                model.set_recursive_params(params.get_child(name))

    def get_recursive_params(self) -> ParameterTree:
        """Assmeble the parameter tree including the children"""

        # NOTE: for the direct data at top level, we must copy, as it is a 1 level dict,
        # which if we don't copy, then we'll be making the new ParameterTree a mutable
        # copy of the old params!
        param_tree = ParameterTree(data=self._params.copy())
        if not self.is_leaf():
            for n, m in self._submodels.items():
                param_tree.add_child(name=n, subtree=m.get_recursive_params())

        return param_tree
