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
        'data/2023a_bas_apriori.csv', delim_whitespace=True)

    # Read in CSV file as plain text
    lines = open('data/2023a_bas_apriori.csv', 'r')
    lines = lines.readlines()
    rows_of_interest = []

    # Finds all rows where both stations are present
    for i in range(len(lines_as_df)):
        locations = lines_as_df.loc[i].locations
        split_locations = locations.split('/')
        if station1 in split_locations and station2 in split_locations:
            rows_of_interest.append(lines[i+1])

    # Adds header to new CSV file
    f = open('data/matching_rows.csv', 'w')
    f.write('BAS date epoch year locations length length_sigma transverse transverse_sigma horizontal horizontal_sigma \n')
    f.close()

    f = open('data/matching_rows.csv', 'a')

    # Writes matching rows to new CSV file
    for row in rows_of_interest:
        f.write(row)

    f.close()


if __name__ == '__main__':
    find_matching_station_data('KOKEE___', 'WETTZELL')
