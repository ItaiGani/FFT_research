import math

import matplotlib.pyplot as plt

# Constants
close_amplitudes = 0.8
min_frequnecy = 0


def plot_audio_graph(iter, title="transform fourier", scale: bool = False):
    fig, ax = plt.subplots()
    x = []
    y = []
    z = []

    for index, heavy in enumerate(iter):
        x += [index] * len(heavy)
        for k in heavy.keys():
            if scale:
                y.append(math.log(k, 2))
            else:
                y.append(k)
            z.append(heavy[k])

    transparency_list = []
    max_amp, min_amp = max(z), min(z)
    if min_amp > max_amp * close_amplitudes:
        f = lambda amp: min((1 - close_amplitudes) * (amp - min_amp) / (max_amp - min_amp) + close_amplitudes, 1)
    else:
        f = lambda amp: min(0.9 * (amp - min_amp) / (max_amp - min_amp) + 0.1, 1)
    for amp in z:
        transparency_list.append(f(amp))
    x.append(0), y.append(0), z.append(0), transparency_list.append(0)
    sc = ax.scatter(x, y, c=z, alpha=transparency_list)
    ax.set_xlabel("windows")
    if scale:
        ax.set_ylabel("frequency Hz (log 2 base)")
    else:
        ax.set_ylabel("frequency Hz")
    ax.set_title(title)
    cbar = fig.colorbar(sc)
    cbar.set_label("Amplitude", loc='center')
    if scale:
        ax.set_ylim(ymin=min_frequnecy, ymax=max(y) + 1)
    else:
        ax.set_ylim(ymin=min_frequnecy, ymax=max(y) + 150)
    plt.show()
