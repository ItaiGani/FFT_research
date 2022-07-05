import time
import sys
import os
from fft_stream_interface import FFTHC

file = FFTHC(r'C:\Users\yocha\OneDrive\Documents\Itai\FFT_research\audio_wav\(500, 8192).wav', thresh=1, win_size=3)
g = file.calculate()
FFTHC.plot(g)