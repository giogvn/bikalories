import sys

sys.path.append("..")
from data_prep.dataframe_creator import DataFrameCreator
from route_analyzer import RouteAnalyzer

if __name__ == "__main__":
    json_dir = "../data/json_data/"
    route_id = "Workout--2023-01-22--11-49-53.json"
    df = DataFrameCreator(json_dir).create_routes_dataframe()
    analyzer = RouteAnalyzer(df)
    print(analyzer.detect_slopes(route_id))
