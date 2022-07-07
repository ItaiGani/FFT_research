import random

import numpy as np
from scipy.io.wavfile import write

samplerate = 44100
time = 3
num_of_frequencies = 1
fsList = []
fsList.extend([(random.randint(200, 4000), random.randint(2 ** 10, 2 ** 14)) for i in range(num_of_frequencies)])

t = np.linspace(0, time, time * samplerate)
data = np.array([np.zeros(time * samplerate)])
for frequency, amplitude in fsList:
    data = data + np.multiply(amplitude * np.sin(2 * np.pi * frequency * t),
                              np.random.normal(1, 0.7, time * samplerate))

# name = str(fsList)[1:-1] + ".wav"
name = "gaussian1.wav"
write(name, samplerate, data.astype(np.int16).T)
