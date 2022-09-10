import os
import sys
import time
import matplotlib.pyplot as plt
import numpy as np

sys.path.append("../FFT_research")
from FFT_research.testing.overlapping_windows import Overlapping_Windows
from FFT_research.fft_stream_interface import FFTHC


def plotting(file_path, threshold=0):
    file = FFTHC(file_path, thresh=threshold)
    g = file.calculate()
    FFTHC.plot(g)


def get_wav_files():
    directory = 'FFT_research/testing/audio_wav/'
    files = os.listdir(directory)

    for i in range(len(files)):
        files[i] = os.path.abspath(directory + files[i])

    return files


WAV_FILES = get_wav_files()


def time_function(window_size, window_overlap, loop=3, stop_after=100):
    total_time = 0

    for filename in WAV_FILES:
        try:
            g = Overlapping_Windows(filename=filename, thresh=0.1, win_size=window_size, win_overlap=window_overlap)
        except NotImplementedError:
            # print(f'\'{filename.split("/")[-1]}\' was not read.')
            continue

        for _ in range(loop):
            t1 = time.perf_counter()
            g.calculate(a=100000)
            t2 = time.perf_counter()
            total_time += t2 - t1
            
            if total_time > stop_after:
                return float('inf')


    return total_time / loop


def find_best_win_overlap(win_size, step=0.01):
    best_win_overlap = 0
    best_time = float('inf')
    for i in range(int(1 / step)):
        overlap = i * step
        calculation_time = time_function(win_size, overlap, stop_after=best_time + 1)
        if calculation_time < best_time:
            best_time = calculation_time
            best_win_overlap = overlap
    return best_win_overlap

def find_best_win_size(win_overlap, step=0.01, max_win_size = 1):
    best_win_size = 0
    best_time = float('inf')
    for i in range(int(max_win_size / step)):
        win_size = (i + 1) * step
        calculation_time = time_function(win_size, win_overlap, best_time + 1)
        if calculation_time < best_time:
            best_time = calculation_time
            best_win_size = win_size
    return best_win_size


def find_best_parameters(size_step, overlap_step, max_win_size=1, loop=3, plot=False):
    best_win_size = 0
    best_overlap = 0

    times = []

    best_time = float('inf')
    for i in range(int(max_win_size / size_step)):
        if plot:
            times.append([])
        win_size = (i + 1) * size_step
        
        for j in range(int(1 / overlap_step)):
            overlap = j * overlap_step

            calculation_time = time_function(win_size, overlap, loop=loop, stop_after=best_time + 1)
            if calculation_time < best_time:
                best_win_size = win_size
                best_overlap = overlap
                best_time = calculation_time
            if plot:
                times[-1].append(calculation_time)
            
            print(f'{win_size = }, {overlap = }')
    
    if plot:
        x = np.arange(0, 1, overlap_step)  # overlap axis
        y = np.arange(0, max_win_size, size_step)  # step axis

        x_center = 0.5 * (x[:-1] + x[1:])
        y_center = 0.5 * (y[:-1] + y[1:])

        X, Y = np.meshgrid(x_center, y_center)
        Z = np.array(times).T

        p = plt.pcolormesh(x, y, X, cmap='turbo', shading='flat')
        # cset =  plt.contour(X, Y, Z, cmap='gray')
        plt.colorbar(p)
        plt.savefig('FFT_research/testing/graph.png')


    return best_win_size, best_overlap


if __name__ == '__main__':
    best_win_size, best_overlap = find_best_parameters(0.4, 0.1, 4, plot=True)
    print(f'{best_win_size = }, {best_overlap = }')
