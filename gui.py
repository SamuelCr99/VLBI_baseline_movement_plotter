import PySimpleGUI as sg
from find_matching_station_data import find_matching_station_data
from plot_baseline import plot_lines
import json
import sys
sys.path.insert(0, './utility')
from find_matching_stations import find_matching_stations

LISTBOX_WIDTH = 40

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

    # Define the layout of the GUI
    sg.theme("DarkBlue")
    sg.SetOptions(font=("Andalde Mono", 12))

    station1_col = [[sg.Text("First station:", justification="center")],
                    [sg.Listbox(key='first_station', values=stations,
                                size=(LISTBOX_WIDTH, 20), enable_events=True)]]

    station2_col = [[sg.Text("Second station:", justification="center")],
                    [sg.Listbox(key='second_station', values=[],
                                size=(LISTBOX_WIDTH, 20))]]
    
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

    window = sg.Window('VLBI Baseline Plotter', layout,
                       margins=[20, 20], resizable=True)

    # Define what the events (button presses and selections) do
    scatterDisabled = False
    residualDisabled = False
    rolling_stdDisabled = False
    saveDisabled = True

    while True:
        event, values = window.read()

        # Close window if user clicks cancel or closes window
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break

        # Generate plots if user clicks plot
        if event == "Plot":
            create_plots(values)

        # Update the list of stations in the second list when user selects
        # the first station
        if event == "first_station":
            available_second_stations = find_matching_stations(
                values["first_station"][0])
            window['second_station'].update(available_second_stations)

        # Disable/Enable the scatter plot settings
        if event == "scatter":
            if scatterDisabled:
                window["scatterRaw"].update(disabled=False)
                window["scatterTrimmed"].update(disabled=False)
                window["scatterTrendline"].update(disabled=False)
                scatterDisabled = False
            else:
                window["scatterRaw"].update(disabled=True)
                window["scatterTrimmed"].update(disabled=True)
                window["scatterTrendline"].update(disabled=True)
                scatterDisabled = True

        # Disable/Enable the residual plot settings
        if event == "residual":
            if residualDisabled:
                window["residualRaw"].update(disabled=False)
                window["residualTrimmed"].update(disabled=False)
                residualDisabled = False
            else:
                window["residualRaw"].update(disabled=True)
                window["residualTrimmed"].update(disabled=True)
                residualDisabled = True

        # Disable/Enable the rolling window std plot settings
        if event == "rolling_std":
            if rolling_stdDisabled:
                window["rolling_stdRaw"].update(disabled=False)
                window["rolling_stdTrimmed"].update(disabled=False)
                window["rolling_stdWindowSize"].update(disabled=False)
                rolling_stdDisabled = False
            else:
                window["rolling_stdRaw"].update(disabled=True)
                window["rolling_stdTrimmed"].update(disabled=True)
                window["rolling_stdWindowSize"].update(disabled=True)
                rolling_stdDisabled = True

        # Disable/Enable the save settings
        if event == "save":
            if saveDisabled:
                window["png"].update(disabled=False)
                window["jpg"].update(disabled=False)
                window["pdf"].update(disabled=False)
                window["svg"].update(disabled=False)
                saveDisabled = False
            else:
                window["png"].update(disabled=True)
                window["jpg"].update(disabled=True)
                window["pdf"].update(disabled=True)
                window["svg"].update(disabled=True)
                saveDisabled = True


if __name__ == '__main__':
    run_gui()
