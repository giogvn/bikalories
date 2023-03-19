import json, os
import pandas as pd
import numpy as np
from geopy import distance
from datetime import datetime
from collections import defaultdict


class RouteAnalyzer:
    def __init__(self, routes: pd.DataFrame) -> None:
        self.routes_df = routes

    def get_distance_between_coords(self, coord1: tuple, coord2: tuple) -> float:
        return distance.distance(coord1, coord2).meters

    def get_route(self, route_id: str) -> pd.DataFrame:
        return self.routes_df.loc[self.routes_df["route_id"] == route_id]

    def calculate_route_dists_and_times(self, route_id: str) -> dict:
        dists = np.empty(shape=None)
        times = np.empty(shape=None)
        dists_and_times = {"dists": dists, "times": times}

        route = self.get_route(route_id)

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
            dists_and_times["dists"] = np.append(dists_and_times["dists"], distance)
            dists_and_times["times"] = np.append(dists_and_times["times"], delta_t)

        return dists_and_times

    def calculate_route_acc_dists_and_times(self, route_id: str) -> list:
        points = self.calculate_route_dists_and_times(route_id)
        dists = points["dists"]
        times = points["times"]
        acumulated_dists = np.cumsum(dists)
        acumulated_times = np.cumsum(times)

        return acumulated_dists, acumulated_times

    def calculate_speeds_and_times(self, route_id: str) -> list:
        route = self.calculate_route_dists_and_times(route_id)
        speeds = [0]
        total_t = 0
        times = [total_t]
        for index, point in enumerate(route[1:]):
            speeds.append(point[0] / point[1])
            total_t += point[1]
            times.append(total_t)

        return speeds, times

    def detect_slopes(self, route_id: str) -> dict:
        slope = False
        slopes = defaultdict(dict)
        counter = 0
        route = self.get_route(route_id)
        for index, row in route.iterrows():
            if index == route.index[-1]:
                break
            points = route.iloc[index : index + 2]
            point1 = points.iloc[0]
            point2 = points.iloc[1]

            elev1 = point1["elevation"]
            elev2 = point2["elevation"]

            if elev1 != elev2 and not slope:
                slope = True
                begin = point1["latitude"], point1["longitude"]
                if elev2 > elev1:
                    type = "uphill"
                else:
                    type = "downhill"

            elif slope and elev1 == elev2:
                slope = False
                slope_end = point2["latitude"], point2["longitude"]
                slopes[counter]["begin"] = begin
                slopes[counter]["end"] = slope_end
                slopes[counter]["type"] = type
                counter += 1

        return slopes

    def get_route_profile(self, prof_dict: dict, prof_key: str = "type") -> list:
        profile = []
        for time_count in prof_dict:
            profile.append(prof_dict[time_count][prof_key])

        return profile
