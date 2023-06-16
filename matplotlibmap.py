import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
import numpy as np
from PIL import Image

STATION_RADIUS = 60.0

def map_to_fig(coordinates):
    map_x = coordinates[0]
    map_y = coordinates[1]

    fig_x = 954+map_x*1908/360
    fig_y = 477-map_y*954/180

    print([fig_x, fig_y])
    return([fig_x,fig_y])


def fig_to_map(coordinates):
    fig_x = coordinates[0]
    fig_y = coordinates[1]

    map_x = (fig_x-954)*360/1908
    map_y = (477-fig_y)*180/954

    return([map_x,map_y])


def mouse_event(event):
    print(fig_to_map([event.xdata, event.ydata]))
    return fig_to_map([event.xdata, event.ydata])


def draw_map(station_coordinates):
    fig = plt.figure(figsize=(10,5))
    ax = fig.gca()
    fig.canvas.mpl_connect('button_press_event', mouse_event)

    img = np.asarray(Image.open('world_map.png'))
    plt.imshow(img)
    ax.scatter(954,477,STATION_RADIUS,"black")
    ax.scatter(954,477,STATION_RADIUS*0.7,"white")
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.show()


if __name__ == '__main__':
    draw_map([])