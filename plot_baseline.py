import matplotlib.pyplot as plt
import numpy as np
import math
import argparse
from utility.find_matching_station_data import find_matching_station_data

figure_num = 0


def is_float(string):
    """
    Checks if given string value can be cast to floating point

    Parameters: 
    string (string): Value to be checked

    Returns: 
    bool: Boolean to tell if value can be cast or not
    """
    try:
        float(string)
        return True
    except ValueError:
        return False


def plot_lines(data, metric, plotSettings, viewSettings):
    """
    Plots the given metric in the matching_rows.csv file using the plotSettings.

    Using the plotSettings parameter, the types of plots produced (scatter
    and/or residual) is decided, as well as the data going in (raw data and/or
    trimmed data) and if a trend line should be drawn.

    Parameters:
    metric (string): The metric that should be plotted. Can be either "length",
    "transverse" or "horizontal".
    plotSettings (list): A list of booleans for the settings to be used when
    plotting.

    Returns:
    No return values!
    """

    global figure_num

    # Read in the data
    distance = []
    year = []
    sigma = []

    for i in range(len(data)):
        distance.append(float(getattr(data.iloc[i], metric)))
        year.append(float(getattr(data.iloc[i], "year")))
        sigma.append(float(getattr(data.iloc[i], f"{metric}_sigma")))
    stations = getattr(data.iloc[0], "locations")
    station1 = stations[:8]
    station2 = stations[9:]

    distance_raw = distance
    year_raw = year
    sigma_raw = sigma

    # Trim the data
    while (1):

        # Get the residuals from the trendline
        trendline = np.polyfit(year, distance, 1)

        residuals = []
        standard_deviation = 0

        for i in range(len(year)):
            correct_distance = trendline[0]*year[i] + trendline[1]
            residual = distance[i] - correct_distance
            residuals.append(residual)
            standard_deviation += pow(residual, 2)
        standard_deviation = math.sqrt(standard_deviation/len(year))

        # Remove data with large deviation
        distance_trimmed = []
        year_trimmed = []
        sigma_trimmed = []
        residuals_trimmed = []

        for i in range(len(year)):
            # Two sigma is considered "large" deviation, check with John
            if abs(residuals[i]) < standard_deviation*2:
                distance_trimmed.append(distance[i])
                year_trimmed.append(year[i])
                sigma_trimmed.append(sigma[i])
                residuals_trimmed.append(residuals[i])
        if len(year) == len(year_trimmed):
            break

        year = year_trimmed
        sigma = sigma_trimmed
        distance = distance_trimmed

    residuals_raw = []
    for i in range(len(year_raw)):
        correct_distance = trendline[0]*year_raw[i] + trendline[1]
        residual = distance_raw[i] - correct_distance
        residuals_raw.append(residual)

    # Generate lists for rolling window std plots
    window_size = float(plotSettings['rolling_stdWindowSize'])

    # Plot containing all datapoints
    std_dev_raw = []
    for i in range(len(year_raw)):
        window_res = []
        window_sig = []
        for k in range(0, len(year_raw)):
            if abs(year_raw[i]-year_raw[k]) <= window_size/2 and is_float(residuals_raw[k] and is_float(sigma_raw[k])):
                window_res.append(pow(float(residuals_raw[k])/float(sigma_raw[k]),2))
                window_sig.append(pow(1/float(sigma_raw[k]),2))
        std_dev_raw.append(math.sqrt(sum(window_res)/sum(window_sig)))

    # Plot for trimmed datapoints
    std_dev_trimmed = []
    for i in range(len(year_trimmed)):
        window_res = []
        window_sig = []
        for k in range(0, len(year_trimmed)):
            if abs(year_trimmed[i]-year_trimmed[k]) <= window_size/2 and is_float(residuals_trimmed[k] and is_float(sigma_trimmed[k])):
                window_res.append(pow(float(residuals_trimmed[k])/float(sigma_trimmed[k]),2))
                window_sig.append(pow(1/float(sigma_trimmed[k]),2))
        std_dev_trimmed.append(math.sqrt(sum(window_res)/sum(window_sig)))

    # Generate the plots
    if plotSettings["scatter"]:
        figure_num += 1
        plt.figure(figure_num)
        plt.title(f"{metric.capitalize()} between {station1} and {station2}")
        plt.figtext(
            0.95, 0.5, f'Number of raw datapoints: {len(year_raw)}\n Number of trimmed datapoints: {len(year_trimmed)}', va="center", ha='center', rotation=90)
        plt.figtext(
            0.5, 0.8, f'Slope of line: {round(trendline[0],2)} mm/year', va="center", ha='center')

        if plotSettings["scatterRaw"]:
            plt.plot(year_raw, distance_raw, "bo",
                     markersize=3, label="Raw data")

        if plotSettings["scatterTrimmed"]:
            plt.plot(year_trimmed, distance_trimmed, "ko",
                     markersize=3, label="Trimmed data")

        if plotSettings["scatterTrendline"]:
            plt.axline([year_trimmed[0], trendline[0]*year_trimmed[0]+trendline[1]],
                       slope=trendline[0], color="red", label="Trend line")

        plt.legend(loc="lower left")
        plt.xlabel('Year')
        # Check with John that this is correct!
        plt.ylabel(f'{metric.capitalize()} [mm]')
        if (viewSettings["save"]):
            plt.savefig(
                f"plots/Scatter_{station1}-{station2}_{metric}.{viewSettings['saveFormat']}", format=viewSettings["saveFormat"])

    if plotSettings["residual"]:
        figure_num += 1
        plt.figure(figure_num)
        plt.title(f"Residual of {metric} between {station1} and {station2}")
        plt.figtext(
            0.95, 0.5, f'Number of raw datapoints: {len(year_raw)}\n Number of trimmed datapoints: {len(year_trimmed)}', va="center", ha='center', rotation=90)

        if plotSettings["residualRaw"]:
            plt.plot(year_raw, residuals_raw, "bo",
                     markersize=3, label="Raw data")

        if plotSettings["residualTrimmed"]:
            plt.plot(year_trimmed, residuals_trimmed, "ko",
                     markersize=3, label="Trimmed data")

        plt.axhline(y=0, color="red", linestyle="-")
        plt.legend(loc="lower left")
        plt.xlabel('Year')
        # Check with John that this is correct!
        plt.ylabel(f'{metric.capitalize()} [mm]')
        if (viewSettings["save"]):
            plt.savefig(
                f"plots/Residual_{station1}-{station2}_{metric}.{viewSettings['saveFormat']}", format=viewSettings["saveFormat"])

    if plotSettings["rolling_std"]:
        figure_num += 1
        plt.figure(figure_num)
        plt.title(f"Rolling std of {metric} between {station1} and {station2}")
        plt.figtext(
            0.95, 0.5, f'Number of raw datapoints: {len(year_raw)}\n Number of trimmed datapoints: {len(year_trimmed)}', va="center", ha='center', rotation=90)

        if plotSettings["rolling_stdRaw"]:
            plt.plot(year_raw, std_dev_raw, "b-",
                     markersize=3, label="Raw data")

        if plotSettings["rolling_stdTrimmed"]:
            plt.plot(year_trimmed, std_dev_trimmed, "k-",
                     markersize=3, label="Trimmed data")

        plt.axhline(y=0, color="red", linestyle="-")
        plt.legend(loc="lower left")
        plt.xlabel('Year')
        # Check with John that this is correct!
        plt.ylabel(f'{metric.capitalize()} [mm]')
        if (viewSettings["save"]):
            plt.savefig(
                f"plots/Rolling_std_{station1}-{station2}_{metric}.{viewSettings['saveFormat']}", format=viewSettings["saveFormat"])
    if viewSettings["display"]:
        plt.show(block=False)
    else:
        plt.close("all")


