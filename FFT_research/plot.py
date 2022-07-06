import matplotlib.pyplot as plt
import numpy as np
import math

def plot_audio_graph(iter, title = "transform fourier", scale: bool = False):
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

    transparency_list = []
    max_amp, min_amp = max(z), min(z)
    for amp in z:
        transparency_list.append(0.9 * (amp-min_amp)/(max_amp-min_amp) + 0.1)
    sc = ax.scatter(x, y, c = z, alpha = transparency_list)
    ax.set_xlabel("windows")
    if(scale):
        ax.set_ylabel("frequency Hz (log 2 base)")
    else:
        ax.set_ylabel("frequency Hz")
    ax.set_title(title)
    cbar = fig.colorbar(sc)
    cbar.set_label("Amplitude", loc='center')
    yabs_max = max(y)
    if(scale):
        ax.set_ylim(ymin=0, ymax = yabs_max + 1)
    else:
        ax.set_ylim(ymin=0, ymax = yabs_max + 150)
    plt.show()
