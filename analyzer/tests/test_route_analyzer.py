import os, sys
from parameterized import parameterized

sys.path.append("..")
sys.path.append("../..")

import unittest
from pathlib import Path
from route_analyzer import RouteAnalyzer
from data_prep.dataframe_creator import DataFrameCreator
import numpy as np


def get_all_routes_files_names(routes_dir: str) -> list:
    routes_files_names = []
    for path in os.listdir(routes_dir):
        route_path = os.path.join(ROUTES_DIR, path)
        if os.path.isfile(route_path):
            routes_files_names.append(path)
    return routes_files_names


TOTAL_DIST_TOL = 20
ROUTES_DIR = Path("../../data/json_data")
ROUTES_FILES = get_all_routes_files_names(ROUTES_DIR)
ROUTES_DF_CREATOR = DataFrameCreator(ROUTES_DIR)
ROUTES_DF = ROUTES_DF_CREATOR.create_routes_dataframe()
ANALYZER = RouteAnalyzer(ROUTES_DF)


class TestRouteAnalyzer(unittest.TestCase):
    global ROUTES_DIR, ROUTES_DF

    @parameterized.expand(ROUTES_FILES)
    def test_route_total_dist_calculus(self, route_id: str):
        (
            acc_dist,
            acc_time,
        ) = ANALYZER.calculate_route_acc_dists_and_times(route_id)
        routes_info = ROUTES_DF_CREATOR.read_routes_info(route_id)[1]
        route_dist = routes_info[route_id]["distance(m)"]
        self.assertTrue(abs(acc_dist[-1] - route_dist) < TOTAL_DIST_TOL)

    @parameterized.expand(ROUTES_FILES)
    def OFF_test_route_total_time_calculus(self, route_id: str):
        (
            acc_dist,
            acc_time,
        ) = ANALYZER.calculate_route_acc_dists_and_times(route_id)
        routes_info = ROUTES_DF_CREATOR.read_routes_info(route_id)[1]
        route_time = routes_info[route_id]["sportTime(s)"]
        self.assertTrue(abs(acc_time[-1] - route_time) < TOTAL_DIST_TOL)


if __name__ == "__main__":
    verbosity = 2
    runner = unittest.TextTestRunner(verbosity=verbosity)
    unittest.main(testRunner=runner)
