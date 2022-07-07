import random

import numpy as np
from scipy.fft import fft, rfft

SAMPLES_NORM = 200


def calculate_fft(data, absolute_thresh, sample_rate, return_absolute=True, calc_rfft=True):
    n = len(data)

    f_hat = rfft(data, n) if calc_rfft else fft(data, n)

    f_hat_abs = np.absolute(f_hat)

    dictionary = dict()
    for i in range(len(f_hat_abs)):
        if f_hat_abs[i] >= absolute_thresh:
            freq = i * sample_rate / n
            dictionary[freq] = f_hat_abs if return_absolute else f_hat[i]

    return dictionary


def approx_norm_squared(window):
    s = 0
    samples = random.sample(range(len(window)), min(SAMPLES_NORM, len(window)))

    for sample in samples:
        s += int(window[sample]) ** 2

    return s / min(SAMPLES_NORM, len(window))
