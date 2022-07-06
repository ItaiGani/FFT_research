import time
import os
import sys
sys.path.append("../FFT_research")
from FFT_research.plot import *
from FFT_research.fft_stream_interface import *

file = FFTHC(r'FFT_research\testing\audio_wav\(500, 8192).wav', thresh=0.5)
g = file.calculate()
FFTHC.plot(g)