import json, os
import pandas as pd
from geopy import distance
from datetime import datetime
from dataframe_creator import DataFrameCreator


'''
R.Paraguaçu: (-23.562405346185454, -46.77605625444006)->(-23.56223209778218, -46.77324323637639)
R. Guatemala (-23.562262407060924, -46.77505893039126)->(-23.560682655839585, -46.77504353977187)
Av. Manoel de Nóbrega (-23.560419711566198, -46.77039949222879)->(-23.56223209778218, -46.77324323637639)
Av. Manoel de Nóbrega (-23.560419711566198, -46.77039949222879)->(-23.55889146395058, -46.76690518788758)
Av. Dr Martin Luther King (-23.557703213925162, -46.763924431024996)->(-23.558286410077947, -46.76682611850268)
Av. Dr Cândido Motta FIlho (-23.556865478187664, -46.75321448962341)->(-23.55711705037529, -46.74987542723435)

'''

class RouteAnalyzer:
    def __init__(self, routes: pd.DataFrame) -> None:
        self.routes_df = routes

    def get_distance_between_coords(self, coord1: tuple, coord2: tuple) -> float:
        return distance.distance(coord1, coord2).meters

    def calculate_route_dists_and_times(self, route_id: str) -> list:
        distances = [(0, 0)]
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

            distances.append((distance, delta_t))
        return distances

    def calculate_route_total_dists_and_times(self, route_id: str) -> tuple:
        points = self.calculate_route_dists_and_times(route_id)
        dists = [p[0] for p in points]
        times = [p[1] for p in points]

        acumulated_dists = [sum(dists[: i + 1]) for i in range(len(dists))]
        acumulated_times = [sum(times[: i + 1]) for i in range(len(times))]

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
    
    def calculate_acceleration_between_coords(self, coord1 : tuple, coord2: tuple) -> float:

