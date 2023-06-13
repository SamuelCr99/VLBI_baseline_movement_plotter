import pandas as pd


def find_matching_stations(station_to_match):
    # Read in CSV file as Pandas dataframes
    lines_as_df = pd.read_csv(
        'data/2023a_bas_apriori.csv', delim_whitespace=True)

    # Read in CSV file as plain text
    lines = open('data/2023a_bas_apriori.csv', 'r')
    lines = lines.readlines()
    stations = []

    # Finds all rows where both stations are present
    for i in range(len(lines_as_df)):
        locations = lines_as_df.loc[i].locations
        split_locations = locations.split('/')
        if split_locations[0] == station_to_match:
            stations.append(split_locations[1])
        elif split_locations[1] == station_to_match:
            stations.append(split_locations[0])

    stations.sort()
    stations_counted_dict = {i: stations.count(i) for i in stations}
    stations_counted_array = []
    for key in stations_counted_dict:
        stations_counted_array.append(f'{key}[{stations_counted_dict[key]}]')

    return stations_counted_array


if __name__ == '__main__':
    find_matching_stations('KOKEE___')

