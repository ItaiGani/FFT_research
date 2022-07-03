from scipy.io import wavfile

class FFTStream:
    def __init__(self, filename : str, mode : int = 0) -> None:
        """Constructor for the FFTStream class.

        Args:
            signal (list): The '.wav' file content.
            sr (int, optional): The sample rate of the signal. Defaults to 44100.
            mode (int, optional): The form of the hc algorithm. Defaults to 0.
        """
        self.sample_rate, self.signal = wavfile.read(filename)
        self.mode : int = mode


    def hc(self, thresh : float = 0):
        pass

    @staticmethod
    def rick(*args, **kwargs):
        import webbrowser
        webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
