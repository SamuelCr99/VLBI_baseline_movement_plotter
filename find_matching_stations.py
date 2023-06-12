import pandas as pd

def find_matching_stations(station_to_match):
    # Read in CSV file as Pandas dataframes
    lines_as_df = pd.read_csv('2023a_bas_apriori.csv', delim_whitespace=True)

    # Read in CSV file as plain text
    lines = open('2023a_bas_apriori.csv', 'r')
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


    stations = list(set(stations))
    stations.sort()
    return stations

if __name__ == '__main__':
    find_matching_stations('KOKEE___')