import scipy.io as sio
from lumos.models.composition import ModelMaker


def export_c_mex_and_data():
    # Create the model
    model = ModelMaker.make_model_from_name("SimpleVehicle")

    # Export c-code
    model.export_c_mex("forward.c")

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

    sio.savemat("forward_data.mat", export_dict)

    pass


if __name__ == "__main__":
    export_c_mex_and_data()
