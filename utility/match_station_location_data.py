import pandas as pd

with open('data/stations.txt', 'r') as file:
    our_stations = file.readlines()

location_rows = pd.read_csv('data/position.csv', delim_whitespace=True)
location_rows['updated'] = False


our_station_remove_old = our_stations
rows_to_write = []

c = 0
for i, loc_row in location_rows.iterrows():
    for our_station in our_stations:
        if loc_row['Name'].lower() == our_station.strip('\n').rstrip('_').lower():
            location_rows.at[i, 'Name'] = our_station.strip('\n')
            location_rows.at[i, 'updated'] = True
location_rows = location_rows.loc[location_rows['updated']]
location_rows.drop(['updated', 'ID', 'X', 'Y', 'Z', 'Occ.Code', 'Origin'], axis=1, inplace=True)
location_rows.Lon = location_rows.Lon * -1
location_rows = location_rows.rename(columns={'Name' : 'station', 'Lon': 'x', 'Lat': 'y'})

for i, loc_row in location_rows.iterrows():
    if loc_row['x'] < -180:
        location_rows.at[i, 'x'] = loc_row['x'] + 360
    elif loc_row['x'] > 180:
        location_rows.at[i, 'x'] = loc_row['x'] - 360


location_rows.to_csv(
    'data/station_locations.csv', sep=",", index=False)