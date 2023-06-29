import pandas as pd


def find_station_names():
    """
    Finds all station names 

    Finds all different station names available in CSV file

    Parameters:
    No parameters! 

    Returns:
    No return values! 
    """

    # Read in CSV file as Pandas dataframes
    lines_as_df = pd.read_csv(
        'data/raw_data.csv', delim_whitespace=True, low_memory=False)

    # Split the stations into two columns
    station_names = lines_as_df['locations'].str.split("/", expand=True)

    # Combine to a sorted list of unique stations
    station_names_list = list(
        set(station_names[0].unique().tolist() + station_names[1].unique().tolist()))
    station_names_list.sort()
    return station_names_list

