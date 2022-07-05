import matplotlib.pyplot as plt
import numpy as np
from math import floor
from fft_stream_interface import FFTHC

TICKS_PER_SECOND = 100


def plot_audio_graph(freq, signal, window_size=0.2):
    signal = signal.T
    # For stereo:
    # signal = (signal[0] + signal[1]) / 2.0
    signal_length = len(signal)  # freq * 11
    tick_length = freq // TICKS_PER_SECOND
    samples_per_window = int(freq * window_size)
    # print(samples_per_window)
    all_freqs = range(20, samples_per_window - 1200)
    bin_size = 24
    bins_num = floor(np.log(all_freqs[-1] / window_size) * bin_size) + 1
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
            rft[floor(np.log(f / window_size) * bin_size)] += ft[f]

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


a = FFTHC("../audio_wav/400Hz.wav")