# TODO: understand why we need this. Without this, the sub-packages can't be found!
# It's most likely a import 'trap' introduced after 3.3, but what's strange is that it
# causes a problem with 3.7 but not with 3.9
import lumos.numpy as lnp
