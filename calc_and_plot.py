import numpy as np
from matplotlib import pyplot as plt
from scipy.fft import rfft
from scipy.io import wavfile
import time

FREQUENCIES = [440 * 2 ** ((n / 8 - 49) / 12) for n in range(88 * 8)]


def calc_fft(data, threshold, show=False, normalize=True, sample_r=44100):
    """
    Calculate the fourier-transform of the given sound data.
    :param data: '.wav' data.
    :param threshold: float between [0, 1]. Clear tones with lower amplitude relative to the greatest amplitude.
    :param show: If true, before returning the output, a graph of the transform will be shown.
    :param normalize: If true, the frequencies will be normalized into 16th of a tone gaps.
    :param sample_r:
    :return: The fourier-transform of the given sound data after applying the requested effects.
    """
    n = len(data)
    f_hat = rfft(data, n)

    f_hat = np.abs(f_hat)
    if normalize:
        f_hat = normalize_fft(f_hat, sample_r)

    max_amp = f_hat.max(initial=0)
    for i in range(len(f_hat)):
        if f_hat[i] < threshold * max_amp:
            f_hat[i] = 0

    if show:
        freq = np.fft.rfftfreq(n, d=1 / sample_r)
        plt.plot(freq, f_hat)
        plt.xlabel("Hz")
        plt.ylabel("Amplitude")
        plt.show()
    return f_hat


def normalize_fft(fft_data, sample_rate):
    """
    Normalize fft data into 16th of a tone gaps. Running complexity: O(n).
    :param fft_data: data of sound, after fourier-transform
    :param sample_rate: sample rate of the data recording
    :return: normalized frequencies.
    """
    result = np.ndarray(fft_data.shape)

    def get_index(freq):
        return int(freq / (sample_rate / (2 * len(fft_data))))  # obvious (;

    s = 0
    first_index = get_index((FREQUENCIES[0] + FREQUENCIES[1]) / 2)
    for j in range(first_index):
        s += fft_data[j]
    s /= max(first_index, 1)
    result[get_index(FREQUENCIES[0])] = s

    for i in range(1, len(FREQUENCIES) - 1):
        s = 0

        # map the indexes to the fft list
        first_index = get_index(((FREQUENCIES[i - 1] + FREQUENCIES[i]) / 2))
        last_index = get_index(((FREQUENCIES[i + 1] + FREQUENCIES[i]) / 2))

        for j in range(first_index, last_index):
            s += fft_data[j]
        s /= max(last_index - first_index, 1)

        # round every frequency to the mean
        for j in range(first_index, last_index):
            result[j] = s

    s = 0
    for j in range(first_index, len(fft_data)):
        s += fft_data[j]
    s /= max(len(fft_data) - first_index, 1)
    result[get_index(FREQUENCIES[-1])] = s

    return result


def analyze_all(data, sample_r, win_size, threshold, normalize=True, *_):
    f_hats = []
    for i in range(len(data) // win_size):
        fft = calc_fft(data[i * win_size:(i + 1) * win_size], threshold, sample_r=sample_r, normalize=normalize)
        f_hats.append(fft)
    return f_hats


def plot_wav(filename="", show_axis=(0, 1500), win_size=4410, analyzing_func=analyze_all, *func_args,
             **func_kwargs):
    """
    Show a graph of a '.wav' file amp-time-freq values.
    :param filename: '.wav' file name.
    :param show_axis: Limit the shown axis.
    :param win_size: Size of each window.
    :param analyzing_func: A function that calculate the fft output somehow. Its arguments have to contain `data`,
    `sample_r`, `win_size`. It should return a 2D array which contains the amplitude of every frequency on every time.
    :param func_args: Additional arguments that would be passed into the analyzing function.
    :param func_kwargs: Additional keyword-arguments that would be passed into the analyzing function.
    :return: Time that took for the analyzing function to run (in seconds).
    """
    sample_r, data = wavfile.read(filename)
    if isinstance(data[0], np.ndarray):
        data = data[:, 0]
    data = data * 2 ** (-15)  # normalize the amplitudes

    t0 = time.perf_counter()
    f_hats = analyzing_func(data, sample_r, win_size, *func_args, **func_kwargs)
    t1 = time.perf_counter()

    #####################################################################
    y = np.fft.rfftfreq(win_size, d=1 / sample_r)
    x = np.linspace(0, len(data) / sample_r, len(data) // win_size)

    y, x = np.meshgrid(y, x)

    z = np.array(f_hats)
    z = z[:-1, :-1]
    z_min, z_max = 0, np.abs(z).max()
    fig, ax = plt.subplots()
    #
    c = ax.pcolormesh(x, y, z, cmap='RdBu', vmin=0, vmax=z_max)
    ax.set_title("Sound- FFT")
    # set the limits of the plot to the limits of the data
    ax.axis([x.min(), x.max(), max(0, show_axis[0]), min(y.max(), show_axis[1])])
    ax.set(xlabel="Time (s)", ylabel="Freq (Hz)")

    fig.colorbar(c, ax=ax)
    plt.show()

    return t1 - t0


def main(*_):
    print(plot_wav(r"/signal processing/plot_fft/piano.wav", threshold=0.2))


if __name__ == '__main__':
    main()
