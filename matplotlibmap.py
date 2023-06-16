import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import pandas as pd
from matplotlib.backend_bases import MouseButton
import math
import warnings
warnings.filterwarnings('ignore')

# Global variables
STATION_DRAW_RADIUS = 60.0
STATION_CLICK_RADIUS = 1
global_station_location = []
selected_station = ""
mouse_on_station = ""
text = None

def map_to_fig(coordinates):
    map_x = coordinates[0]
    map_y = coordinates[1]

    if map_x == None or map_y == None: 
        return [0,0] 

    fig_x = 954+map_x*1908/360
    fig_y = 477-map_y*954/180

    return [fig_x,fig_y]


def fig_to_map(coordinates):
    fig_x = coordinates[0]
    fig_y = coordinates[1]

    if fig_x == None or fig_y == None: 
        return [0,0] 


    map_x = (fig_x-954)*360/1908
    map_y = (477-fig_y)*180/954

    return [map_x,map_y]

def on_move(event):
    if event.inaxes:
        global mouse_on_station
        global text
        x,y = fig_to_map([event.xdata, event.ydata])
        distance_to_stations = global_station_location.copy()
        distance_to_stations["distance"] = distance_to_stations.apply(lambda s: math.sqrt(math.pow(s["x"]-x,2)+math.pow(s["y"]-y,2)), axis=1)
        distance_to_stations.sort_values("distance", inplace=True)
        distance_to_stations.reset_index(inplace=True)
        old_mouse_on_station = mouse_on_station
        if distance_to_stations.loc[0].distance <= STATION_CLICK_RADIUS:
            mouse_on_station = distance_to_stations.loc[0]['station']
        else:
            mouse_on_station = ""

        if (mouse_on_station != old_mouse_on_station):
            text.set_text(mouse_on_station)
            text.set_position([event.xdata+5, event.ydata + 5])

def on_click(event):
    if event.button is MouseButton.LEFT:
        global selected_station 
        x,y = fig_to_map([event.xdata, event.ydata])
        distance_to_stations = global_station_location.copy()
        distance_to_stations["distance"] = distance_to_stations.apply(lambda s: math.sqrt(math.pow(s["x"]-x,2)+math.pow(s["y"]-y,2)), axis=1)
        distance_to_stations.sort_values("distance", inplace=True)
        distance_to_stations.reset_index(inplace=True)
        if distance_to_stations.loc[0].distance <= STATION_CLICK_RADIUS:
            selected_station = distance_to_stations.loc[0]['station']
            plt.close('all')


def draw_map(station_coordinates, title):
    global selected_station
    selected_station = ""
    
    global global_station_location
    global_station_location = station_coordinates

    global mouse_on_station
    mouse_on_station = ""

    global text

    station_coordinates["fig_x"] = station_coordinates.apply(lambda s: map_to_fig([s.x,s.y])[0], axis=1)
    station_coordinates["fig_y"] = station_coordinates.apply(lambda s: map_to_fig([s.x,s.y])[1], axis=1)

    # Draw the map
    plt.ion()
    _, ax = plt.subplots(figsize=(10,5), num=title)
    text = plt.text(0, 0, "", size=12, color="black", backgroundcolor="white")
    img = np.asarray(Image.open('world_map.png'))
    plt.imshow(img)
    ax.scatter(station_coordinates.fig_x.to_list(),station_coordinates.fig_y.to_list(),STATION_DRAW_RADIUS,"black")
    ax.scatter(station_coordinates.fig_x.to_list(),station_coordinates.fig_y.to_list(),STATION_DRAW_RADIUS*0.5,"white")
    plt.axis('off')
    plt.tight_layout(pad=0)

    # Add the events to the event loop
    plt.connect('motion_notify_event', on_move)
    plt.connect('button_press_event', on_click)

    # Show the map
    plt.show(block=True)

    # Return the selected station
    print(f'Selected station: {selected_station}')
    return selected_station
