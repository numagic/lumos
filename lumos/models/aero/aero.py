import numpy as np

from lumos.models.ml import gp, mlp
from lumos.models.base import model_io, Model, ModelReturn

# NOTE: we just put some dummy inputs here for now.
@model_io(
    inputs=("front_ride_height", "rear_ride_height", "yaw"), outputs=("Cx", "Cy", "Cz")
)
class AeroModel(Model):
    # FIXME: there are a few implicit limitations:
    # 2) the parameter size for some model (gp, mlp), depends on the I/O size, we should
    # implement checks.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ConstAero(AeroModel):
    @classmethod
    def get_default_params(self):
        return {"Cx": 0.6, "Cy": 0.0, "Cz": 1.9}

    def forward(self, inputs):
        return ModelReturn(outputs=self._params)


class GPAero(AeroModel):
    # FIXME: we should pass these as configuration parameters for the model instance.
    num_points = 1024

    @classmethod
    def get_default_params(cls):
        # NOTE: we don't use the property methods here because special care is needed to
        # use property method inside a class method
        # see: https://stackoverflow.com/questions/128573/using-property-on-classmethods
        #
        # While we can make these class method properties for now, but in the future
        # we might want to make the I/O names dynamic that are only defined after the
        # object is instantiated (for example, passing all submodel outputs as a part of
        # parent model outputs)
        num_inputs = len(cls.get_direct_group_names("inputs"))
        num_outputs = len(cls.get_direct_group_names("outputs"))
        return {
            "gp_points": np.random.randn(cls.num_points, num_inputs),
            "alpha": np.random.randn(num_outputs, cls.num_points),
        }

    def forward(self, inputs):
        array_inputs = self.make_vector("inputs", **inputs)
        coeff = gp(array_inputs, self._params["gp_points"], self._params["alpha"])

        outputs = self.make_dict(
            "outputs", **{n: coeff[idx] for idx, n in enumerate(self.names.outputs)}
        )

        return ModelReturn(outputs=outputs)


class MLPAero(AeroModel):
    num_layers = 3
    layer_dim = 128

    weights_prefix = "weights_layer"  # parameter prefix for a layer's weights

    @classmethod
    def _list_to_dict(cls, weights: list):
        return {f"weights_layer_{i}": w for i, w in enumerate(weights)}

    @classmethod
    def _dict_to_list(cls, weights: dict):
        # NOTE: this requires ordered dict, which is default in python for 3.6+
        # We rely on the ordered dict instead of the number in name
        return [v for k, v in weights.items() if k.startswith(cls.weights_prefix)]

    @classmethod
    def get_default_params(cls):
        num_inputs = len(cls.get_direct_group_names("inputs"))
        num_outputs = len(cls.get_direct_group_names("outputs"))

        layers_dim = [cls.layer_dim] * cls.num_layers
        ins = [num_inputs] + layers_dim[:-1]
        outs = layers_dim
        # NOTE: we make the default parameters small so that it doesn't affect vehicle
        # behaviour too much (so we can more easilyi assess runtime and convergence of
        # a random aero map with MLP)
        weights = [1e-3 * np.random.randn(od, id) for id, od in zip(ins, outs)]

        # Final layer
        weights.append(np.random.randn(num_outputs, layers_dim[-1]))

        weights_dict = cls._list_to_dict(weights)

        params = {"air_density": 1.225}
        params.update(weights_dict)
        return params

    def forward(self, inputs):
        # NOTE: at the moment we only support parameters of a flat dict where the key is
        # a string, and the value a scalar or an array. And since Casadi only supports
        # up to 2d array (matrices), this present an issue for MLP params.
        #
        # MLP params are at least 3 dimensional, we could do list of weights (if weights)
        # are 2d only, but that breaks the flat dict requirement on values.
        array_inputs = self.make_vector("inputs", **inputs)

        coeff = mlp(array_inputs, weights=self._dict_to_list(self._params))
        outputs = self.make_dict(
            "outputs", **{n: coeff[idx] for idx, n in enumerate(self.names.outputs)}
        )
        return ModelReturn(outputs=outputs)
