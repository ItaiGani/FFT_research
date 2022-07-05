import matplotlib.pyplot as plt
import numpy as np
import math

def plot_audio_graph(iter):
    fig, ax = plt.subplots() 
    x = []
    y = []
    z = []

    for index, heavy  in enumerate(iter):
        x += [index] * len(heavy)
        for k in heavy.keys():
            y.append(math.log(k,2))
            z.append(heavy[k]) 

    sc = ax.scatter(x, y, c = z)
    ax.set_xlabel("windows")
    ax.set_ylabel("frequency (log 2 scale)")
    ax.set_title("FFT")
    cbar = fig.colorbar(sc)
    cbar.set_label("Amplitude", loc='center')
    plt.show()
