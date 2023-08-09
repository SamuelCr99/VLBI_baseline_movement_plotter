import pandas as pd


def find_matching_station_data(station1, station2):
    """
    Returns all data points containing both stations.

    It searches the database for rows containing both stations and writes that
    data to matching_rows.csv. The code assumes that there are rows of data that
    contains both stations.

    Parameters:
    station1 (string): One of the stations
    station2 (string): The other station

    Returns:
    lines_of_interest (DataFrame): All rows of data that contains both stations
    """

    # Read in CSV file as Pandas dataframes
    lines_as_df = pd.read_csv(
        'data/raw_data.csv', delim_whitespace=True, low_memory=False)

    lines_of_interest = lines_as_df.loc[
        (lines_as_df['locations'] == f"{station1}/{station2}") | (lines_as_df['locations'] == f"{station2}/{station1}")]
    lines_of_interest.reset_index(inplace = True)
    return lines_of_interest