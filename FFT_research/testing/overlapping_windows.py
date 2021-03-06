import math
import random
import sys

sys.path.append("../FFT_research")
from FFT_research.fft_stream_interface import FFTHC
from FFT_research.calculate_hc_fft import approx_norm_squared, calculate_fft


class Overlapping_Windows(FFTHC):
    def __init__(self, filename: str, thresh: float = 0, win_size: float = 0.1, win_overlap: float = 0,
                 mode: int = 0) -> None:
        super().__init__(filename, thresh, win_size, win_overlap, mode)

    def calculate(self, samples_number=100, a=10):
        overlapping_samples = self.samples_per_window * self.win_overlap
        samples_step = int(self.samples_per_window - overlapping_samples)
        number_of_wins = math.ceil(
            (len(self.signal) - self.samples_per_window) / (self.samples_per_window - overlapping_samples)) + 1

        window = self.signal[0: self.samples_per_window]
        absolute_thresh = self.thresh * (approx_norm_squared(window) ** 0.5)
        last_fft = calculate_fft(window, absolute_thresh, self.sample_rate)
        last_fft_index = 0
        res = [last_fft]

        for i in range(1, number_of_wins):
            window = self.signal[i * samples_step: i * samples_step + self.samples_per_window]

            def error(x):
                return float(window[x]) - float(self.signal[last_fft_index * samples_step + x])

            if len(window) < self.samples_per_window:
                absolute_thresh = self.thresh * (approx_norm_squared(window) ** 0.5)
                last_fft = calculate_fft(window, absolute_thresh, self.sample_rate)
                last_fft_index = i
                res.append(last_fft)
                break

            norm = 0
            samples = random.sample(range(self.samples_per_window), min(samples_number, self.samples_per_window))
            for sample in samples:
                norm += error(sample) ** 2
            norm **= 1 / 2

            if norm > a:
                absolute_thresh = self.thresh * (approx_norm_squared(window) ** 0.5)
                last_fft = calculate_fft(window, absolute_thresh, self.sample_rate)
                last_fft_index = i
            res.append(last_fft)
        return (x for x in res)
