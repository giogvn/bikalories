import json, requests, os


class JsonModifier:
    def __init__(self, json_dir: str):
        global modified_files, log_file, output_file
        self.json_dir = json_dir

    def get_location_elevation(
        self, lats: list, longs: list, key: str = "elevation"
    ) -> float:

        url = "https://api.open-meteo.com/v1/elevation"

        f = lambda x: round(x, 4)
        lats = list(map(f, lats))
        longs = list(map(f, longs))
        params = {
            "latitude": (i for i in lats),
            "longitude": (i for i in longs),
        }
        response = requests.get(url, params)

        return response.json()[key]

    def update_many_points(self, dirs_list: list, key: str) -> list:
        lats = []
        longs = []
        points_hash = {i: point for i, point in enumerate(dirs_list)}
        for point in points_hash.values():
            lats.append(point["latitude"])
            longs.append(point["longitude"])

        new_coords = self.get_location_elevation(lats, longs)

        for index, point in points_hash.items():
            point[key] = float(new_coords[index])

        return list(points_hash.values())

    def generate_splits(self, data, max_inserts) -> tuple:
        data_splits = len(data) // max_inserts
        data_rem = len(data) % max_inserts
        return data_splits, data_rem

    def update_key(self, json_path: str, key: str = "elevation") -> None:
        with open(json_path, "r") as f:
            data = json.load(f)

        total_points = len(data)
        max_inserts = 100

        n_max_inserts, n_final_inserts = self.generate_splits(
            data["route"], max_inserts
        )
        start = 0
        step = max_inserts
        for i in range(n_max_inserts):
            data["route"][start : start + step] = self.update_many_points(
                data["route"][start : start + step], key
            )
            start += step
        if n_final_inserts > 0:
            data["route"][start : start + step] = self.update_many_points(
                data["route"][-n_final_inserts:], key
            )

        with open(json_path, "w") as f:
            json.dump(data, f, indent=4)

    def update_jsons(self) -> bool:
        curr_file = ""
        try:
            for file in os.listdir(self.json_dir):
                if not modified_files[file]:
                    curr_file = file
                    print(f"Updating file: {file}")
                    file_path = os.path.join(self.json_dir, file)
                    self.update_key(file_path)
                    modified_files[file] = True
                    with open(log_file, "w") as f:
                        json.dump(modified_files, f, indent=4)
            return True
        except:
            with open(output_file, "a") as f:
                f.write(f"Failed to update file {curr_file}'" + "\n")

            return False


if __name__ == "__main__":
    json_dir = "../data/json_data/"
    log_file = "modified_json.json"
    output_file = "fail_files.txt"
    with open(log_file, "r") as f:
        modified_files = json.load(f)
    modifier = JsonModifier(json_dir)

    while not modifier.update_jsons():
        continue
