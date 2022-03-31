import glob
import os
import unittest
from tempfile import TemporaryDirectory

import numpy as np
import pandas as pd
from pyarrow import parquet as pq

from lumos.simulations.laptime_simulation import LaptimeSimulation


class TestOCPLogging(unittest.TestCase):
    num_iter: int = 5

    def test_logging(self):
        with TemporaryDirectory() as temp_dir:
            # FIXME: this is unneceesarily expensive to use an LTC
            # But we have only implemented logging for the FixedGrid subclass only
            # at the moment...
            ocp = LaptimeSimulation(
                sim_config=LaptimeSimulation.get_sim_config(
                    track="data/tracks/Catalunya.csv",
                    backend="casadi",
                    num_intervals=100,
                    logging_config={
                        "results_dir": temp_dir,  # store in a new directory at current directory
                        "sim_name": "Temp",
                        "log_final_iter": True,
                        "log_metrics_history": True,
                        "log_every_nth_iter": 1,  # if 0, logging is off
                    },
                )
            )

            x0 = ocp.get_init_guess()

            solution, info = ocp.solve(x0, max_iter=self.num_iter, print_level=0,)

            # Check the number of log files are correct
            # There should be:
            # - 1 all_iters parquet
            # - 1 final_iter csv
            # - 1 metrics history csv
            expected_num_csv = 2
            expected_num_parquet = 1
            csv_files = glob.glob(os.path.join(ocp.logging_dir, "*.csv"))
            self.assertEqual(len(csv_files), expected_num_csv)

            parquet_files = glob.glob(os.path.join(ocp.logging_dir, "*.parquet"))
            self.assertEqual(len(parquet_files), expected_num_parquet)

            # Ensure the max constraiont violation agrees with inf_pr
            combined_df = pq.read_pandas(
                os.path.join(ocp.logging_dir, "all_iters.parquet")
            ).to_pandas()
            metrics_history_df = pd.read_csv(
                os.path.join(ocp.logging_dir, "metrics_history.csv")
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
                    metrics_history_df["max_violation_distance"][it],
                    iter_df["distance"][idx],
                )
