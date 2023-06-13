import pandas as pd


def find_matching_stations(station_to_match):
    """
    Finds all stations which share at least 1 VLBI station with given station.
  
    Loops through all VLBI data to find which VLBI stations have had at least 1 
    VLBI together with given station. Then counts the number of sessions.  
  
    Parameters:
    arg1 (str): Name of station to match against.
  
    Returns:
    list[str]: List of all stations which match, with number of matches. 
    """


    # Read in CSV file as Pandas data frame
    lines_as_df = pd.read_csv(
        'data/2023a_bas_apriori.csv', delim_whitespace=True, low_memory=False)

    # Read in CSV file as plain text
    lines = open('data/2023a_bas_apriori.csv', 'r')
    lines = lines.readlines()
    stations = []

    # Finds all rows where station is present and adds station to list for 
    # returning
    for i in range(len(lines_as_df)):
        locations = lines_as_df.loc[i].locations
        split_locations = locations.split('/')
        if split_locations[0] == station_to_match:
            stations.append(split_locations[1])
        elif split_locations[1] == station_to_match:
            stations.append(split_locations[0])

    # Sort so list is in alphabetic order
    stations.sort()

    # Creates a dictionary containing the number of times a station has shared 
    # VLBI session with station_to_match
    stations_counted_dict = {i: stations.count(i) for i in stations}
    stations_counted_array = []
    for key in stations_counted_dict:
        # Fill new list with name and count value
        stations_counted_array.append(f'{key}[{stations_counted_dict[key]}]')

    return stations_counted_array


if __name__ == '__main__':
    find_matching_stations('KOKEE___')

