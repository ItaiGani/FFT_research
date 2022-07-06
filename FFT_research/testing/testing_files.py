import time
import os
import sys

from matplotlib import scale
sys.path.append("../FFT_research")
from FFT_research.plot import *
from FFT_research.fft_stream_interface import *

file = FFTHC(r'FFT_research\testing\audio_wav\(200, 4096), (300, 4096).wav', thresh=1)
g = file.calculate()
FFTHC.plot(g, title = "Mulim" ,scale = True)