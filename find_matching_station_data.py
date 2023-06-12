import pandas as pd

def find_matching_station_data(station1, station2):
    lines_as_df = pd.read_csv('2023a_bas_apriori.csv', delim_whitespace=True)
    lines = open('2023a_bas_apriori.csv', 'r')
    lines = lines.readlines()
    rows_of_interest = []


    for i in range(len(lines_as_df)): 
        locations = lines_as_df.loc[i].locations
        split_locations = locations.split('/')
        if station1 in split_locations and station2 in split_locations:
            rows_of_interest.append(lines[i+1])

    f = open('matching_rows.csv', 'w')
    f.write('BAS date epoch year locations length length_sigma transverse transverse_sigma horizontal horizontal_sigma \n')
    f.close()

    f = open('matching_rows.csv', 'a')
    for row in rows_of_interest:
        f.write(row)

    f.close()

if __name__ == '__main__':
    find_matching_station_data('KOKEE___', 'WETTZELL')