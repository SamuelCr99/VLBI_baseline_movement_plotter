import matplotlib.pyplot as plt
import numpy as np
import math
import mplcursors

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
    info = []

    for i in range(len(data)):
        distance_i = getattr(data.iloc[i], metric)
        year_i = getattr(data.iloc[i], "year")
        sigma_i = getattr(data.iloc[i], f"{metric}_sigma")
        info_i = getattr(data.iloc[i], "date")
        info.append(info_i)

        if is_float(distance_i) and is_float(year_i) and is_float(sigma_i):
            distance.append(float(distance_i))
            year.append(float(year_i))
            sigma.append(float(sigma_i))

    stations = getattr(data.iloc[0], "locations")
    station1 = stations[:8]
    station2 = stations[9:]

    distance_raw = distance
    year_raw = year
    sigma_raw = sigma
    info_raw = info

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
        info_trimmed = []
        residuals_trimmed = []

        for i in range(len(year)):
            if abs(residuals[i]) <= standard_deviation*plotSettings["scatterLim"]:
                distance_trimmed.append(distance[i])
                year_trimmed.append(year[i])
                sigma_trimmed.append(sigma[i])
                info_trimmed.append(info[i])
                residuals_trimmed.append(residuals[i])
        
        # Stop if we didn't remove any outliers
        if len(year) == len(year_trimmed):
            break

        year = year_trimmed
        sigma = sigma_trimmed
        distance = distance_trimmed
        info = info_trimmed

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
            scatter_raw = plt.plot(year_raw, distance_raw, "bo",
                     markersize=3, label="Raw data")

        if plotSettings["scatterTrimmed"]:
            scatter_trimmed = plt.plot(year_trimmed, distance_trimmed, "ko",
                     markersize=3, label="Trimmed data")

        if plotSettings["scatterTrendline"]:
            plt.axline([year_trimmed[0], trendline[0]*year_trimmed[0]+trendline[1]],
                       slope=trendline[0], color="red", label="Trend line")

        # Adds arrows and annotations to all points
        if plotSettings["scatterRaw"] or plotSettings["scatterTrimmed"]:
            scatter = scatter_raw if plotSettings["scatterRaw"] else scatter_trimmed
            info = info_raw if plotSettings["scatterRaw"] else info_trimmed
            scatter_cursor = mplcursors.cursor(
                scatter, hover=mplcursors.HoverMode.Transient)
            scatter_cursor.connect(
                "add", lambda sel: sel.annotation.set_text(info[sel.index]))

        plt.legend(loc="lower left")
        plt.xlabel('Year')
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
            residual_raw = plt.plot(year_raw, residuals_raw, "bo",
                     markersize=3, label="Raw data")

        if plotSettings["residualTrimmed"]:
            residual_trimmed = plt.plot(year_trimmed, residuals_trimmed, "ko",
                     markersize=3, label="Trimmed data")
            
        # Adds arrows and annotations to all points
        if plotSettings["residualRaw"] or plotSettings["residualTrimmed"]:
            residual = residual_raw if plotSettings["residualRaw"] else residual_trimmed
            info = info_raw if plotSettings["residualRaw"] else info_trimmed
            residual_cursor = mplcursors.cursor(
                residual, hover=mplcursors.HoverMode.Transient)
            residual_cursor.connect(
                "add", lambda sel: sel.annotation.set_text(info[sel.index]))

        plt.axhline(y=0, color="red", linestyle="-")
        plt.legend(loc="lower left")
        plt.xlabel('Year')
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
        plt.ylabel(f'{metric.capitalize()} [mm]')
        if (viewSettings["save"]):
            plt.savefig(
                f"plots/Rolling_std_{station1}-{station2}_{metric}.{viewSettings['saveFormat']}", format=viewSettings["saveFormat"])
    if viewSettings["display"]:
        plt.show(block=False)
    else:
        plt.close("all")