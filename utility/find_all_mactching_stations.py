import json
from find_matching_stations import find_matching_stations


def find_all_matching_stations():
    """
    DEPRECATED
    Creates a JSON file with all stations and the stations they have shared 
    at least 1 session with. 

    Runs find_matching_stations() on all available stations, saves the result 
    in a JSON file.

    Parameters:
    No parameters! 

    Returns:
    No return values!
    """
    matching_stations_dict = {}
    with open('data/stations.txt') as file:
        stations = file.readlines()
        for station in stations:
            station = station.strip('\n')
            matching_stations = find_matching_stations(station)
            matching_stations_dict[station] = matching_stations

    with open('data/matching_stations.json', 'w') as file:
        # Write contents of dictionary to file
        json.dump(matching_stations_dict, file, indent=4)


if __name__ == "__main__":
    find_all_matching_stations()
