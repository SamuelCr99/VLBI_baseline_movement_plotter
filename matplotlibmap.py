import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
import numpy as np
from PIL import Image
import pandas as pd
import math
import warnings
warnings.filterwarnings('ignore')

STATION_DRAW_RADIUS = 60.0
STATION_CLICK_RADIUS = 1
global_station_location = []
selected_station = ""
mouse_on_station = ""
text = None

def map_to_fig(coordinates):
    map_x = coordinates[0]
    map_y = coordinates[1]

    fig_x = 954+map_x*1908/360
    fig_y = 477-map_y*954/180

    return [fig_x,fig_y]


def fig_to_map(coordinates):
    fig_x = coordinates[0]
    fig_y = coordinates[1]

    map_x = (fig_x-954)*360/1908
    map_y = (477-fig_y)*180/954

    return [map_x,map_y]


def on_click(event):
    global selected_station 
    x,y = fig_to_map([event.xdata, event.ydata])
    distance_to_stations = global_station_location.copy()
    distance_to_stations["distance"] = distance_to_stations.apply(lambda s: math.sqrt(math.pow(s["x"]-x,2)+math.pow(s["y"]-y,2)), axis=1)
    distance_to_stations.sort_values("distance", inplace=True)
    distance_to_stations.reset_index(inplace=True)
    if distance_to_stations.loc[0].distance <= STATION_CLICK_RADIUS:
        selected_station = distance_to_stations.loc[0]['station']
        plt.close()
        
def on_move(event):
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
        try:
            with plt.ion():
                # plt.pause(0.05)
                text.remove()
        except:
            pass
        if mouse_on_station != "": 
            with plt.ion():
                # plt.pause(0.05)
                text = plt.text(event.xdata + 10, event.ydata + 10, mouse_on_station, size=12)

def draw_map(station_coordinates, title):
    global selected_station
    selected_station = ""
    
    global global_station_location
    global_station_location = station_coordinates

    global mouse_on_station
    mouse_on_station = ""

    global text
    text = None

    fig, ax = plt.subplots(figsize=(10,5), num=title)
    
    fig.canvas.mpl_connect('button_press_event', on_click)
    fig.canvas.mpl_connect('motion_notify_event', on_move)

    img = np.asarray(Image.open('world_map.png'))
    plt.imshow(img)

    station_coordinates["fig_x"] = station_coordinates.apply(lambda s: map_to_fig([s.x,s.y])[0], axis=1)
    station_coordinates["fig_y"] = station_coordinates.apply(lambda s: map_to_fig([s.x,s.y])[1], axis=1)
    ax.scatter(station_coordinates.fig_x.to_list(),station_coordinates.fig_y.to_list(),STATION_DRAW_RADIUS,"black")
    ax.scatter(station_coordinates.fig_x.to_list(),station_coordinates.fig_y.to_list(),STATION_DRAW_RADIUS*0.5,"white")
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.show()
    print(f'Selected station: {selected_station}')

    # fig.canvas.mpl_disconnect('button_press_event')
    # fig.canvas.mpl_disconnect('motion_notify_event')
    # plt.ioff()
    plt.close('all')
    return selected_station
