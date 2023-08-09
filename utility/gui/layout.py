import PySimpleGUI as sg

TABLE_LENGTH = 25
TABLE_WIDTHS = [12,6]
TABLE_HEADINGS = ["Station","Obs."]

def create_layout(stations):
    station1_col = [[sg.Text("First station:", justification="center")],
                    [sg.Table(stations, headings=TABLE_HEADINGS, key='first_station',
                                col_widths=TABLE_WIDTHS,
                                auto_size_columns=False,
                                justification='l',
                                alternating_row_color="#141F29",
                                select_mode=sg.SELECT_MODE_BROWSE,
                                expand_x=True,
                                expand_y=True,
                                enable_click_events=True)],
                    [sg.Text("", key="station1_text"), sg.Push(),
                        sg.Button("Map", key="map_station1")]]

    station2_col = [[sg.Text("Second station:", justification="center")],
                    [sg.Table([], headings=TABLE_HEADINGS, key='second_station',
                                col_widths=TABLE_WIDTHS,
                                auto_size_columns=False,
                                justification='l',
                                alternating_row_color="#141F29",
                                select_mode=sg.SELECT_MODE_BROWSE,
                                expand_x=True,
                                expand_y=True,
                                enable_click_events=True)],
                    [sg.Text("", key="station2_text"), sg.Push(),
                        sg.Button("Map", key="map_station2")]]

    metric_settings_col = [[sg.Radio("Length", "metric", default=True,
                                     key="length"),
                            sg.Radio("Transverse", "metric", key="transverse"),
                            sg.Radio("Horizontal", "metric", key="horizontal")]]

    data_selection_column = [[sg.Column(station1_col, expand_x=True, expand_y=True), sg.Column(station2_col, expand_x=True, expand_y=True)],
                             [sg.Text("Choice of metric")],
                             [sg.Column(metric_settings_col, expand_x=True)]]

    data_selection_tab = sg.Tab("Data selection", data_selection_column,
                                expand_x=True, expand_y=True)

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
                                         pad=[[0, 0], [22, 0]]),
                                    sg.Slider(range=(1, 60), resolution=1,
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

    layout = [[sg.TabGroup([[data_selection_tab, settings_tab, view_tab]], expand_x=True, expand_y=True)],
              [sg.VPush()],
              [sg.Column(buttons_col, expand_x=True, expand_y=False)]]
    return layout
