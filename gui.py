import PySimpleGUI as sg
from find_matching_station_data import find_matching_station_data
from plot_baseline import plot_lines

stations = []
with open('stations.txt') as file:
    for line in file:
        stations.append(line)

sg.theme("DarkBlue")
col1 = [[sg.Text("First station")],
          [sg.Listbox(key='first_station', values=stations, size=(30,30))],
          [sg.Text("Plot alternatives:"),sg.Checkbox('Raw data', default=False,key='rawDataPlot')]]

col2 = [[sg.Text("Second station")],
          [sg.Listbox(key='second_station' ,values=stations, size=(30,30))],
          [sg.Push(), sg.Button('Ok'), sg.Button('Cancel')]]

layout = [
    [sg.Column(col1),
    sg.Column(col2)]
]

window = sg.Window('Best Program', layout)
return_values = ''

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    if event == "Ok":
        return_values = values
        window.close()

station1 = return_values["first_station"][0].strip('\n')
station2 = return_values["second_station"][0].strip('\n')
rawDataPlot = return_values["rawDataPlot"]

# station1 = 'KOKEE___'
# station2 = 'WETTZELL'
print(station1)
print(station2)

find_matching_station_data(station1, station2)
plot_lines()
