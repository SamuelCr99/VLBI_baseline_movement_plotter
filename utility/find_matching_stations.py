import pandas as pd


def find_matching_stations(station_to_match):
    """
    Finds all stations which share at least 1 VLBI station with given station.

    Loops through all VLBI data to find which VLBI stations have had at least 1 
    VLBI together with given station. Then counts the number of sessions.  

    Parameters:
    arg1 (str): Name of station to match against.

    Returns:
    list[str]: List of all stations which match, with number of matches. 
    """

    # Read in CSV file as Pandas data frame
    lines_as_df = pd.read_csv(
        'data/2023a_bas_apriori.csv', delim_whitespace=True, low_memory=False)

    lines_of_interest = lines_as_df.loc[
        lines_as_df['locations'].str.contains(station_to_match)]

    station_names = pd.DataFrame()
    station_names['locations'] = lines_of_interest['locations'].copy()
    station_count = station_names.groupby(
        station_names.columns.tolist(), as_index=False).size()

    stations_counted_array = []
    for _, row in station_count.iterrows():
        name_of_station = row.loc['locations']
        name_of_station = name_of_station.replace(station_to_match, '')
        name_of_station = name_of_station.replace('/', '')
        count = row.loc['size']
        stations_counted_array.append(f'{name_of_station}[{count}]')

    stations_counted_array.sort()
    return stations_counted_array


if __name__ == '__main__':
    find_matching_stations('KOKEE___')
