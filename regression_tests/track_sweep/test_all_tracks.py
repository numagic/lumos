import logging
import os
from unittest import TestCase

import pandas as pd

from lumos.models.composition import ModelMaker
from lumos.simulations.laptime_simulation import LaptimeSimulation

logger = logging.getLogger()


class TestLapsimOnTrack(TestCase):
    def test_ltc(self):

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
        ocp = LaptimeSimulation(model_config=model_config, sim_config=sim_config)

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
            result = _solve_with_track(f)
            # import random

            # result = {
            #     "track": f,
            #     "status": random.randint(0, 1),
            #     "num_iter": random.randint(10, 30),
            #     "laptime": random.random(),
            #     "status_msg": "bla",
            # }
            # results = results.append(result, ignore_index=True)

        # Summary statistics
        summary = pd.DataFrame(
            [
                {
                    "num_success": (results["status"] == 1).sum(),
                    "num_total": len(results),
                    "success_pct": (results["status"] == 1).sum() / len(results) * 100,
                    "avg_success_iter": results.loc[
                        results["status"] == 1, "num_iter"
                    ].mean(),
                }
            ]
        )

        OUTPUT_DIR = "ltc_sweep"
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        results.to_csv(os.path.join(OUTPUT_DIR, "results.csv"))
        summary.to_csv(os.path.join(OUTPUT_DIR, "summary.csv"))

        pass
