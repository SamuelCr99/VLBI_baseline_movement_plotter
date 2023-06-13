import pandas as pd

def find_station_names():
    # Read in CSV file as Pandas dataframes
    lines_as_df = pd.read_csv('data/2023a_bas_apriori.csv', delim_whitespace=True)

    # Read in CSV file as plain text
    lines = open('data/2023a_bas_apriori.csv', 'r')
    lines = lines.readlines()
    stations = []

    # Finds all rows where both stations are present
    for i in range(len(lines_as_df)): 
        locations = lines_as_df.loc[i].locations
        split_locations = locations.split('/')
        if split_locations[0] not in stations: 
            stations.append(split_locations[0])
        if split_locations[1] not in stations:
            stations.append(split_locations[1])
    stations.sort()
    f = open('data/stations.txt', 'w')

    # Writes matching rows to new CSV file
    for station in stations:
        f.write(f'{station}\n')

    f.close()

if __name__ == '__main__':
    find_station_names()