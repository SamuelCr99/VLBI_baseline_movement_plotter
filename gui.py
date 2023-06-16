from matplotlibmap import draw_map
import PySimpleGUI as sg
from find_matching_station_data import find_matching_station_data
from plot_baseline import plot_lines
import json
import pandas as pd
from utility.find_matching_stations import find_matching_stations
from layout import create_layout

STATION_RADIUS = 2.0


def create_plots(values):
    """
    Collects values which shall be plotted. 

    Collects values which shall be plotted from the GUI, finds correct values
    and plots them. 

    Parameters:
    values(dict): Dictionary containing values from GUI

    Returns:
    No return values!
    """

    station1 = values["first_station"][0].split('[')[0]
    station2 = values["second_station"][0].split('[')[0]
    plotSettings = {
        "scatter": values["scatter"],
        "scatterRaw": values["scatterRaw"],
        "scatterTrimmed": values["scatterTrimmed"],
        "scatterTrendline": values["scatterTrendline"],
        "residual": values["residual"],
        "residualRaw": values["residualRaw"],
        "residualTrimmed": values["residualTrimmed"],
        "rolling_std": values["rolling_std"],
        "rolling_stdRaw": values["rolling_stdRaw"],
        "rolling_stdTrimmed": values["rolling_stdTrimmed"],
        # Plot code takes years as input, but GUI accepts amount of months
        "rolling_stdWindowSize": values["rolling_stdWindowSize"]/12
    }
    format = "png" if values["png"] else (
        "jpg" if values["jpg"] else ("pdf" if values["pdf"] else "svg"))
    viewSettings = {
        "display": values["display"],
        "save": values["save"],
        "saveFormat": format
    }
    metric = "length" if values["length"] else (
        "transverse" if values["transverse"] else "horizontal")

    find_matching_station_data(station1, station2)
    plot_lines(metric, plotSettings, viewSettings)


def disable_window_elements(elements_to_update, state, window):
    # Disables a list of elements
    for element in elements_to_update:
        window[element].update(disabled=state)


def run_gui():
    """
    Runs the GUI.

    Gives the user the ability to choose stations, change plot settings and
    change which parameter to plot.

    Parameters:
    No parameters!

    Returns:
    No return values!
    """

    with open('data/matching_stations.json', 'r') as json_file:
        matching_stations = json.load(json_file)

    stations = list(matching_stations.keys())

    station_locations = pd.read_csv("data/station_locations.csv")

    # Define the layout of the GUI
    sg.theme("DarkBlue")
    sg.SetOptions(font=("Andalde Mono", 12))

    layout = create_layout(stations)
    main_window = sg.Window('VLBI Baseline Plotter', layout,
                            margins=[20, 20], resizable=True, finalize=True)

    scatterDisabled = False
    residualDisabled = False
    rolling_stdDisabled = False
    saveDisabled = True
    available_second_stations = []

    # Event loop for the GUI
    while True:
        window, event, values = sg.read_all_windows()
        # Close main_window if user clicks cancel or closes main_window
        if event == sg.WIN_CLOSED and window == main_window or event == 'Cancel':
            break

        # Generate plots if user clicks plot
        if event == "Plot":
            create_plots(values)

        # Update the list of stations in the second list when user selects
        # the first station, and update the text for chosen station 1
        if event == "first_station":
            available_second_stations = find_matching_stations(
                values["first_station"][0])
            main_window['second_station'].update(available_second_stations)
            main_window["station1_text"].update(values["first_station"][0])

        # Update the text for chosen station 2
        if event == "second_station":
            main_window["station2_text"].update(
                values["second_station"][0].split('[')[0])

        # Disable/Enable the scatter plot settings
        if event == "scatter":
            if scatterDisabled:
                disable_window_elements(
                    ["scatterRaw", "scatterTrimmed", "scatterTrendline"], False, main_window)
                scatterDisabled = False
            else:
                disable_window_elements(
                    ["scatterRaw", "scatterTrimmed", "scatterTrendline"], True, main_window)
                scatterDisabled = True

        # Disable/Enable the residual plot settings
        if event == "residual":
            if residualDisabled:
                disable_window_elements(
                    ["residualRaw", "residualTrimmed"], False, main_window)
                residualDisabled = False
            else:
                disable_window_elements(
                    ["residualRaw", "residualTrimmed"], True, main_window)
                residualDisabled = True

        # Disable/Enable the rolling maindow std plot settings
        if event == "rolling_std":
            if rolling_stdDisabled:
                disable_window_elements(
                    ["rolling_stdRaw", "rolling_stdTrimmed", "rolling_stdWindowSize"], False, main_window)
                rolling_stdDisabled = False
            else:
                disable_window_elements(
                    ["rolling_stdRaw", "rolling_stdTrimmed", "rolling_stdWindowSize"], True, main_window)
                rolling_stdDisabled = True

        # Disable/Enable the save settings
        if event == "save":
            if saveDisabled:
                disable_window_elements(
                    ["png", "jpg", "pdf", "svg"], False, main_window)
                saveDisabled = False
            else:
                disable_window_elements(
                    ["png", "jpg", "pdf", "svg"], True, main_window)
                saveDisabled = True

        # Show the map for the first station
        if event == "map_station1":
            # Draw map
            selected_station = draw_map(
                station_locations, "Select first station")

            # Update the selection lists and text if a station was selected
            if selected_station:
                main_window["first_station"].set_value([selected_station])
                available_second_stations = find_matching_stations(
                    selected_station)
                main_window['second_station'].update(available_second_stations)
                main_window["station1_text"].update(selected_station)

        # Show the map for the second station
        if event == "map_station2":
            # Get the available stations as a DataFrame (without data point
            # count)
            available_second_stations_2 = []
            for station in available_second_stations:
                available_second_stations_2.append(station.split('[')[0])
            available_second_stations_df = station_locations.loc[station_locations['station'].isin(
                available_second_stations_2)]

            # Draw map
            selected_station = draw_map(
                available_second_stations_df, "Select second station")

            # Update the selection list and text if a station was selected
            if selected_station:
                # Get the data point count back with the station name
                selected_station_text = ""
                for station in available_second_stations:
                    if selected_station in station:
                        selected_station_text = station
                        break
                # Update list and text element
                main_window["second_station"].set_value(
                    [selected_station_text])
                main_window["station2_text"].update(selected_station_text)


if __name__ == '__main__':
    run_gui()
