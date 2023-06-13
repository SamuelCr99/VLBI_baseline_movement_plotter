import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math

def plot_lines(metric,plotSettings):

    # Read in the data
    distance = []
    year = []

    data = pd.read_csv('data/matching_rows.csv', delim_whitespace=True)

    for i in range(len(data)):
        distance.append(getattr(data.loc[i], metric))
        year.append(data.loc[i].year)

    stations = getattr(data.loc[0], "locations")
    station1 = stations[:8]
    station2 = stations[9:]

    distance_raw = distance
    year_raw = year

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
        residuals_trimmed = []

        for i in range(len(year)):
            if abs(residuals[i]) < standard_deviation*2:        # Two sigma is considered "large" deviation, check with John
                distance_trimmed.append(distance[i])
                year_trimmed.append(year[i])
                residuals_trimmed.append(residuals[i])
        if len(year) == len(year_trimmed):
            break

        year = year_trimmed
        distance = distance_trimmed

    # Generate the plots
    figure_num = 0

    if plotSettings["scatter"]:
        figure_num+=1
        plt.figure(figure_num)
        plt.title(f"{metric.capitalize()} between {station1} and {station2}")
        plt.annotate(f'Total number of datapoints: {len(year_raw)}', (0.53, 0.9), xycoords='axes fraction', fontsize=10)

        if plotSettings["scatterRaw"]:
            plt.plot(year_raw, distance_raw, "bo", markersize=3, label="Raw data")

        if plotSettings["scatterTrimmed"]:
            plt.plot(year_trimmed, distance_trimmed, "ko", markersize=3, label="Trimmed data")

        if plotSettings["scatterTrendline"]:
            plt.axline([year_trimmed[0],trendline[0]*year_trimmed[0]+trendline[1]], slope=trendline[0], color="red", label="Trend line")

        plt.legend(loc="lower left")
        plt.xlabel('Year')
        plt.ylabel(f'{metric.capitalize()} [mm]') # Check with John that this is correct! 


    if plotSettings["residual"]:
        figure_num+=1
        plt.figure(figure_num)
        plt.title(f"Residual of {metric} between {station1} and {station2}")
        plt.annotate(f'Total number of datapoints: {len(year_raw)}', (0.53, 0.9), xycoords='axes fraction', fontsize=10)
        plt.axhline(y=0, color="red", linestyle="-")

        if plotSettings["residualRaw"]:
            residuals_raw = []
            for i in range(len(year_raw)):
                correct_distance = trendline[0]*year_raw[i] + trendline[1]
                residual = distance_raw[i] - correct_distance
                residuals_raw.append(residual)
            plt.plot(year_raw, residuals_raw, "bo", markersize = 3, label="Raw data")
        
        if plotSettings["residualTrimmed"]:
            plt.plot(year_trimmed, residuals_trimmed, "ko", markersize = 3, label="Trimmed data")

        plt.legend(loc="lower left")
        plt.xlabel('Year')
        plt.ylabel(f'{metric.capitalize()} [mm]') # Check with John that this is correct!

    plt.show()

if __name__ == '__main__':
    plotSettings = {
    "scatter": True,
    "scatterRaw": True,
    "scatterTrimmed": True,
    "scatterTrendline": True,
    "residual": True,
    "residualRaw": True,
    "residualTrimmed": True,
    "residualLine": True
    }
    plot_lines('length',plotSettings)