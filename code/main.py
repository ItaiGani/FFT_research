from scipy.io import wavfile
import math
from plot import plot_audio_graph
from calc_hc import calc_fft


class main_fft:
    def __init__(self, filename: str, thresh: float = 0, win_size: float = 0.1, win_overlap: float = 0, mode: int = 0) -> None:
        self.sample_rate, self.signal = wavfile.read(filename)
        self.thresh = thresh
        self.win_size = win_size
        self.win_overlap = win_overlap
        self.mode: int = mode

        self.samples_per_window = self.sample_rate * self.win_size

    def calc(self):
        overlapping_samples = self.samples_per_window * self.win_overlap
        samples_step = int(self.samples_per_window - overlapping_samples)
        number_of_wins = math.ceil(
            (len(self.signal) - self.samples_per_window) / (self.samples_per_window - overlapping_samples)) + 1

        res = []
        for i in range(number_of_wins):
            f_hat = calc_fft(self.signal[i * samples_step: (i + 1) * samples_step], self.thresh, self.sample_rate)
            res.append(f_hat)
        return res

    @staticmethod
    def rick(*args, **kwargs):
        import webbrowser
        webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    def plot(self):
        plot_audio_graph(self.sample_rate, self.signal, self.window_size)
