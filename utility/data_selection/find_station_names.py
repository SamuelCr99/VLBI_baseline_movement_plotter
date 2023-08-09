import pandas as pd


def find_station_names():
    """
    Finds all station names 

    Finds all different station used in the data/raw_data.csv file.

    Parameters:
    No parameters! 

    Returns:
    list(list(str,int)): List of all stations, with number of observations.
    """

    # Read in CSV file as Pandas dataframes
    lines_as_df = pd.read_csv(
        'data/raw_data.csv', delim_whitespace=True, low_memory=False)

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

