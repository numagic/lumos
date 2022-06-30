import sys

import scipy.io as sio
from lumos.models.composition import ModelMaker


def export_c_code_and_data(file_name: str, options, includes):
    """Export a state space model as c-code and data from recorded I/O"""
    # Create the model
    model = ModelMaker.make_model_from_name("SimpleVehicle")

    # Export c-code
    model.export_c_code(f"{file_name}.c", options=options, includes=includes)

    # Export some data that can be used for testing (to check if execution in mex gives
    # the same results as in python)
    params = model.get_recursive_params()
    flat_params, _ = params.tree_ravel()

    vx, vy, yaw_rate = 40.0, 0.0, 0.0
    no_slip_omega = vx / model._params["rolling_radius"]
    states = model.make_vector(
        "states",
        vx=vx,
        vy=vy,
        yaw_rate=yaw_rate,
        wheel_speed_fl=no_slip_omega,
        wheel_speed_fr=no_slip_omega,
        wheel_speed_rl=no_slip_omega,
        wheel_speed_rr=no_slip_omega,
    )

    inputs = model.make_vector(
        "inputs", throttle=0.2, brake=0.0, steer=0.01, ax=0, ay=0
    )
    mesh = 0.0

    model_return = model.forward_with_arrays(states, inputs, mesh)

    export_dict = model_return._asdict()
    export_dict.update(
        {"states": states, "inputs": inputs, "mesh": mesh, "params": flat_params}
    )

    sio.savemat(f"{file_name}.mat", export_dict)


if __name__ == "__main__":
    # Takes 1 commandline input for the file name
    # sys.argv is what follows 'python3'

    # For matlab mex function
    options = {"mex": True}
    includes = []

    # For s-function as described in: https://web.casadi.org/blog/s-function/
    # options = {
    #     "casadi_real": "real_T",
    #     "casadi_int": "int_T",
    #     "with_header": True,
    # }
    # includes = ["simstruc.h"]
    export_c_code_and_data(sys.argv[1], options, includes)
