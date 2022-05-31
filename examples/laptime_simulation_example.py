import logging
import os

from lumos.models.composition import ModelMaker
from lumos.models.simple_vehicle_on_track import SimpleVehicleOnTrack
from lumos.models.tires.utils import create_params_from_tir_file
from lumos.simulations.laptime_simulation import LaptimeSimulation

logger = logging.getLogger(__name__)


# FIXME: hardcoded relative track directory
TRACK_DIR = "data/tracks"


def main():
    is_cyclic = True
    track = "Catalunya"
    track_file = os.path.join(TRACK_DIR, track + ".csv")

    sim_config = LaptimeSimulation.get_sim_config(
        num_intervals=250,
        hessian_approximation="exact",
        is_cyclic=is_cyclic,
        is_condensed=False,
        backend="casadi",
        track=track_file,
        transcription="LGR",
        logging_config={
            "results_dir": "results",  # store in a new directory at current directory
            "sim_name": track,
            "log_final_iter": False,
            "log_metrics_history": False,
            "log_every_nth_iter": 0,  # if 0, logging is off
        },
    )

    model_config = SimpleVehicleOnTrack.get_recursive_default_model_config()

    # EXAMPLE: change tire model
    # model_config.replace_subtree(
    #     "vehicle.tire", ModelMaker.make_config("PerantoniTire")
    # )

    # EXMAPLE: change an aero model
    # model_config.replace_subtree("vehicle.aero", ModelMaker.make_config("MLPAero"))

    model = SimpleVehicleOnTrack(model_config=model_config)
    params = model.get_recursive_default_params()

    # Example of changing model parameters
    # TODO: an issue here is that we need to instantiate the model first to get params
    # but that's unavoidable because without the model, we don't even know the tree
    # structure of all the submodels, let alone the default parameters.
    # params.set_param("vehicle.vehicle_mass", 1700)

    # Example: change tire parameters
    sharpened_params = create_params_from_tir_file("data/tires/sharpened.tir")
    # FIXME: here we're using private methods. We should probably add a method to change
    # the parameters of an entire node in the ParameterTree
    for c in ["fl", "fr", "rl", "rr"]:
        submodel_path = "vehicle.tire_" + c
        tire_params = params._get_subtree(submodel_path)
        tire_params._data = sharpened_params
        params.replace_subtree(submodel_path, tire_params)

    ocp = LaptimeSimulation(
        model_params=params, model_config=model_config, sim_config=sim_config
    )

    x0 = ocp.get_init_guess()
    ocp.profile(x0, repeat=10, hessian=True)

    solution, info = ocp.solve(
        x0,
        max_iter=200,
        print_level=5,
        print_timing_statistics="yes",
        print_info_string="yes",
        derivative_test="none",
        dual_inf_tol=1e-3,
        constr_viol_tol=1e-3,
    )
    total_time = ocp.dec_var_operator.get_var(
        solution, group="states", name="time", stage=-1
    )
    logger.info(f"Maneuver time {total_time:.3f} sec")

    return

    # Change param and solve again
    ocp.modify_model_param("vehicle.vehicle_mass", 2100.0)
    solution, info = ocp.solve(
        solution,
        max_iter=200,
        print_level=5,
        print_timing_statistics="yes",
        print_info_string="yes",
        derivative_test="none",
        dual_inf_tol=1e-3,
        constr_viol_tol=1e-3,
    )
    total_time = ocp.dec_var_operator.get_var(
        solution, group="states", name="time", stage=-1
    )
    logger.info(f"Maneuver time {total_time:.3f} sec")

    # # Tighten slip bound, solve again
    # for c in ["fl", "fr", "rl", "rr"]:
    #     for s in range(ocp.num_stages):
    #         ocp.set_con_output_bounds("slip_ratio_" + c, stage=s, bounds=(-0.1, 0.1))
    #         ocp.set_con_output_bounds(
    #             "slip_angle_" + c, stage=s, bounds=(-np.deg2rad(10), np.deg2rad(10))
    #         )

    # solution, info = ocp.solve(
    #     solution,
    #     lagrange=info["mult_g"],
    #     zl=info["mult_x_L"],
    #     zu=info["mult_x_U"],
    #     max_iter=200,
    #     print_level=5,
    #     print_timing_statistics="yes",
    #     print_info_string="yes",
    #     derivative_test="none",
    #     dual_inf_tol=1e-3,
    #     constr_viol_tol=1e-3,
    # )
    # total_time = ocp.dec_var_operator.get_var(
    #     solution, group="states", name="time", stage=-1
    # )

    # logger.info(f"Maneuver time {total_time:.3f} sec")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
