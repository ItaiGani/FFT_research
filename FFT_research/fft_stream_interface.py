from scipy.io import wavfile
import sys
import math
sys.path.append("../FFT_research")

from FFT_research.plot import plot_audio_graph
from FFT_research.calculate_hc_fft import calculate_fft, approx_norm_squared


class FFTHC:
    def __init__(self, filename: str, thresh: float = 0, win_size: float = 0.1, win_overlap: float = 0, mode: int = 0) -> None:
        """
        Args:
            filename (str): Path for '.wav' file to read.
            thresh (float, optional): The minimum amplitude of a coefficient that consider as heavy (in percentage). Defaults to 0.
            win_size (int, optional): The size of a window (in seconds). Defaults to 1.
            win_overlap (int, optional): The percentage of the overlapping (between 0 to 1). Defaults to 0.
            mode (int, optional): The fft mode to run. Defaults to 0.
        """
        self.sample_rate, self.signal = wavfile.read(filename)
        if hasattr(self.signal[0],'__len__') and len(self.signal[0]) > 1:
            raise NotImplementedError(f"More than 1 chanel in {filename}")

        self.thresh = thresh
        self.win_size = win_size
        self.win_overlap = win_overlap
        self.mode: int = mode

        self.samples_per_window = self.sample_rate * self.win_size


    def calculate(self):
        """Calculates the heavy coefficients over the file.

        Returns:
            generator of freq-amp dictionaries representing the windows.
        """
        overlapping_samples = self.samples_per_window * self.win_overlap
        samples_step = int(self.samples_per_window - overlapping_samples)
        number_of_wins = math.ceil((len(self.signal) - self.samples_per_window) / (self.samples_per_window - overlapping_samples)) + 1

        res = []
        for i in range(number_of_wins): 
            window = self.signal[i * samples_step : (i + 1) * samples_step]
            absolute_thresh = self.thresh * (approx_norm_squared(window) ** 0.5)
            f_hat = calculate_fft(window, absolute_thresh, self.sample_rate)
            res.append(f_hat)
        
        return (x for x in res)
        

    @staticmethod
    def rick(*args, **kwargs):
        import webbrowser
        webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    @staticmethod
    def plot(iter, title: str = "FFT", scale: bool = False):
        plot_audio_graph(iter, title, scale)
