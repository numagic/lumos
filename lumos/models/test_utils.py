import logging
import os
import unittest
import uuid
from functools import wraps
from typing import List

import numpy as np
from casadi import MX, Function

import lumos.numpy as lnp


logger = logging.getLogger(__name__)


def use_backends(backends: List[str]):
    """Decortator to run tests with different backends.

    This is a workaround of an issue with parameterized_class + inheritance,

    Parameterized_class works by doing the following:
    1) add new classes with subfix to current module
    2) remove 'test_' method from the original class, so the original class doesn't get to run.
    see: https://github.com/wolever/parameterized/blob/0403e891d9a6ec5fa77c0e200f31e1298fcacbc9/parameterized/parameterized.py#L606
    Problem is: if the original class is inherited, the deletion doesn't happen because
    those those 'test_' methods are defined in its parent class!

    TODO: currently there are still issues compared to using parameterized
    1) using 1 test instead of n tests, so as soon as one backend fails, we stop running
    the rest of the tests
    2) more difficult to tell which backend fails and why

    """

    def decorator(fn):
        @wraps(fn)
        def wrapped(self, *args, **kwargs):
            original_backend = lnp.get_backend()
            for i, backend in enumerate(backends):
                with self.subTest(i=i):
                    lnp.set_backend(backend)
                    logger.info(f"Running with {backend} backend")
                    try:
                        fn(self, *args, **kwargs)
                    except AssertionError as ae:
                        # Catch assertion failure seperately so it counts as 'failed'
                        # instead of 'errors'
                        raise ae
                    except Exception as e:
                        # Throw a mesage to highlight with which backend the test fails
                        # (This is something we would get from parameterlized as it creates
                        # separate tests)
                        # using raise from, see: https://stackoverflow.com/a/29442282
                        raise Exception(f"Error with {backend} backend") from e
                    finally:
                        # Return to original backend
                        # TODO: maybe this should be a context manager?
                        lnp.set_backend(original_backend)

        return wrapped

    return decorator


class BaseModelTest:
    ModelClass: type
    # this defines the variable groups that need to be passed to model forward call
    forward_arguments: List[str] = ["inputs"]
    need_mesh_input: bool = False

    @classmethod
    def setUpClass(cls):
        cls.model = cls.ModelClass()
        cls.params = cls.model.get_recursive_params()

        cls.args_dict = {
            g: {n: 0.1 for n in cls.model.get_group_names(g)}
            for g in cls.forward_arguments
        }

        if cls.need_mesh_input:
            cls.args_dict["mesh"] = 0.0

    @use_backends(backends=["jax", "numpy", "casadi"])
    def test_forward(self):
        """
        smoke test to see if forward call throws an error.
        """

        # TODO: Casadi behaves more like 'typebroadcast', it can take in float and
        # return float, but that's not what we need. We want to make sure t works with
        # Casadi symbolic variables. (But maybe if the test works with float, then it
        # will work with symbolic variables as well?)
        def _nested_dict_to_mx(d):
            if isinstance(d, dict):
                return {k: _nested_dict_to_mx(v) for k, v in d.items()}
            else:
                return MX(d)

        if lnp.get_backend() == "casadi":
            args_dict = _nested_dict_to_mx(self.args_dict)
        else:
            args_dict = self.args_dict

        # Calling without external parameters
        out = self.model.forward(**args_dict)

        logger.debug(f"outputs is of type {type(out.outputs)}")

        # Calling with external parameters
        _ = self.model.apply_and_forward(**args_dict, params=self.params)

    # TODO: we should impement a model auto-diff test to check if auto-diff works
    # (should we also check the autodiff accuracy?)
    @unittest.skip("To be implemented")
    def test_backward(self):
        # TODO: should backward be abstracted to model level? But numpy model wouldn't
        # have an autodiff tool. In addition, the original target is to only use jax
        # for autodiff (and casadi could be used for benchmark only)
        pass

    # TODO: code generation should only be possible for casadi backend. Where should we
    # put the test?
    # TODO: maybe for everymodel, we just want to test if it can generate code with
    # casadi, but don't touch anything else to do with Casadi?
    @use_backends(backends=["casadi"])
    def test_code_generation(self):
        # Code generation requires using the array inputs interface
        args_dict = {
            k: MX.sym("mesh") if k == "mesh" else MX.sym(k, self.model.get_num_vars(k))
            for k, v in self.args_dict.items()
        }

        # TODO: need to add parameter to the function
        f = Function(
            "f",
            list(args_dict.values()),
            list(self.model.forward_with_arrays(**args_dict)),
        )

        # call the function with concrete values
        args_dict = {
            k: v if k == "mesh" else self.model.make_vector(k, **v)
            for k, v in self.args_dict.items()
        }
        _ = f.call(list(args_dict.values()))

        # Note: name must start with a letter, have no underscore, doesn't
        # overlap with some special names. So can't pass in full path name.
        # see: https://github.com/casadi/casadi/blob/8d0f80a4d0fe2054384bfb9748f7a0f6bae540ff/casadi/core/function.cpp#L1167
        # Due to such restrictions, we must generate and fix the name by hand, and
        # operate in current directory.

        file_name = f.fix_name(uuid.uuid4().hex) + ".c"
        f.generate(file_name)
        # At the moment only check if the generated code has more than 10 lines.
        # TODO:compile and run generated code. Need to configure compiler
        with open(file_name, "r") as f:
            file_length = len(f.read())
            self.assertTrue(file_length > 10)
            logger.debug(f"file length = {file_length} lines")

        # Manually clean up
        os.remove(file_name)


class BaseStateSpaceModelTest(BaseModelTest):
    forward_arguments: List[str] = ["inputs", "states"]
    need_mesh_input = True

    def _forward_euler(self, init_states, inputs, time_step, num_steps):
        """Helper to run forward euler with a fixed inputs for a few steps"""

        # Ensure we don't modify the initial states
        states = dict(init_states)
        for step in range(num_steps):
            model_return = self.model.forward(states, inputs, step * time_step)
            for k in states:
                states[k] += model_return.states_dot[k] * time_step

        return states, model_return.outputs


if __name__ == "__name__":
    unittest.main()
