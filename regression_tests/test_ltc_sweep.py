import json
import logging
import os
from unittest import TestCase

import pandas as pd

from lumos.models.composition import ModelMaker
from lumos.models.tires.utils import create_params_from_tir_file
from lumos.simulations.laptime_simulation import LaptimeSimulation

logger = logging.getLogger()


class TestTrackSweep(TestCase):
    def test_sweep(self):

        TRACK_DIR = "data/tracks"

        track_files = [
            os.path.join(TRACK_DIR, f)
            for f in os.listdir(TRACK_DIR)
            if f.endswith(".csv")
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

        # Change the tire to sharpened
        model = ModelMaker.make_model_from_config(model_config)
        params = model.get_recursive_default_params()
        sharpened_params = create_params_from_tir_file("data/tires/sharpened.tir")
        # FIXME: here we're using private methods. We should probably add a method to change
        # the parameters of an entire node in the ParameterTree
        tire_params = params._get_subtree("vehicle.tire")
        tire_params._data = sharpened_params
        params.replace_subtree("vehicle.tire", tire_params)

        ocp = LaptimeSimulation(
            model_params=params, model_config=model_config, sim_config=sim_config
        )

        def _solve_with_track(track_file):
            ocp._build_track_from_file(track_file)
            ocp.update_track_bounds()

            x0 = ocp.get_init_guess()
            logger.info(f"Starting solve for {track_file}")
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

        results = pd.DataFrame()
        for f in track_files:
            # result = _solve_with_track(f)
            # HACK: remove this quick test hack
            import random

            result = {
                "track": f,
                "status": random.randint(0, 1),
                "num_iter": random.randint(10, 30),
                "laptime": random.random(),
                "status_msg": "bla",
            }

            results = results.append(result, ignore_index=True)

        # Summary statistics
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

        results.to_csv("results.csv")
        summary.to_csv("summary.csv")

        # HACK: copy paste now, but merge with df creation later
        def _create_metric(name, unit, value):
            return {"name": name, "unit": unit, "value": value}

        # using customSmallerIsBetter, so need to make metrics also better when smaller
        metrics = [
            _create_metric("num_total", "-", int(num_success)),
            _create_metric("failure_pct", "%", (1 - num_success / len(results)) * 100),
            _create_metric(
                "avg_success_iter", "iter", results.loc[is_success, "num_iter"].mean()
            ),
        ]

        with open("summary.json", "w") as outfile:
            json.dump(metrics, outfile)
        pass
