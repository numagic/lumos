from jax.config import config

# By default we use 64bit as over/underflow are quite likely to happen with 32bit and
# 2nd derivative autograd, without a lot of careful management...
config.update("jax_enable_x64", True)

# For initial phase, we also report verbosely if jax is recompiling.
config.update("jax_log_compiles", 1)
