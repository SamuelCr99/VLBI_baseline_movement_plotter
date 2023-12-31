import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
from PIL import Image
import warnings
import mplcursors
import PySimpleGUI as sg
from math import sqrt
warnings.filterwarnings('ignore')

# Global variables
STATION_DRAW_RADIUS = 60.0
MIN_STATION_DISTANCE = 2

def draw_fig(canvas, fig, canvas_toolbar):
    if canvas.children:
        for child in canvas.winfo_children():
            child.destroy()
    if canvas_toolbar.children:
        for child in canvas_toolbar.winfo_children():
            child.destroy()
    figure_canvas_agg = FigureCanvasTkAgg(fig, master=canvas)
    toolbar = Toolbar(figure_canvas_agg, canvas_toolbar)
    figure_canvas_agg.get_tk_widget().pack(side='right', fill='both', expand=1)
    figure_canvas_agg.draw()
    toolbar.update()


class Toolbar(NavigationToolbar2Tk):
    def __init__(self, *args, **kwargs):
        super(Toolbar, self).__init__(*args, **kwargs)


def map_to_fig(coordinates):
    # Converts map coordinates to figure coordinates
    map_x = coordinates[0]
    map_y = coordinates[1]

    if map_x == None or map_y == None:
        return [0, 0]

    fig_x = 954+map_x*1908/360
    fig_y = 477-map_y*954/180

    return [fig_x, fig_y]


def move_coords_too_close(coords):
    for index, coord in coords.iterrows():
        x = coord.pixel_coordinates[0]
        y = coord.pixel_coordinates[1]

        check = True

        while check:
            check = False
            for coord_other in coords.pixel_coordinates:
                x_other = coord_other[0]
                y_other = coord_other[1]
                x_delta = x_other-x
                y_delta = y_other-y
                distance = sqrt((x_delta)**2 + (y_delta)**2)

                if distance < MIN_STATION_DISTANCE:
                    x += MIN_STATION_DISTANCE
                    check = True
                    break
        coords.pixel_coordinates.iloc[index] = [x,y]

def fig_to_map(coordinates):
    # Converts figure coordinates to map coordinates
    fig_x = coordinates[0]
    fig_y = coordinates[1]

    if fig_x == None or fig_y == None:
        return [0, 0]

    map_x = (fig_x-954)*360/1908
    map_y = (477-fig_y)*180/954

    return [map_x, map_y]


def draw_map(station_coordinates, title):
    """
    Draws world map with station locations to a new window

    Draws a world map with station locations to a new window, the stations can
    then be hovered to display name and pressed to be selected. 

    Parameters: 
    station_coordinates(Pandas DataFrame): Pandas DF containing all station 
    coordinates. 
    title(str): Title of window

    Returns: 
    str: Returns the name of selected station 
    """
    # Prepare the coordinates for the stations
    station_coordinates["pixel_coordinates"] = station_coordinates.apply(
        lambda s: map_to_fig([s.x, s.y]), axis=1)
    
    # Move points that are too close to other points
    move_coords_too_close(station_coordinates)

    # Draw the map
    fig, ax = plt.subplots(figsize=(10, 5), num=title)
    img = np.asarray(Image.open('resources/world_map.png'))
    ax.imshow(img)

    pixel_x = [i[0] for i in station_coordinates.pixel_coordinates]
    pixel_y = [i[1] for i in station_coordinates.pixel_coordinates]

    # Draw station locations on to screen
    station_points = ax.scatter(pixel_x, pixel_y, STATION_DRAW_RADIUS, "black")
    ax.scatter(pixel_x, pixel_y, STATION_DRAW_RADIUS*0.5, "white")

    plt.axis('off')
    plt.tight_layout(pad=0)

    # Add labels to the stations
    cursor_hover = mplcursors.cursor(
            station_points, hover=mplcursors.HoverMode.Transient)
    cursor_hover.connect(
        "add", lambda sel: sel.annotation.set_text(station_coordinates.loc[sel.index].station))

    # Add a "click"-listener to the stations
    cursor_click = mplcursors.cursor(station_points)
    cursor_click.connect("add", lambda sel: map_window.write_event_value("selected",sel.index))

    # Open the window
    layout = [[sg.Canvas(s=(1000,500), key='map_canvas', expand_x=True, expand_y=True)],
              [sg.Canvas(s=(1000,50), key="toolbar_canvas", expand_x=True, expand_y=False)]]
    map_window = sg.Window(title, layout, resizable=True, finalize=True, modal=True, margins=(0,0), element_padding=0)
    draw_fig(map_window['map_canvas'].TKCanvas, fig, map_window['toolbar_canvas'].TKCanvas)

    # Wait for a selection or close
    while True:
        event, values = map_window.read()
        if event == "selected":
            selected_station = station_coordinates.station.iloc[values["selected"]]
            plt.close(fig=title)
            map_window.close()
            break

        elif event == sg.WINDOW_CLOSED:
            selected_station = ""
            plt.close(fig=title)
            map_window.close()
            break

    # Return the selected station
    return selected_station
