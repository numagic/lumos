import logging
import re
from typing import Any, Dict

logger = logging.getLogger(__name__)


def read_tir_file(file_path: str) -> Dict[str, Any]:
    """Create tire data dictionary from Pacejka .tir file.

    Args:
        file_path (str): tir file path.
    Returns:
        Dict[str, Any]: flat parameter dicitonary contianing only numeric data.

    Typical data file looks like:

    .
    .
    .
    [OVERTURNING_COEFFICIENTS]
    QSX2                     = 0.6038            $Camber induced overturning couple         
    QSX3                     = 0.025405          $Fy induced overturning couple    
    .
    .
    .
    """

    params = {}
    with open(file_path, "r") as f:
        tir_data = f.readlines()

        for line in tir_data:
            # TODO: this is pretty flaky and would break if somebody puts a "=" into
            # comments
            if "=" in line:
                name, val, *_ = re.split("[=$]", line.replace(" ", ""))
                try:
                    params[name] = float(val)
                except ValueError:
                    logger.debug(f"{name} is not a numeric value and is discarded.")

    return params


# TODO: at the moment, the params can actually have different fields depending on the
# form of the tir file! This makes jitting difficult (because the input pytree changes)
def create_params_from_tir_file(tir_file):
    """Augment tir file params with some compute params."""
    params = read_tir_file(tir_file)
    params.update(
        {
            # Used to avoid low speed singularity, [Eqn (4.E6a) Page 178 - Book]
            "epsilonv": 1e-6,
            "epsilonx": 1e-3,
            "epsilonk": 1e-6,
            "epsilony": 1e-3,
        }
    )
    return params
