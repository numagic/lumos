import itertools
import json
import logging
import os

import pandas as pd

from lumos.models.composition import ModelMaker
from lumos.models.tires.utils import create_params_from_tir_file
from lumos.simulations.laptime_simulation import LaptimeSimulation

logger = logging.getLogger()


def _create_metric(name, unit, value):
    return {"name": name, "unit": unit, "value": value}


class MetricGenerator:
    def create_metrics(self):
        metrics = sweep_tracks()
        for backend, num_intervals in itertools.product(
            ["casadi", "jax"], [100, 1000, 10000]
        ):
            logger.info(
                f"profiling nlp with backend={backend}, num_intervals={num_intervals}"
            )
            metrics += profile_nlp(backend, num_intervals)

        with open("summary.json", "w+") as outfile:
            json.dump(metrics, outfile)


def sweep_tracks():
    TRACK_DIR = "data/tracks"

    track_files = [
        os.path.join(TRACK_DIR, f) for f in os.listdir(TRACK_DIR) if f.endswith(".csv")
    ]

    # Quickest way is to run with jax and only compiling for the first solve
    sim_config = LaptimeSimulation.get_sim_config(
        num_intervals=250,
        hessian_approximation="exact",
        is_cyclic=True,
        is_condensed=False,
        backend="jax",
        track=track_files[0],
        transcription="LGR",
    )

    model_config = ModelMaker.make_config("SimpleVehicleOnTrack")

    ocp = LaptimeSimulation(model_config=model_config, sim_config=sim_config)

    def _solve_with_track(track_file):
        logger.info(f"solving ltc for: {track_file}")
        ocp.set_track(track_file)

        x0 = ocp.get_init_guess()
        logger.info(f"Starting solve for {track_file}")
        solution, info = ocp.solve(
            x0,
            max_iter=200,
            print_level=4,
            print_timing_statistics="no",
            derivative_test="none",
            dual_inf_tol=1e-3,
            constr_viol_tol=1e-3,
        )
        info["laptime"] = ocp.dec_var_operator.get_var(
            solution, group="states", name="time", stage=-1
        )
        info["track"] = track_file
        logger.info(f"Maneuver time {info['laptime']:.3f} sec")

        COLUMNS_TO_EXTRACT = (
            "track",
            "status",
            "num_iter",
            "laptime",
            "status_msg",
        )

        result = {k: info[k] for k in COLUMNS_TO_EXTRACT}
        return result

    # Summary statistics
    results = pd.DataFrame.from_records([_solve_with_track(f) for f in track_files])
    is_success = results["status"] == 0
    num_success = is_success.sum()
    summary = pd.DataFrame(
        [
            {
                "num_success": num_success,
                "num_total": len(results),
                "success_pct": num_success / len(results) * 100,
                "avg_success_iter": results.loc[is_success, "num_iter"].mean(),
            }
        ]
    )

    # Artifacts files for the record
    results.to_csv("track_sweep_results.csv")
    summary.to_csv("track_sweep_summary.csv")

    # Create benchmark result for traclomg amd github page visualization
    # See: https://github.com/benchmark-action/github-action-benchmark
    # using customSmallerIsBetter, so need to make metrics also better when smaller
    metrics = [
        _create_metric("num_total", "-", len(results)),
        _create_metric("failure_pct", "%", (1 - num_success / len(results)) * 100),
        _create_metric(
            "avg_success_iter", "iter", results.loc[is_success, "num_iter"].mean()
        ),
    ]

    return metrics


def profile_nlp(backend: str, num_intervals: int):
    # Quickest way is to run with jax and only compiling for the first solve
    sim_config = LaptimeSimulation.get_sim_config(
        num_intervals=num_intervals,
        hessian_approximation="exact",
        is_cyclic=True,
        is_condensed=False,
        backend=backend,
        track="data/tracks/Catalunya.csv",
        transcription="LGR",
    )

    model_config = ModelMaker.make_config("SimpleVehicleOnTrack")
    ocp = LaptimeSimulation(model_config=model_config, sim_config=sim_config)

    x0 = ocp.get_init_guess()
    if backend == "jax":
        # Trigger jax jitting, to remove it from the profiling
        _ = ocp.profile(x0, repeat=1, hessian=True)
    results = ocp.profile(x0, repeat=10, hessian=True)

    metrics = []
    for name in [
        "nlp.objective",
        "nlp.gradient",
        "nlp.constraints",
        "nlp.jacobian",
        "nlp.hessian",
    ]:
        metrics.append(
            _create_metric(
                ".".join([backend, str(num_intervals), name]), "sec", results[name]
            )
        )

    return metrics


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    generator = MetricGenerator()
    generator.create_metrics()
