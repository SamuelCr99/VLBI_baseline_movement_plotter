import pandas as pd
import os

def find_matching_station_data(station1, station2, start_yr, end_yr):
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

    abs_path = os.path.dirname(__file__)
    # Read in CSV file as Pandas dataframes
    lines_as_df = pd.read_csv(f"{abs_path}/../../data/raw_data.bas", delim_whitespace=True, low_memory=False,
                              names=["BAS","date","epoch","year","locations","length","length_sigma","transverse","transverse_sigma","horizontal","horizontal_sigma"], skiprows=2)

    # Pick out the stations
    lines_as_df = lines_as_df.loc[
        (lines_as_df['locations'] == f"{station1}/{station2}") | (lines_as_df['locations'] == f"{station2}/{station1}")]
    
    # Pick from the selected years
    if start_yr:
        lines_as_df = lines_as_df.loc[lines_as_df['year'] >= start_yr]
    if end_yr:
        lines_as_df = lines_as_df.loc[lines_as_df['year'] <= end_yr]

    lines_as_df.reset_index(inplace = True)
    return lines_as_df