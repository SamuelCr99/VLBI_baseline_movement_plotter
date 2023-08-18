import pandas as pd
import os

def match_station_location_data(our_stations):
    """
    Finds the location of all stations
    
    Goes through the data/position.csv file and returns the position of all
    given stations.

    Parameters:
    our_stations(list(str)): The names of the stations that we want position of
    
    Returns:
    DataFrame: Containing stations and their positiion
    """

    abs_path = os.path.dirname(__file__)
    location_rows = pd.read_csv(f'{abs_path}/../../data/position.csv')
    location_rows['updated'] = False

    for i, loc_row in location_rows.iterrows():
        for our_station in our_stations:
            our_station = our_station[0]
            if loc_row['station'].lower() == our_station.strip('\n').rstrip('_').lower():
                location_rows.at[i, 'station'] = our_station.strip('\n')
                location_rows.at[i, 'updated'] = True
    location_rows = location_rows.loc[location_rows['updated']]
    location_rows.drop(["updated"], axis=1, inplace=True)
    location_rows = location_rows.rename(columns={'lon': 'x', 'lat': 'y'})

    for i, loc_row in location_rows.iterrows():
        if loc_row['x'] < -180:
            location_rows.at[i, 'x'] = loc_row['x'] + 360
        elif loc_row['x'] > 180:
            location_rows.at[i, 'x'] = loc_row['x'] - 360
    
    # Reset index of location_rows
    location_rows.reset_index(drop=True, inplace=True)

    return location_rows