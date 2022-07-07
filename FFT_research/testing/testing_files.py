import time
import os
import sys

from matplotlib import scale

sys.path.append("../FFT_research")
from FFT_research.testing.overlapping_windows import Overlapping_Windows
from FFT_research.fft_stream_interface import FFTHC


def plotting(file_path, threshold = 0):
    file = FFTHC(file_path, thresh = threshold)
    g = file.calculate()
    FFTHC.plot(g)

def get_wav_files():
    directory = 'FFT_research/testing/audio_wav/'
    files = os.listdir(directory)

    for i in range(len(files)):
        files[i] = os.path.abspath(directory + files[i])

    return files

WAV_FILES = get_wav_files()

def time_function(window_size, window_overlap, loop=3):
    total_time_no_overlap = 0
    total_time_with_overlap = 0

    for filename in WAV_FILES:
        try:
            f = FFTHC(filename=filename, thresh=0, win_size=window_size, win_overlap=window_overlap)
            g = Overlapping_Windows(filename=filename, thresh=0, win_size=window_size, win_overlap=window_overlap)
        except NotImplementedError:
            # print(f'\'{filename.split("/")[-1]}\' was not read.')
            continue
        
        for _ in range(loop):
            t1 = time.perf_counter()
            f.calculate()
            t2 = time.perf_counter()
            total_time_no_overlap += t2 - t1

            t1 = time.perf_counter()
            g.calculate(a=100000)
            t2 = time.perf_counter()
            total_time_with_overlap += t2 - t1

    
    return total_time_no_overlap / loop, total_time_with_overlap / loop


if __name__ == '__main__':
    for i in range(11):
        times = time_function(0.1, 0.1*i)
        print(f'overlap percentage: {0.1*i}\n\twithout overlapping: {times[0]}\n\twith overlapping: {times[1]}')
