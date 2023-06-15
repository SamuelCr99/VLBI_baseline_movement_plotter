import pandas as pd

with open('data/stations.txt', 'r') as file:
    our_stations = file.readlines()

location_rows = pd.read_csv('data/station_locations_old.csv', delimiter=";")
location_rows['updated'] = False
        

our_station_remove_old = our_stations
rows_to_write = []

c = 0
for i, loc_row in location_rows.iterrows():
    for our_station in our_stations:
        if loc_row['station'].lower() == our_station.strip('\n').rstrip('_').lower():
            location_rows.at[i,'station'] = our_station.strip('\n')
            location_rows.at[i, 'updated'] = True
location_rows = location_rows.loc[location_rows['updated']] 
location_rows.drop(['updated'], axis=1, inplace=True)
location_rows.to_csv('data/station_locations_correct_names.csv', sep=",", index=False)

# with open('data/station_locations_correct_names.csv', 'w') as file: 
#     file.writelines(rows_to_write)