if __name__ == '__main__':
    # Create parser to allow program to be run in script mode
    parser = argparse.ArgumentParser(
        prog='Plot baseline',
        description='Plots baselines between 2 given stations')

    parser.add_argument('station1', type=str)
    parser.add_argument('station2', type=str)
    parser.add_argument('--no_scatter', action='store_true', help="don't plot scatter plot")
    parser.add_argument('--no_residual', action='store_true', help="don't plot residual plot")
    parser.add_argument('--no_rolling_std', action='store_true', help="don't plot rolling std plot")
    parser.add_argument('--no_raw', action='store_true', help="don't plot raw data")
    parser.add_argument('--no_trimmed', action='store_true', help="don't plot trimmed data")
    parser.add_argument('--no_trendline', action='store_true', help="don't plot trendline")

    parser.add_argument('--save_plots', action='store_true', help="save plots to file")
    parser.add_argument('--show_plots', action='store_true', help="show plots")
    parser.add_argument('--file_type', type=str, default="png", help="file type to save plots as")

    parser.add_argument('--window_size', type=float, default=12, help="window size for rolling std (months)")
    args = parser.parse_args()

    plotSettings = {
        "scatter": not args.no_scatter,
        "scatterRaw": not args.no_raw,
        "scatterTrimmed": not args.no_trimmed,
        "scatterTrendline": not args.no_trendline,
        "residual": not args.no_residual,
        "residualRaw": not args.no_raw,
        "residualTrimmed": not args.no_trimmed,
        "rolling_std": not args.no_rolling_std,
        "rolling_stdRaw": not args.no_raw,
        "rolling_stdTrimmed": not args.no_trimmed,
        "rolling_stdWindowSize": args.window_size/12
    }

    viewSettings = {
        "display": args.show_plots,
        "save": args.save_plots,
        "saveFormat": args.file_type
    }

    data = find_matching_station_data(args.station1, args.station2)
    plot_lines(data, 'length', plotSettings, viewSettings)
    if args.show_plots:
        plt.show()
