import random

import numpy as np
from scipy.fft import rfft

SAMPLES_NORM = 200


def calculate_fft(data, absolute_thresh, sample_rate):
    n = len(data)
    f_hat = rfft(data, n)

    f_hat = np.abs(f_hat)

    dictionary = dict()
    for i in range(len(f_hat)):
        if f_hat[i] >= absolute_thresh:
            dictionary[i * sample_rate / (2 * len(f_hat))] = f_hat[i]

    return dictionary


def approx_norm_squared(window):
    s = 0
    samples = random.sample(range(len(window)), min(SAMPLES_NORM, len(window)))

    for sample in samples:
        s += int(window[sample]) ** 2

    return s / min(SAMPLES_NORM, len(window))
