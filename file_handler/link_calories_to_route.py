import pandas as pd
import os, json, datetime, pytz
from datetime import datetime


class CaloriesToRouteLinker:
    def __init__(self, routes_dir: str, cals_path: str):
        self.routes_dir = routes_dir
        self.cals_data = self.read_json_into_list(cals_path)
        self.routes_dict = self.create_routes_dict()

    def read_json_into_list(self, cals_path: str) -> list:
        with open(cals_path, "r") as f:
            out = json.load(f)

        return out

    def create_routes_dict(self) -> dict:
        out = {}
        for path in os.listdir(self.routes_dir):
            route_path = os.path.join(self.routes_dir, path)
            if os.path.isfile(route_path):
                out[path] = route_path

        return out

    def write_info_to_json(
        self, json_path: str, info: any, new_key: str = "general_info"
    ) -> None:
        with open(json_path, "r") as f:
            data = json.load(f)
        data_dict = {}
        data_dict["route"] = data

        data_dict[new_key] = info

        with open(json_path, "w") as f:
            json.dump(data_dict, f, indent=4)

    def add_info(self, workout: dict, key="json_name") -> None:
        route = self.routes_dict[workout[key]]

        self.write_info_to_json(route, workout)

    def add_info_to_all_workouts(self):
        for workout in self.cals_data:
            self.add_info(workout)

    def add_space_before_timezone_data(self, old_string: str) -> str:
        new_string = old_string.replace("+", " +")
        return new_string

    def remove_timezone_data(self, old_string: str) -> str:
        index = old_string.find(" -")
        return old_string[:index]

    def update_chars(self, key: str) -> str:
        new_string = key.replace(" ", "--").replace(":", "-")
        return "Workout--" + new_string + ".json"

    def update_datetime_time_zone(
        self, date_time: str, zone: str = "America/Sao_Paulo"
    ) -> str:

        date_format = "%Y-%m-%d %H:%M:%S %z"
        date_time = datetime.strptime(date_time, date_format)

        local_timezone = pytz.timezone(zone)
        local_time = date_time.astimezone(local_timezone)

        date_string = local_time.strftime(date_format)

        return date_string

    def match_start_time_format_to_route(self, key="startTime") -> None:
        for index, workout in enumerate(self.cals_data):
            old_string = self.cals_data[index][key]
            new_string = self.add_space_before_timezone_data(old_string)
            new_string = self.update_datetime_time_zone(new_string)
            self.cals_data[index][key] = new_string
            new_string = self.remove_timezone_data(new_string)
            new_string = self.update_chars(new_string)

            self.cals_data[index]["json_name"] = new_string


if __name__ == "__main__":
    routes_dir = "../data/json_data/"
    cals_path = "../data/calories_data.json"

    linker = CaloriesToRouteLinker(routes_dir, cals_path)
    linker.match_start_time_format_to_route()
    linker.add_info_to_all_workouts()
