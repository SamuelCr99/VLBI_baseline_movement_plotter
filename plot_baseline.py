import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math

def plot_lines():

    # Read in the data
    distance = []
    year = []

    data = pd.read_csv('matching_rows.csv', delim_whitespace=True)

    for i in range(len(data)):
        distance.append(data.loc[i].length)
        year.append(data.loc[i].year)

    # Trim the data
    while(1):

        # Get the residuals from the trendline
        trendline = np.polyfit(year, distance, 1)

        residuals = []
        standard_deviation = 0

        for i in range(len(year)):
            correct_distance = trendline[0]*year[i] + trendline[1]
            residual = distance[i] - correct_distance
            residuals.append(residual)
            standard_deviation += pow(residual,2)
        standard_deviation = math.sqrt(standard_deviation/len(year))
        print(standard_deviation)

        # Remove data with large deviation
        distance_trimmed = []
        year_trimmed = []

        for i in range(len(year)):
            if abs(residuals[i]) < standard_deviation*2:        # Two sigma is considered "large" deviation, check with John
                distance_trimmed.append(distance[i])
                year_trimmed.append(year[i])
        if len(year) == len(year_trimmed):
            break

        year = year_trimmed
        distance = distance_trimmed

    # Plot baseline distance to time
    plt.text(year_trimmed[int(len(year_trimmed)/4)], distance_trimmed[0], f'Total number of datapoints: {len(year_trimmed)}', fontsize = 12)
    plt.plot(year_trimmed, distance_trimmed)
    plt.xlabel('Year')
    plt.ylabel('Distance [mm]') # Check with John that this is correct! 
    plt.show()

if __name__ == '__main__':
    plot_lines()