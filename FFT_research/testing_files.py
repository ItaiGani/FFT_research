import time
import sys
import os
from fft_stream_interface import FFTHC

file = FFTHC(r'C:\Users\yocha\OneDrive\Documents\Itai\FFT_research\audio_wav\(500, 8192).wav')
g = file.calculate()
for d in g:
    print(d)