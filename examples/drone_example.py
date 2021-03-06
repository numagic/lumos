import logging
import numpy as np
from lumos.optimal_control.config import LoggingConfig
from lumos.simulations.drone_simulation import DroneSimulation

logger = logging.getLogger(__name__)


def main():
    # h_approx = "limited-memory"
    h_approx = "exact"

    ocp = DroneSimulation(
        sim_config=DroneSimulation.get_sim_config(
            num_intervals=99,
            hessian_approximation=h_approx,
            backend="casadi",
            transcription="LGR",
            is_condensed=False,
            logging_config=LoggingConfig(
                sim_name="drone", results_dir="results", log_every_nth_iter=0
            ),
        )
    )

    x0 = ocp.get_init_guess()

    solution, info = ocp.solve(
        x0,
        max_iter=200,
        print_level=5,
        print_timing_statistics="no",
        derivative_test="none",
    )

    total_time = ocp.get_total_time(solution)
    final_theta = ocp.dec_var_operator.get_var(
        solution, group="states", name="theta", stage=-1
    )

    logger.info(f"Maneuver time {total_time:.3f} sec")
    logger.info(f"Final theta {final_theta:.2f} rad")
    logger.info(f"Final sin(theta) {np.sin(final_theta):.2f}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
