import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import statistics


def plot_lines(metric):
    # Read in the data
    distance = []
    year = []
    station1 = ""
    station2 = ""
    data = pd.read_csv('data/matching_rows.csv', delim_whitespace=True, low_memory=False)
    window_size = 1
    std_dev_array = []

    for i in range(len(data)):
        distance.append(getattr(data.loc[i], metric))
        year.append(data.loc[i].year)


    for i in range(len(data)):
        window = [] 
        for k in range(i, len(data)): 
            if year[k] - year[i] < window_size:
                window.append(distance[k]) 
            else: 
                break
        if len(window) > 1:
            std_dev_array.append(statistics.stdev(window))
        else: 
            std_dev_array.append(0)
    plt.plot(year, std_dev_array)

    plt.title(f" of {metric} between {station1} and {station2}")
    plt.annotate(f'Total number of datapoints: {len(year)}', (
        0.53, 0.9), xycoords='axes fraction', fontsize=10)
    plt.show()


if __name__ == '__main__':
    plot_lines('length')
