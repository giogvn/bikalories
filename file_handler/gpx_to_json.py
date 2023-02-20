import gpxpy
import pandas as pd
import sys, os
from gpx_converter import Converter
from pathlib import Path


class GPXHandler:
    def __init__(self) -> None:
        pass

    def read_gpx_file(self, file_name: str) -> any:
        with open(file_name, "r") as f:
            return gpxpy.parse(f)

    def parsed_gpx_to_dataframe(self, parsed_gpx: any) -> pd.DataFrame:
        points = []
        for segment in parsed_gpx.tracks[0].segments:
            for p in segment.points:
                points.append(
                    {
                        "timestamp": p.time,
                        "latitude": p.latitude,
                        "longitude": p.longitude,
                        "elevation": p.elevation,
                    }
                )
        return pd.DataFrame.from_records(points)

    def gpx_to_json(self, file_name: str, output_path: str) -> str:
        gpx_data_frame = self.parsed_gpx_to_dataframe(self.read_gpx_file(file_name))
        return gpx_data_frame.to_json(orient="index", path_or_buf=output_path)

    def write_json_from_gpx(self, input: str, output_dir: str) -> None:
        output_path = output_dir + Path(input).stem + ".json"
        with open(output_path, "w") as f:
            self.gpx_to_json(input, output_path)


if __name__ == "__main__":
    gpx_handler = GPXHandler()
    output_dir = "../data/json_data/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    input = sys.argv[1]
    if os.path.isdir(input):
        for file in os.listdir(input):
            file_path = os.path.join(input, file)
            gpx_handler.write_json_from_gpx(file_path, output_dir)
    else:
        gpx_handler.write_json_from_gpx(input, output_dir)
