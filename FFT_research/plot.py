import matplotlib.pyplot as plt
import numpy as np
import math

def plot_audio_graph(iter, title = "FFT", scale: bool = False):
    fig, ax = plt.subplots() 
    x = []
    y = []
    z = []

    for index, heavy  in enumerate(iter):
        x += [index] * len(heavy)
        for k in heavy.keys():
            if(scale):
                y.append(math.log(k,2))
            else:
                y.append(k)
            z.append(heavy[k]) 

    sc = ax.scatter(x, y, c = z)
    ax.set_xlabel("windows")
    if(scale):
        ax.set_ylabel("frequency Hz (log 2 base)")
    else:
        ax.set_ylabel("frequency Hz")
    ax.set_title(title)
    cbar = fig.colorbar(sc)
    cbar.set_label("Amplitude", loc='center')
    plt.show()
