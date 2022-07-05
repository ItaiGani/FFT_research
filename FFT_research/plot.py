import matplotlib.pyplot as plt
import numpy as np
from math import floor

def plot_audio_graph(iter):
    x = []
    y = []
    z = []

    for index, heavy  in enumerate(iter):
        x += [index] * len(heavy)
        for k in heavy.keys():
            y.append(k)
            z.append(heavy[k]) 

    plt.scatter(x, y, c = z)
    plt.colorbar()
    plt.show()
    print("Asdasd")
