import PySimpleGUI as sg
from find_matching_station_data import find_matching_station_data
from plot_baseline import plot_lines
import json


available_second_stations = []
with open('data/matching_stations.json', 'r') as json_file:
    matching_stations = json.load(json_file)

stations = list(matching_stations.keys())

# Define the layout of the GUI
sg.theme("DarkBlue")
sg.SetOptions(font=("Andalde Mono", 12))

station1_col = [[sg.Text("First station")],
                [sg.Listbox(key='first_station', values=stations, size=(30, 30), enable_events=True)]]

station2_col = [[sg.Text("Second station")],
                [sg.Listbox(key='second_station', values=available_second_stations, size=(30, 30))]]

scatter_col = [[sg.Checkbox('Scatter:  ', default=True, key='scatter', enable_events=True)],
               [sg.VPush()]]

scatter_settings_col = [[sg.Checkbox('Raw data', default=False, key='scatterRaw', expand_x=True)],
                        [sg.Checkbox('Trimmed data', default=True,
                                     key='scatterTrimmed', expand_x=True)],
                        [sg.Checkbox('Trend line', default=True, key='scatterTrendline', expand_x=True)]]

residual_col = [[sg.Checkbox('Residual:', default=True, key='residual', enable_events=True)],
                [sg.VPush()]]

residual_settings_col = [[sg.Checkbox('Raw data', default=False, key='residualRaw', expand_x=True)],
                         [sg.Checkbox('Trimmed data', default=True, key='residualTrimmed', expand_x=True)]]

settings_col = [[sg.Text("Plot alternatives")],
                [sg.Column(scatter_col), sg.Column(scatter_settings_col)],
                [sg.HorizontalSeparator(pad=20, color="gray")],
                [sg.Column(residual_col), sg.Column(residual_settings_col)]]

buttons_col = [[sg.Text("Choice of metric")],
               [sg.Radio("Length", "metric", default=True, key="length"), sg.Radio(
                   "Transverse", "metric", key="transverse"), sg.Radio("Horizontal", "metric", key="horizontal")],
               [sg.VPush()],
               [sg.Button('Plot'), sg.Button('Cancel')]]

layout = [[sg.Column(station1_col), sg.Column(station2_col)],
          [sg.HorizontalSeparator(pad=20)],
          [sg.Column(settings_col), sg.VerticalSeparator(pad=20), sg.Push(), sg.Column(buttons_col, vertical_alignment='bottom')]]

window = sg.Window('VLBI Baseline Plotter', layout)
return_values = {}

# Define what the events (button presses and selections) do
scatterDisabled = False
residualDisabled = False

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
        break
    if event == "Plot":
        return_values = values
        window.close()
    if event == "first_station":
        available_second_stations = matching_stations[values["first_station"][0]]
        window['second_station'].update(available_second_stations)
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
    if event == "residual":
        if residualDisabled:
            window["residualRaw"].update(disabled=False)
            window["residualTrimmed"].update(disabled=False)
            residualDisabled = False
        else:
            window["residualRaw"].update(disabled=True)
            window["residualTrimmed"].update(disabled=True)
            residualDisabled = True


station1 = return_values["first_station"][0].split('[')[0]
station2 = return_values["second_station"][0].split('[')[0]
plotSettings = {
    "scatter": return_values["scatter"],
    "scatterRaw": return_values["scatterRaw"],
    "scatterTrimmed": return_values["scatterTrimmed"],
    "scatterTrendline": return_values["scatterTrendline"],
    "residual": return_values["residual"],
    "residualRaw": return_values["residualRaw"],
    "residualTrimmed": return_values["residualTrimmed"],
    "residualLine": True
}
metric = "length" if return_values["length"] else "transverse"
metric = "transverse" if return_values["transverse"] else "horizontal"

find_matching_station_data(station1, station2)
plot_lines(metric, plotSettings)
