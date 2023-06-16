import PySimpleGUI as sg
from find_matching_station_data import find_matching_station_data
from plot_baseline import plot_lines
import json
import sys
import pandas as pd
import math
sys.path.insert(0, './utility')
from find_matching_stations import find_matching_stations
from matplotlibmap import draw_map

LISTBOX_WIDTH = 40
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
    format = "png" if values["png"] else ("jpg" if values["jpg"] else ("pdf" if values["pdf"] else "svg"))
    viewSettings = {
        "display": values["display"],
        "save": values["save"],
        "saveFormat": format
    }
    metric = "length" if values["length"] else (
        "transverse" if values["transverse"] else "horizontal")

    find_matching_station_data(station1, station2)
    plot_lines(metric, plotSettings, viewSettings)


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

    station1_col = [[sg.Text("First station:", justification="center")],
                    [sg.Listbox(key='first_station', values=stations,
                                size=(LISTBOX_WIDTH, 20), enable_events=True)],
                    [sg.Text("", key="station1_text"), sg.Push(),
                     sg.Button("Map", key="map_station1")]]

    station2_col = [[sg.Text("Second station:", justification="center")],
                    [sg.Listbox(key='second_station', values=[],
                                size=(LISTBOX_WIDTH, 20), enable_events=True)],
                    [sg.Text("", key="station2_text"), sg.Push(),
                     sg.Button("Map", key="map_station2")]]
    
    metric_settings_col = [[sg.Radio("Length", "metric", default=True,
                                     key="length"),
                            sg.Radio("Transverse", "metric", key="transverse"),
                            sg.Radio("Horizontal", "metric", key="horizontal")]]
    
    data_selection_column = [[sg.Column(station1_col), sg.Column(station2_col)],
                             [sg.Text("Choice of metric")],
                             [sg.Column(metric_settings_col, expand_x=True)]]

    data_selection_tab = sg.Tab("Data selection", data_selection_column,
                                expand_x=True)

    scatter_settings_col = [[sg.Checkbox('Raw data', default=False,
                                         key='scatterRaw', expand_x=True)],
                            [sg.Checkbox('Trimmed data', default=True,
                                         key='scatterTrimmed', expand_x=True)],
                            [sg.Checkbox('Trend line', default=True,
                                         key='scatterTrendline', expand_x=True)]]

    residual_settings_col = [[sg.Checkbox('Raw data', default=False,
                                          key='residualRaw', expand_x=True)],
                             [sg.Checkbox('Trimmed data', default=True,
                                          key='residualTrimmed',
                                          expand_x=True)]]

    rolling_std_settings_col = [[sg.Checkbox('Raw data', default=False,
                                             key='rolling_stdRaw',
                                             expand_x=True)],
                                [sg.Checkbox(
                                    'Trimmed data', default=True,
                                    key='rolling_stdTrimmed', expand_x=True)],
                                [sg.Text("Window size (months)",
                                         pad=[[0,0],[22,0]]),
                                         sg.Slider(range=(0, 60), resolution=1,
                                                   orientation="h",
                                                   default_value=12,
                                                   key="rolling_stdWindowSize")]]

    settings_col = [[sg.Checkbox('Scatter', default=True, key='scatter',
                                 enable_events=True)],
                    [sg.Column(scatter_settings_col, pad=[
                               [40, 0], [0, 20]], expand_x=True)],
                    [sg.Checkbox('Residual', default=True,
                                 key='residual', enable_events=True)],
                    [sg.Column(residual_settings_col, pad=[
                               [40, 0], [0, 20]], expand_x=True)],
                    [sg.Checkbox('Rolling window std', default=True,
                                 key='rolling_std', enable_events=True)],
                    [sg.Column(rolling_std_settings_col, pad=[
                               [40, 0], [0, 0]], expand_x=True)]]

    settings_tab = sg.Tab("Plot settings", [[sg.Column(
        settings_col, expand_x=True, expand_y=True, pad=20)]])
    
    view_col = [[sg.Checkbox("Display plots", default=True, key="display")],
                [sg.Checkbox("Save plots", default=False, key="save",
                             enable_events=True)],
                [sg.Text("Format: ", pad=[[40, 0], [0, 0]]),
                 sg.Radio("PNG", "saveFormat", default=True, key="png",
                          disabled=True),
                 sg.Radio("JPG", "saveFormat", key="jpg", disabled=True),
                 sg.Radio("PDF", "saveFormat", key="pdf", disabled=True),
                 sg.Radio("SVG", "saveFormat", key="svg", disabled=True)]]
    
    view_tab = sg.Tab("View settings", [[sg.Column(
        view_col, expand_x=True, expand_y=True, pad=20)]])

    buttons_col = [[sg.VPush()],
                   [sg.Push(), sg.Button('Plot'), sg.Button('Cancel')]]

    layout = [[sg.TabGroup([[data_selection_tab, settings_tab, view_tab]])],
              [buttons_col]]

    main_window = sg.Window('VLBI Baseline Plotter', layout,
                       margins=[20, 20], resizable=True, finalize=True)

    # Define what the events (button presses and selections) do
    scatterDisabled = False
    residualDisabled = False
    rolling_stdDisabled = False
    saveDisabled = True
    available_second_stations = []

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
            main_window["station2_text"].update(values["second_station"][0].split('[')[0])

        # Disable/Enable the scatter plot settings
        if event == "scatter":
            if scatterDisabled:
                main_window["scatterRaw"].update(disabled=False)
                main_window["scatterTrimmed"].update(disabled=False)
                main_window["scatterTrendline"].update(disabled=False)
                scatterDisabled = False
            else:
                main_window["scatterRaw"].update(disabled=True)
                main_window["scatterTrimmed"].update(disabled=True)
                main_window["scatterTrendline"].update(disabled=True)
                scatterDisabled = True

        # Disable/Enable the residual plot settings
        if event == "residual":
            if residualDisabled:
                main_window["residualRaw"].update(disabled=False)
                main_window["residualTrimmed"].update(disabled=False)
                residualDisabled = False
            else:
                main_window["residualRaw"].update(disabled=True)
                main_window["residualTrimmed"].update(disabled=True)
                residualDisabled = True

        # Disable/Enable the rolling maindow std plot settings
        if event == "rolling_std":
            if rolling_stdDisabled:
                main_window["rolling_stdRaw"].update(disabled=False)
                main_window["rolling_stdTrimmed"].update(disabled=False)
                main_window["rolling_stdWindowSize"].update(disabled=False)
                rolling_stdDisabled = False
            else:
                main_window["rolling_stdRaw"].update(disabled=True)
                main_window["rolling_stdTrimmed"].update(disabled=True)
                main_window["rolling_stdWindowSize"].update(disabled=True)
                rolling_stdDisabled = True

        # Disable/Enable the save settings
        if event == "save":
            if saveDisabled:
                main_window["png"].update(disabled=False)
                main_window["jpg"].update(disabled=False)
                main_window["pdf"].update(disabled=False)
                main_window["svg"].update(disabled=False)
                saveDisabled = False
            else:
                main_window["png"].update(disabled=True)
                main_window["jpg"].update(disabled=True)
                main_window["pdf"].update(disabled=True)
                main_window["svg"].update(disabled=True)
                saveDisabled = True

        if event == "map_station1":
            selected_station = draw_map(station_locations, "Select first station")
            if selected_station:
                main_window["first_station"].set_value([selected_station])
                available_second_stations = find_matching_stations(selected_station)
                main_window['second_station'].update(available_second_stations)
                main_window["station1_text"].update(selected_station)

        if event == "map_station2":
            available_second_stations_2 = []
            for station in available_second_stations: 
                available_second_stations_2.append(station.split('[')[0])
            available_second_stations_df = station_locations.loc[station_locations['station'].isin(available_second_stations_2)]
            
            selected_station = draw_map(available_second_stations_df, "Select second station")
            if selected_station:
                selected_station_text = ""
                for station in available_second_stations:
                    if selected_station in station:
                        selected_station_text = station
                        break
                main_window["second_station"].set_value([selected_station_text])
                main_window["station2_text"].update(selected_station_text)


if __name__ == '__main__':
    run_gui()
