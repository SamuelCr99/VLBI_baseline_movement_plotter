import json
from utility.find_matching_stations import find_matching_stations

matching_stations_dict = {}
with open('data/stations.txt') as file: 
    stations = file.readlines()
    for station in stations: 
        station = station.strip('\n')
        matching_stations = find_matching_stations(station)
        matching_stations_dict[station] = matching_stations


with open('data/matching_stations.json', 'w') as file:
    json.dump(matching_stations_dict, file, indent = 4)