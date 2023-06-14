import pandas as pd


def find_matching_station_data(station1, station2):
    """
    Writes a CSV file with all the data points containing both stations.

    It searches the database for rows containing both stations and writes that
    data to matching_rows.csv. The code assumes that there are rows of data that
    contains both stations.

    Parameters:
    station1 (string): One of the stations
    station2 (string): The other station

    Returns:
    No return values!
    """

    # Read in CSV file as Pandas dataframes
    lines_as_df = pd.read_csv(
        'data/2023a_bas_apriori.csv', delim_whitespace=True, low_memory=False)
    
    lines_of_interest = lines_as_df.loc[
        (lines_as_df['locations'] == f"{station1}/{station2}") | (lines_as_df['locations'] == f"{station2}/{station1}")]

    lines_of_interest.to_csv('data/matching_rows.csv', ' ', index=False)

if __name__ == '__main__':
    find_matching_station_data('WETTZELL', 'KOKEE___')
