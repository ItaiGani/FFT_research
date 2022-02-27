import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
import matplotlib.cm as cm
import matplotlib.colors as colors


def reduced_signal(f, g):
    """ computes the difference between f and g """
    return f - g


def norm(f):
    """ computes the norm (times 100 for convenience) of a function """
    return 100 * np.sqrt(np.sum(f ** 2))


def add_points(freq, fft_controll, points, moving):
    freq = 440 * 2 ** (np.round(np.log(freq / 440) * 48) / 48)  # round to musical tone
    for i in range(len(freq)):
        if 0 < fft_controll[i]:  # looking at amplitudes of the spikes higher than 0
            points.append([moving / check_rate, freq[i], fft_controll[i]])


def fft(path):
    """ computes the frequency and amplitude """
    sampFreq, sound = wavfile.read(path)  # sampFreq = 44.1 kHz
    sound = sound / 2.0 ** 15  # normalize the frequency
    signal = sound[:, 0] # only right ear
    signal = signal[:length_of_fft * sampFreq:]
    window = int(signal.size / (length_of_fft * check_rate))
    freq = np.fft.rfftfreq(window, d=1 / sampFreq)

    # first function
    win_controll = np.array(signal[:window:])
    fft_controll = np.abs(np.fft.rfft(signal[:window:]))

    points = []
    # windows in time
    for moving in range(length_of_fft * check_rate):
        # reduced function, instead of calc every coefficient we check if the heavy coefficient hasn't changed
        win = np.array(signal[window * moving:window * (moving + 1):])
        r_i = reduced_signal(win, win_controll)
        # check if the reduced function is good enough
        _norm = norm(r_i)
        if _norm <= alpha:
            print("norm is: ", str(round(_norm, 2)) + "; good enough!")
            add_points(freq, fft_controll, points, moving)
        else:
            print("norm is: ", str(round(_norm, 2)) + "; calculating again!")
            fft_controll = np.abs(np.fft.rfft(signal[window * moving:window * (moving + 1):]))
            add_points(freq, fft_controll, points, moving)
        win_controll = np.array(signal[window * moving:window * (moving + 1):])
    return np.array(points)


def filter(points):
    """ filter all bad points based on amplitude """
    bar = (max(points[::, 2]) * spike) / 100
    filtered_p = []
    for x in points:
        if x[2] >= bar:
            filtered_p.append(x)
    return np.array(filtered_p)



def label_maker(lst):
    """ makes the range of labels on the graph """
    label = list(set(np.round(np.arange(0, max(lst) + 1, max(lst) / 10))))
    return np.array(label)


def plot(points):
    """ plots the graph """
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['figure.figsize'] = (9, 7)
    plt.xlabel("time[s]")
    plt.ylabel("frequency[hz]")
    t = points[::, 0]
    f = points[::, 1]
    a = points[::, 2]
    c_norm = colors.Normalize(vmin=0, vmax=max(a))
    plt.scatter(t, f, c=a, cmap='viridis', norm=c_norm)
    y_label = label_maker(a)
    plt.colorbar(cm.ScalarMappable(cmap='viridis', norm=c_norm), ticks=y_label, label='amplitude')
    t_label = label_maker(t)
    plt.xticks(t_label, t_label)
    x_label = label_maker(f)
    plt.yticks(x_label, x_label)
    plt.show()


if __name__ == '__main__':
    path = 'SoundFiles/110hz.wav'
    length_of_fft = 60  # seconds of the song
    check_rate = 10  # 1/check_rate samples in a second
    spike = 5 # how much percent of low amplitude points to kick
    alpha = 100  # norm change, the more high the less accurate the next time window will have to be

    plot(filter(fft(path)))
