import numpy as np
import random

from calc_and_plot import calc_fft

PI = 3.141592653589793
E = 2.718281828459045


def chi(x, freq, sample_r):
    x /= sample_r  # x/sr because we have passed w samples from the beginning of the block
    return E ** (2j * PI * freq * x)


def guesser2(data, sample_r, win_size, alpha, gamma, t, threshold, normalize=True, *_):
    f_hats = []
    fft = calc_fft(data[0:win_size], threshold, sample_r=sample_r)
    s_hc = [(freq, fft[i]) for i, freq in enumerate(np.fft.rfftfreq(win_size, 1 / sample_r)) if fft[i] >= gamma]
    f_hats.append(fft)

    for i in range(1, len(data) // win_size):
        win = data[i * win_size:(i + 1) * win_size]

        s_hc_2 = []
        for freq, amp in s_hc:
            # compute the b fourier coefficient
            s = 0
            samples = random.sample(range(win_size), t)
            for w in samples:
                s += win[w] * chi(w, freq, sample_r)
            s /= t
            b_hat = abs(float(s))
            if b_hat >= gamma:
                s_hc_2.append((freq, amp))
        s_hc = s_hc_2

        # computing the difference
        def r(x):
            return win[x] - sum([amplitude * chi(x, freq, sample_r) for freq, amplitude in s_hc])

        norm = 0
        for z in range(win_size):
            norm += r(z) ** 2
        norm **= 1 / 2

        if norm > alpha:
            fft = calc_fft(win, threshold, sample_r=sample_r, normalize=normalize)
            s_hc = [(freq, fft[i]) for i, freq in enumerate(np.fft.rfftfreq(win_size, 1 / sample_r)) if fft[i] >= gamma]

        f_hats.append(fft)
    return f_hats


def guesser2_overlapping_windows(data, sample_r, win_size, dx, alpha, gamma, t, threshold, normalize=True, *_):
    f_hats = []
    fft = calc_fft(data[0:win_size], threshold, sample_r=sample_r)
    s_hc = [(freq, fft[i]) for i, freq in enumerate(np.fft.rfftfreq(win_size, 1 / sample_r)) if fft[i] >= gamma]
    f_hats.append(fft)

    for i in range(1, len(data) // win_size):
        win = data[i * win_size:(i + 1) * win_size]

        s_hc_2 = []
        for freq, amp in s_hc:
            # compute the b fourier coefficient
            s = 0
            samples = random.sample(range(win_size), t)
            for w in samples:
                s += win[w] * chi(w, freq, sample_r)
            s /= t
            b_hat = abs(float(s))
            if b_hat >= gamma:
                s_hc_2.append((freq, amp))
        s_hc = s_hc_2

        # computing the difference
        def r(x):
            return win[x] - sum([amplitude * chi(x, freq, sample_r) for freq, amplitude in s_hc])

        norm = 0
        for z in range(win_size):
            norm += r(z) ** 2
        norm **= 1 / 2

        if norm > alpha:
            fft = calc_fft(win, threshold, sample_r=sample_r, normalize=normalize)
            s_hc = [(freq, fft[i]) for i, freq in enumerate(np.fft.rfftfreq(win_size, 1 / sample_r)) if fft[i] >= gamma]

        f_hats.append(fft)
    return f_hats
