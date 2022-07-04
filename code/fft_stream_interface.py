from main import main_fft

class FFTHC(main_fft):
    def __init__(self, filename: str, thresh: float = 0, win_size: float = 0.1, win_overlap: float = 0, mode: int = 0):
        """
        Args:
            filename (str): Path for '.wav' file to read.
            thresh (float, optional): The minimum amplitude of a coefficient that consider as heavy. Defaults to 0.
            win_size (int, optional): The size of a window (in seconds). Defaults to 1.
            win_overlap (int, optional): The percentage of the overlapping (between 0 to 1). Defaults to 0.
            mode (int, optional): The fft mode to run. Defaults to 0.
        """
        super()

    def calc(self) -> list(dict(float, float)):
        super()

    def plot(self):
        """
        plotting a time to frequency (log scale)
        """
        super()
