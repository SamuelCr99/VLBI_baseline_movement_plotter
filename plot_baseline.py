import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math

def plot_lines(metric,plotTypes):

    # Read in the data
    distance = []
    year = []

    data = pd.read_csv('matching_rows.csv', delim_whitespace=True)

    for i in range(len(data)):
        distance.append(getattr(data.loc[i], metric))
        year.append(data.loc[i].year)

    distance_original = distance
    year_original = year

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
    figure_num = 0

    if plotTypes["scatter"] == True:
        figure_num+=1
        plt.figure(figure_num)
        plt.text(year_original[int(len(year_original)/4)], distance_original[0], f'Total number of datapoints: {len(year_original)}', fontsize = 12)
        plt.plot(year_original, distance_original)
        plt.xlabel('Year')
        plt.ylabel('Distance [mm]') # Check with John that this is correct! 

    if plotTypes["scatterTrimmed"] == True:
        figure_num+=1
        plt.figure(figure_num)
        plt.text(year_trimmed[int(len(year_trimmed)/4)], distance_trimmed[0], f'Total number of datapoints: {len(year_trimmed)}', fontsize = 12)
        plt.plot(year_trimmed, distance_trimmed)
        plt.xlabel('Year')
        plt.ylabel('Distance [mm]') # Check with John that this is correct! 
    plt.show()

if __name__ == '__main__':
    plotTypes = {
    "scatter": True,
    "scatterTrimmed": True
    }
    plot_lines('length',plotTypes)