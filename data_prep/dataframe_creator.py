import pandas as pd
import json, os


class DataFrameCreator:
    def __init__(self, routes_dir: str):
        self.routes_dir = routes_dir
        self.routes = self.create_list_of_routes(routes_dir)
        pass

    def read_route_from_json(self, json_path: str, key: str = "route") -> list:
        with open(json_path, "r") as f:
            out = json.load(f)[key]
        return out

    def add_route_id_to_points(self, route_id: int, route: list) -> None:

        for point in route:
            point["route_id"] = route_id

    def create_list_of_routes(self, routes_dir: str) -> list:
        out = []
        route_id = 0
        for path in os.listdir(self.routes_dir):
            route_path = os.path.join(self.routes_dir, path)
            if os.path.isfile(route_path):
                route = self.read_route_from_json(route_path)
                self.add_route_id_to_points(route_id, route)
                out.append(route)
                route_id += 1
        return out

    def create_routes_dataframe(self) -> pd.DataFrame:
        routes_df = pd.DataFrame()
        for route in self.routes:
            df = pd.DataFrame.from_records(route)
            routes_df = pd.concat([routes_df, df])

        return routes_df


if __name__ == "__main__":
    routes_dir = "../data/json_data/"
    df_creator = DataFrameCreator(routes_dir)
    df = df_creator.create_routes_dataframe()
    print(df)
