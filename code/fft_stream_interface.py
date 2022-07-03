from analyzing import guesser2_overlapping_windows


class FFTStream:
    def __init__(self, signal : list(int), sr: int = 44100, mode : int = 0) -> None:
        """Constructor for the FFTStream class.

        Args:
            signal (list): The '.wav' file content.
            sr (int, optional): The sample rate of the signal. Defaults to 44100.
            mode (int, optional): The form of the hc algorithm. Defaults to 0.
        """
        self.signal : list(int) = signal
        self.sample_rate : int = sr
        self.mode : int = mode


    def hc(self, thresh : float = 0):
        return guesser2_overlapping_windows(self.signal, self.sample_rate, 1000, 4, 11, 19.2, 1, 10000, True)

    @staticmethod
    def rick(*args, **kwargs):
        import webbrowser
        webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")


if __name__ == '__main__':
    FFTStream("../audio_wav/piano.wav")