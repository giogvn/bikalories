import pandas as pd
import json, os


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

    def read_routes_info(self, routes_dir: str) -> tuple:
        routes = []
        routes_info = {}
        for path in os.listdir(self.routes_dir):
            route_path = os.path.join(self.routes_dir, path)
            if os.path.isfile(route_path):
                route, route_info = self.read_route_from_json(route_path)
                route_id = route_info["json_name"]
                self.add_route_id_to_points(route_id, route)
                routes_info[route_id] = route_info
                routes.append(route)

        return routes, routes_info

    def create_routes_dataframe(self) -> pd.DataFrame:
        routes_df = pd.DataFrame()
        for route in self.routes:
            df = pd.DataFrame.from_records(route)
            routes_df = pd.concat([routes_df, df])

        return routes_df
