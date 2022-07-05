import numpy as np
from scipy.fft import rfft


def calculate_fft(data, thresh, sample_rate):
    n = len(data)
    f_hat = rfft(data, n)

    f_hat = np.abs(f_hat)

    dictionary = dict()
    for i in range(len(f_hat)):
        if f_hat[i] >= thresh:
            dictionary[i * sample_rate / (2 * len(f_hat))] = f_hat[i]

    return dictionary 