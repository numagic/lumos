import itertools
import glob
import os
import unittest
from tempfile import TemporaryDirectory

import numpy as np
import pandas as pd
from pyarrow import parquet as pq
from parameterized import parameterized

from lumos.optimal_control.config import LoggingConfig
from lumos.simulations.drone_simulation import DroneSimulation
from lumos.simulations.laptime_simulation import LaptimeSimulation


class TestOCPLogging(unittest.TestCase):
    num_iter: int = 5
    SimClass: type = DroneSimulation

    def _run_and_log(
        self,
        results_dir: str,
        log_every_nth_iter: int,
        drone_or_ltc: str = "drone",
        is_condensed: bool = False,
    ):
        logging_config = LoggingConfig(
            sim_name="temp",
            results_dir=results_dir,
            log_every_nth_iter=log_every_nth_iter,
        )
        if drone_or_ltc == "drone":
            sim_config = DroneSimulation.get_sim_config(
                backend="casadi",
                num_intervals=100,
                is_condensed=is_condensed,
                logging_config=logging_config,
            )
            ocp = DroneSimulation(sim_config=sim_config)
        else:
            sim_config = LaptimeSimulation.get_sim_config(
                track="data/tracks/Catalunya.csv",
                backend="casadi",
                num_intervals=100,
                is_condensed=is_condensed,
                logging_config=logging_config,
            )
            ocp = LaptimeSimulation(sim_config=sim_config)

        x0 = ocp.get_init_guess()
        solution, info = ocp.solve(x0, max_iter=self.num_iter, print_level=0,)

        return ocp.logging_dir

    @parameterized.expand(
        [[0, 2, 0], [1, 2, 1], [10, 2, 1],]
    )
    def test_correct_files_are_created(
        self, log_every_nth_iter, expected_num_csv, expected_num_parquet
    ):
        with TemporaryDirectory() as temp_dir:
            logging_dir = self._run_and_log(
                results_dir=temp_dir, log_every_nth_iter=log_every_nth_iter
            )

            # Check the number of log files are correct
            # one csv for final results and 1 csv for metrics history should always be
            # written
            # log_every_nth_iter = 0 -> no parquet files for all iterations
            csv_files = glob.glob(os.path.join(logging_dir, "*.csv"))
            self.assertEqual(len(csv_files), expected_num_csv)

            parquet_files = glob.glob(os.path.join(logging_dir, "*.parquet"))
            self.assertEqual(len(parquet_files), expected_num_parquet)

    def test_no_logging(self):
        """Just a smoke test. Kind of difficult to verify it doesn't produce anything"""
        sim_config = DroneSimulation.get_sim_config(
            backend="casadi", num_intervals=100,
        )
        ocp = DroneSimulation(sim_config=sim_config)
        x0 = ocp.get_init_guess()
        solution, info = ocp.solve(x0, max_iter=self.num_iter, print_level=0)

    @parameterized.expand(itertools.product(("drone", "ltc"), (True, False)))
    def test_log_every_iter(self, drone_or_ltc, is_condensed):
        with TemporaryDirectory() as temp_dir:
            logging_dir = self._run_and_log(
                is_condensed=is_condensed,
                results_dir=temp_dir,
                log_every_nth_iter=1,
                drone_or_ltc=drone_or_ltc,
            )

            # Check the number of log files are correct
            # There should be:
            # - 1 all_iters parquet
            # - 1 final_iter csv
            # - 1 metrics history csv
            expected_num_csv = 2
            expected_num_parquet = 1
            csv_files = glob.glob(os.path.join(logging_dir, "*.csv"))
            self.assertEqual(len(csv_files), expected_num_csv)

            parquet_files = glob.glob(os.path.join(logging_dir, "*.parquet"))
            self.assertEqual(len(parquet_files), expected_num_parquet)

            # Ensure the max constraiont violation agrees with inf_pr
            combined_df = pq.read_pandas(
                os.path.join(logging_dir, "all_iters.parquet")
            ).to_pandas()
            metrics_history_df = pd.read_csv(
                os.path.join(logging_dir, "metrics_history.csv")
            )

            # FIXME: it's not nice to get constraint names from here...
            con_names = [c for c in combined_df.columns if "_con." in c]
            for it in range(self.num_iter):
                iter_df = combined_df.loc[combined_df["iter"] == it]
                idx, column = iter_df[con_names].abs().stack().idxmax()
                self.assertAlmostEqual(
                    metrics_history_df["inf_pr"][it], np.abs(iter_df[column][idx])
                )
                self.assertEqual(
                    metrics_history_df["max_violation_con_name"][it], column
                )
                self.assertAlmostEqual(
                    metrics_history_df["max_violation_mesh"][it], iter_df["mesh"][idx],
                )
