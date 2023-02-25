import pandas as pd
from geopy import distance
import json, os
from datetime import datetime


class DataFrameCreator:
    def __init__(self, routes_dir: str):
        self.routes_dir = routes_dir
        self.routes, self.routes_info = self.read_routes_info(routes_dir)

    def read_route_from_json(
        self, json_path: str, route_key: str = "route", info_key: str = "general_info"
    ) -> list:
        with open(json_path, "r") as f:
            data = json.load(f)
            route = data[route_key]
            route_info = data[info_key]
        return route, route_info

    def add_route_id_to_points(self, route_id: int, route: list) -> None:
        for point in route:
            point["route_id"] = route_id

    def read_routes_info(self, routes_dir: str) -> list:
        routes = []
        routes_info = {}
        route_id = 0
        for path in os.listdir(self.routes_dir):
            route_path = os.path.join(self.routes_dir, path)
            if os.path.isfile(route_path):
                route, route_info = self.read_route_from_json(route_path)
                self.add_route_id_to_points(route_id, route)
                routes_info[route_id] = route_info
                routes.append(route)
                route_id += 1
        return routes, routes_info

    def create_routes_dataframe(self) -> pd.DataFrame:
        routes_df = pd.DataFrame()
        for route in self.routes:
            df = pd.DataFrame.from_records(route)
            routes_df = pd.concat([routes_df, df])

        return routes_df


class RouteAnalyzer:
    def __init__(self, routes: pd.DataFrame) -> None:
        self.routes_df = routes

    def get_distance_between_coords(self, coord1: tuple, coord2: tuple) -> float:
        return distance.distance(coord1, coord2).meters

    def calculate_route_total_dist_and_time(self, route_id: int = 0) -> list:
        distances = [(0, 0)]
        total_dist = 0
        total_time = 0
        route = self.routes_df.loc[self.routes_df["route_id"] == route_id]

        for index, row in route.iterrows():
            if index == route.index[-1]:
                break
            points = route.iloc[index : index + 2]
            point1 = points.iloc[0]
            point2 = points.iloc[1]

            coord1 = point1["latitude"], point1["longitude"]
            coord2 = point2["latitude"], point2["longitude"]

            time1 = datetime.fromtimestamp(point1["timestamp"] / 1000)
            time2 = datetime.fromtimestamp(point2["timestamp"] / 1000)

            distance = self.get_distance_between_coords(coord1, coord2)
            delta_t = (time2 - time1).total_seconds()

            total_dist += distance
            total_time += delta_t
            distances.append((total_dist, total_time))
        return distances


if __name__ == "__main__":
    routes_dir = "../data/json_data/"
    df_creator = DataFrameCreator(routes_dir)
    df = df_creator.create_routes_dataframe()
    route_analyzer = RouteAnalyzer(df)
    calc_diff = []
    for route_id in range(df["route_id"].max()):
        total_route = route_analyzer.calculate_route_total_dist_and_time(route_id)
        break
