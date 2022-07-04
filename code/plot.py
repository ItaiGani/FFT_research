import matplotlib.pyplot as plt
from scipy.io import wavfile
import numpy as np
from math import floor


TICKS_PER_SECOND = 100
WINDOW_SIZE = 0.2


def plot_audio_graph_from_file(file_name):
    fs, signal = wavfile.read(file_name)
    plot_audio_graph(fs, signal)


def plot_audio_graph(fs, signal):
    signal = signal.T
    # For stereo:
    # signal = (signal[0] + signal[1]) / 2.0
    signal_length = len(signal)  # fs * 11
    tick_length = fs // TICKS_PER_SECOND
    samples_per_window = int(fs * WINDOW_SIZE)
    # print(samples_per_window)
    all_freqs = range(20, samples_per_window - 1200)
    bin_size = 24
    bins_num = floor(np.log(all_freqs[-1] / WINDOW_SIZE) * bin_size) + 1
    prev_to_add = 10

    i = 0
    window_start = 0
    previous_rft = []
    while window_start + samples_per_window < signal_length:
        window = signal[window_start:window_start+samples_per_window]
        ft = np.fft.fft(window, samples_per_window)

        # round
        rft = np.linspace(0+0j, 0, bins_num)
        for f in all_freqs:
            rft[floor(np.log(f / WINDOW_SIZE) * bin_size)] += ft[f]

        rft = np.abs(rft)

        to_add = min(prev_to_add, len(previous_rft))
        aft = [sum([previous_rft[-i][f] for i in range(1, to_add)], start=rft[f]) for f in range(bins_num)]

        # print(approx_avg_amplitude(window))
        thresh = 1000000 * prev_to_add
        freqs = np.array([f for f in range(bins_num) if aft[f] > thresh])
        colors = [aft[f] for f in freqs]
        freqs = freqs / bin_size
        plt.scatter(np.linspace(i, i, len(freqs)), freqs, c=colors, s=1, cmap='viridis')

        i += 1 / TICKS_PER_SECOND
        window_start += tick_length
        previous_rft.append(rft)

    plt.colorbar()
    plt.xlabel("time")
    plt.ylabel("frequency (log-scale)")
    plt.show()


plot_audio_graph_from_file("../audio_wav/400Hz.wav")
