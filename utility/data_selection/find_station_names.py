import pandas as pd
import os


def find_station_names():
    """
    Finds all station names 

    Finds all different station used in the data/raw_data.csv file.

    Parameters:
    No parameters! 

    Returns:
    list(list(str,int)): List of all stations, with number of observations.
    """

    abs_path = os.path.dirname(__file__)
    # Read in CSV file as Pandas dataframes
    lines_as_df = pd.read_csv(f"{abs_path}/../../data/raw_data.bas", delim_whitespace=True, low_memory=False,
                              names=["BAS","date","epoch","year","locations","length","length_sigma","transverse","transverse_sigma","horizontal","horizontal_sigma"], skiprows=2)

    # Split the stations into two columns
    station_names = lines_as_df.locations.str.split("/", expand=True)

    # Combine to a sorted list of unique stations
    station_names_list = list(
        set(station_names[0].unique().tolist() + station_names[1].unique().tolist()))
    station_names_list.sort()

    station_observations_list = []
    for station in station_names_list:
        lines_with_station = lines_as_df[lines_as_df.locations.str.contains(station)]
        station_observations_list.append(len(lines_with_station.locations.tolist()))

    return list(zip(station_names_list, station_observations_list))

