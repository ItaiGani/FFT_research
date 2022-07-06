import time
import os
import sys
sys.path.append("../FFT_research")
from FFT_research.fft_stream_interface import FFTHC


def get_wav_files():
    directory = 'FFT_research/testing/audio_wav/'
    files = os.listdir(directory)

    for i in range(len(files)):
        files[i] = os.path.abspath(directory + files[i])

    return files

WAV_FILES = get_wav_files()
# print(WAV_FILES)


def time_function(window_size, window_overlap, loop=3):
    total_time = 0

    for filename in WAV_FILES:
        try:
            f = FFTHC(filename=filename, thresh=0, win_size=window_size, win_overlap=window_overlap)
        except NotImplementedError:
            print(f'\'{filename.split("/")[-1]}\' was not read.')
            continue
        
        for _ in range(loop):
            t1 = time.perf_counter()
            f.calculate()
            
            t2 = time.perf_counter()
            total_time += t2 - t1
    
    return total_time / loop
