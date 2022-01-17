import matplotlib.pyplot as plt
import numpy as np
from pyparsing import alphanums
from scipy.io import wavfile
from scipy.fft import rfft, rfftfreq
import math


print("started")
#constants
frequency_error = 12            #the size of the "buckets" of frequcnies
samples         = 100           #in the homework instructions, this is (T/W)
heavy_amplitude = 5*10**4       #what consideres as heavy coefficient
alpha           = 10**4           #how close the windows should be to considered as the same


fig, ax = plt.subplots()    #creating the graph
Ax = []                     #list of x-values in the graph, represnts the time 
By = []                     #iist of y-values in the graph, represtns the frequency
C = []                      #list of z-values in the graph, represnts the amplitude of specific frequency at specific time.
# notice that we have to save the next equality: len(Ax)=len(By)=len(C)
round_frequencies = [110*((2**(1/frequency_error))**i) for i in range(1, frequency_error*7 + 6)]        #list of the frequecnies's "buckets"
#print(round_frequencies)

fs_rate, signal = wavfile.read("audio_wav\pirates_of_the_caribbean_short_version.wav")              #imports the signal
print ("Frequency sampling", fs_rate)
l_audio = len(signal.shape)
print ("Channels", l_audio)
if l_audio == 2:        #if the audio has 2 channels, we take their avg.
    signal = signal.sum(axis=1) / 2
samples_lst = np.linspace(0, signal.shape[0], samples, dtype=int)       #dividing theortically the audio into "samples" parts
print(signal.shape[0])
#print(samples_lst)
for i in range(len(samples_lst)-1):
    signal_restricted = signal[samples_lst[i]:samples_lst[i+1]:]
    N = signal_restricted.shape[0]
    #print ("Complete Samplings N", N)
    secs = N / float(fs_rate)
    #print ("secs", secs)
    Ts = 1.0/fs_rate # sampling interval in time
    #print ("Timestep between samples Ts", Ts)
    FFT = np.abs(rfft(signal_restricted))               #computing FFT on the restricted signal
    freqs = rfftfreq(signal_restricted.size, Ts)        #notice that the amplitude of freqs[l] = FFT[l]
    By_i = [0 for i in range(len(round_frequencies))]
    C_i = [0 for i in range(len(round_frequencies))]
    for l, j in enumerate(FFT):
        if freqs[l] > round_frequencies[-1]:            #highest frequency
            By_i[-1] = round_frequencies[-1]
            C_i[-1] += j
            continue
        if freqs[l] <= 110:                             #lowest frequency
            By_i[0] = round_frequencies[0]
            C_i[0] += j
            continue
        left = 0                                        #the next few lines is to find the closest round frequcny using binary search
        right = len(round_frequencies)-2
        while left <= right:                        
            mid = (left + right)//2
            if round_frequencies[mid] <= freqs[l] <= round_frequencies[mid+1]:
                d = (freqs[l]-round_frequencies[mid]) > (round_frequencies[mid+1]-freqs[l])
                # if holds, d = True = 1 which means freqs[l] is closer to round_freqs[mid + 1]
                # otherwise d = False = 0 means freqs[l] is closer to round_freqs[mid]
                By_i[mid + d] = round_frequencies[mid+d]
                C_i[mid + d] += j
                break
            elif round_frequencies[mid+1] < freqs[l]:
                left = mid + 1
            else:
                right = mid-1
    
    heavy_By_i = []                                                                 
    heavy_C_i  = []
    for frequency, amplitude in zip(By_i, C_i):                                      #adding to heavy coefficients list the heavy ones.
        if amplitude > heavy_amplitude:
            heavy_By_i.append(math.log(frequency + 1,2))
            heavy_C_i.append(amplitude)
    Ax.extend([samples_lst[i]/fs_rate for j in range(len(heavy_C_i))])                    #adding the points to the graph, note: we could change it to len(heavy_By_i)
    By.extend(heavy_By_i)                                                           #to make the graph clearer, I'm showing only the high amplitude's frequencies
    C.extend(heavy_C_i)

sc = ax.scatter(Ax, By, c=C, s=12, edgecolor="none")                                 #plotting the graph
ax.set_ylabel('frequency (log base 2 scale)', loc='center')
ax.set_xlabel('time', loc='left')
ax.set_title("pirates of the caribbean")
cbar = fig.colorbar(sc)
cbar.set_label("Amplitude", loc='center')
plt.savefig("graphs/test.png")

print("ended")
