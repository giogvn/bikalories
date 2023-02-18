import gpxpy
import pandas as pd
import sys

def read_file(file_name):
    return gpxpy.parse(file_name)

def convert_to_dataframe(gpx_parsed):
    points = []
    for segment in gpx_parsed.tracks[0].segments:
        for p in segment.points:
            points.append({
                'timestamp': p.time,
                'latitude': p.latitude,
                'longitude': p.longitude,
                'elevation': p.elevation,
            })
    return pd.DataFrame.from_records(points)

def df_to_csv(df, file_name):
    df.to_csv(file_name)

def main(gpx_file):
    dir = ''

    gpx_parsed = read_file(gpx_file)
    df = convert_to_dataframe(gpx_parsed)


gpx_file = 'run.gpx'
with open(gpx_path) as f:
    gpx = gpxpy.parse(f)
