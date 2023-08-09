from utility.gui.map import draw_map
from utility.gui.layout import create_layout
from utility.data_selection.find_matching_station_data import find_matching_station_data
from utility.data_selection.find_matching_stations import find_matching_stations
from utility.data_selection.find_station_names import find_station_names
from utility.data_selection.match_station_location_data import match_station_location_data
from utility.plot.plot_baseline import plot_lines
import PySimpleGUI as sg
import matplotlib.pyplot as plt


def create_plots(station1, station2, values):
    """
    Collects values which shall be plotted. 

    Collects values which shall be plotted from the GUI, finds correct values
    and plots them. 

    Parameters:
    values(dict): Dictionary containing values from GUI

    Returns:
    No return values!
    """

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

    matching_rows = find_matching_station_data(station1, station2)
    plot_lines(matching_rows, metric, plotSettings, viewSettings)


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

    scatterDisabled = False
    residualDisabled = False
    rolling_stdDisabled = False
    saveDisabled = True
    first_station_list = []
    second_station_list = []
    sort_1_stat_reverse = True
    sort_1_obs_reverse = True
    sort_2_stat_reverse = True
    sort_2_obs_reverse = True
    selected_first_station = ""
    selected_second_station = ""

    first_station_list = find_station_names()
    station_locations = match_station_location_data(first_station_list)

    # Define the layout of the GUI
    sg.theme("DarkBlue")
    sg.SetOptions(font=("Andalde Mono", 12))

    layout = create_layout(first_station_list)
    main_window = sg.Window('VLBI Baseline Plotter', layout,
                            margins=[20, 20], resizable=True, finalize=True)

    # Fixes visual bug on Windows 11
    plt.figure()
    plt.close()

    # Event loop for the GUI
    while True:
        window, event, values = sg.read_all_windows()
        # Close main_window if user clicks cancel or closes main_window
        if event == sg.WIN_CLOSED and window == main_window or event == 'Cancel':
            break

        # Generate plots if user clicks plot
        if event == "Plot":
            if not (values["first_station"] and values["second_station"]):
                sg.popup("Please select two stations!",title="Warning")
            elif not (values["scatter"] or values["residual"] or values["rolling_std"]):
                sg.popup("Please select plot type!",title="Warning")
            elif values["scatter"] and not (values["scatterRaw"] or values["scatterTrimmed"] or values["scatterTrendline"]):
                sg.popup("Please select data to plot in scatter plot!",title="Warning")
            elif values["residual"] and not (values["residualRaw"] or values["residualTrimmed"]):
                sg.popup("Please select data to plot in residual plot!",title="Warning")
            elif values["rolling_std"] and not (values["rolling_stdRaw"] or values["rolling_stdTrimmed"]):
                sg.popup("Please select data to plot in std plot!",title="Warning")
            else: 
                create_plots(selected_first_station, selected_second_station, values)

        # Click on station 1 table
        if event[0] == "first_station" and event[1] == "+CLICKED+":
            
            click_row, click_col = event[2]

            # Unusable clicks
            if click_row == None or click_col == None or click_col == -1:
                continue
            
            # Sort
            elif click_row == -1:

                # Sort based on station name
                if click_col == 0:
                    first_station_list.sort(key=lambda row: row[0], reverse=sort_1_stat_reverse)
                    sort_1_stat_reverse = not sort_1_stat_reverse
                    sort_1_obs_reverse = True

                # Sort based on observation count
                elif click_col == 1:
                    first_station_list.sort(key=lambda row: row[1], reverse=sort_1_obs_reverse)
                    sort_1_obs_reverse = not sort_1_obs_reverse
                    sort_1_stat_reverse = True

                # Update the list
                main_window["first_station"].update(first_station_list)
            
            # Update the list of stations in the second list when user selects
            # the first station, and update the text for chosen station 1
            else:
                selected_first_station = first_station_list[click_row][0]
                second_station_list = find_matching_stations(selected_first_station)
                main_window['second_station'].update(second_station_list)
                main_window["station1_text"].update(selected_first_station)
                main_window["station2_text"].update("")

        # Click on station 2 table
        if event[0] == "second_station" and event[1] == "+CLICKED+":

            click_row, click_col = event[2]

            # Unusable clicks
            if click_row == None or click_col == None or click_col == -1:
                continue
            
            # Sort
            elif click_row == -1:

                # Sort based on station name
                if click_col == 0:
                    second_station_list.sort(key=lambda row: row[0], reverse=sort_2_stat_reverse)
                    sort_2_stat_reverse = not sort_2_stat_reverse
                    sort_2_obs_reverse = True

                # Sort based on observation count
                elif click_col == 1:
                    second_station_list.sort(key=lambda row: row[1], reverse=sort_2_obs_reverse)
                    sort_2_obs_reverse = not sort_2_obs_reverse
                    sort_2_stat_reverse = True

                # Update the list
                main_window["second_station"].update(second_station_list)

            else:
                selected_second_station = second_station_list[click_row][0]
                main_window["station2_text"].update(selected_second_station)

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
                selected_first_station = selected_station
                main_window["first_station"].update(select_rows = [[i[0] for i in first_station_list].index(selected_station)])
                second_station_list = find_matching_stations(selected_station)
                main_window['second_station'].update(second_station_list)
                main_window["station1_text"].update(selected_station)
                main_window["station2_text"].update("")

        # Show the map for the second station
        if event == "map_station2":
            # Get the available stations as a DataFrame (without data point
            # count)
            second_station_list_df = station_locations.loc[station_locations['station'].isin(
                [i[0] for i in second_station_list])]
            second_station_list_df = second_station_list_df.reset_index(drop=True)

            # Draw map
            selected_station = draw_map(
                second_station_list_df, "Select second station")


            # Update the selection lists and text if a station was selected
            if selected_station:
                selected_second_station = selected_station
                main_window["second_station"].update(select_rows = [[i[0] for i in second_station_list].index(selected_station)])
                main_window["station2_text"].update(selected_station)

if __name__ == '__main__':
    run_gui()
