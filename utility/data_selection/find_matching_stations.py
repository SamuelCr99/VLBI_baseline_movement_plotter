import pandas as pd


def find_matching_stations(station_to_match):
    """
    Finds all stations which share at least one observation with given station.

    Loops through all VLBI data to find which VLBI stations have had at least 1 
    VLBI together with given station. Then counts the number of sessions.  

    Parameters:
    arg1 (str): Name of station to match against.

    Returns:
    list[str]: List of all stations which match, with number of matches. 
    """

    # Read in CSV file as Pandas data frame
    lines_as_df = pd.read_csv(
        'data/raw_data.csv', delim_whitespace=True, low_memory=False)

    lines_of_interest = lines_as_df.loc[
        lines_as_df['locations'].str.contains(station_to_match)]

    station_names = pd.DataFrame()
    station_names['locations'] = lines_of_interest['locations'].copy()
    station_count = station_names.groupby(
        station_names.columns.tolist(), as_index=False).size()

    station_count['locations'] = station_count['locations'].apply(lambda x: x.replace(station_to_match,'').replace('/', ''))

    return list(zip(station_count.locations.tolist(),station_count["size"].tolist()))
