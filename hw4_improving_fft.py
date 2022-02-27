import matplotlib.pyplot as plt
import numpy as np
from pyparsing import alphanums
from scipy.io import wavfile
from scipy.fft import rfft, rfftfreq
import math
import time


print("##################### started #####################")
t0 = time.perf_counter()                                                                            #just for me to see the times

#printing some useful info about the signal
fs_rate, signal = wavfile.read("./piano.wav")              #imports the signal
signal = signal/(2**15)                                            #normalizing the audio
signal = signal[:fs_rate*10:]                                      #taking the first 10 seconds
print ("Frequency sampling", fs_rate)
l_audio = len(signal.shape)
print ("Channels", l_audio)
if l_audio == 2:        #if the audio has 2 channels, we take their avg.
    signal = signal.sum(axis=1) / 2

#variables and constants
Ts = 1.0/fs_rate                                                        # sampling interval in time
frequency_error = 12                                                    #the size of the "buckets" of frequcnies
samples         = 50*signal.shape[0]//fs_rate                           #in the homework instructions, this is (T/W)
heavy_amplitude = None                                                  #what considers as heavy coefficient
alpha           = math.sqrt(((1400/2**15)**2)*signal.shape[0]/samples)  #how close the windows should be to considered as the same, I calculated this as sqrt((avg_distance**2)*signal.shape[0]/samples)
counter_successed_guesses = 0                                           #used in the guesser's algorithms    
filter_coefficient = 0.15                                               #plotting the points such their amplitude is higher than filter*max(amplitudes) 

#functions
def calculate_reduced_signal(signal, samples, i, j):
    """gets signal and samples lst and two indices, return the reduced i-th signal by j, it means that we should already have the FFT of part j and we want b_i - b_j
    usually, we would want signal will contain the audio and samples contain the samples_lst"""
    assert i,j < len(samples)-1                                                                         #assuring the indices in the range
    d = min(samples[i+1]-samples[i], samples[j+1]-samples[j])
    reduced_i_signal = signal[samples[i]:samples[i]+d] - signal[samples[j]:samples[j]+d]                #numpy subtraction
    return reduced_i_signal

def norm_values(lst):
    return math.sqrt(np.sum(np.square(lst)))                                                            #numpy rules


#helpful lists
round_frequencies = np.array([22.5*((2**(1/frequency_error))**i) for i in range(1, frequency_error*10+1)])          #list of the frequecnies's "buckets"
samples_lst = np.linspace(0, signal.shape[0], samples, dtype=int)                                                   #dividing theortically the audio into "samples" parts
samples_check_list = np.full(len(samples_lst)-1 ,False)                                                         #saves which parts of the graph we already guessed and which not
padding = int((samples_lst[1] - samples_lst[0]) * 0.75) # to compute with overlapping windows we take additional padding entries before and after the window

fig, ax = plt.subplots()    #creating the graph
def vfft():
    global counter_successed_guesses
    #global padding
    Ax = []                     #list of x-values in the graph, represnts the time 
    By = []                     #iist of y-values in the graph, represtns the frequency
    C = []                      #list of z-values in the graph, represnts the amplitude of specific frequency at specific time.
    # notice that we have to save the next equality: len(Ax)=len(By)=len(C)
    for i in range(len(samples_lst)-1):
        if samples_check_list[i] == True:
            continue
        lim_down, lim_up = max(0, samples_lst[i] - padding), min(len(signal) - 2, samples_lst[i+2] + padding) # compute window limits to not exceed the signal range
        signal_restricted = signal[lim_down:lim_up:]
        FFT = np.abs(rfft(signal_restricted))               #computing FFT on the restricted signal
        freqs = rfftfreq(signal_restricted.size, Ts)        #notice that the amplitude of freqs[l] = FFT[l]
        By_i = [0 for _ in range(len(round_frequencies))]
        C_i = [0 for _ in range(len(round_frequencies))]
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
        
        Ax.extend([samples_lst[i]/fs_rate for j in range(len(C_i))])                    #adding the points to the graph, note: we could change it to len(By_i)
        By.extend(By_i)                                                                 #to make the graph clearer, I'm showing only the high amplitude's frequencies
        C.extend(C_i)
        samples_check_list[i] = True
        for l in range(i+1, len(samples_lst)-1):
            if samples_check_list[l] == True:
                continue
            reduced_l = calculate_reduced_signal(signal, samples_lst, l, i)
            if norm_values(reduced_l) <= alpha:
                counter_successed_guesses += 1
                Ax.extend([samples_lst[l]/fs_rate for j in range(len(C_i))])              #adding the points to the graph, note the change in Ax, as the time now is on the samples_lst[l]
                By.extend(By_i)                                                           #to make the graph clearer, I'm showing only the high amplitude's frequencies
                C.extend(C_i)
                samples_check_list[l] = True

    if False in samples_check_list:                             
        print("Error, there is uncalculated segment")                                           #should not get here


    highest_amplitude_filter = filter_coefficient*max(C)                                        #removing all the points that their ampiltudes are too low
    Ax = [Ax[i] for i in range(len(C)) if C[i] >= highest_amplitude_filter]                     
    By = [math.log(By[i] + 1, 2) for i in range(len(C)) if C[i] >= highest_amplitude_filter]
    C  = [C[i] for i in range(len(C)) if C[i] >= highest_amplitude_filter]

    return Ax, By, C

Ax, By, C = vfft()


sc = ax.scatter(Ax, By, c=C, s=15, edgecolor="none")                                        #plotting the graph
ax.set_ylabel('frequency (log base 2 scale)', loc='center')
ax.set_xlabel('time', loc='left')
ax.set_title("pirates of the caribbean")
cbar = fig.colorbar(sc)
cbar.set_label("Amplitude", loc='center')
# plt.savefig("graphs/test.png")
plt.show()


print("successed guesses = " + str(counter_successed_guesses))
t1 = time.perf_counter()
print("total time for analyzing " + str(t1-t0) + " seconds")
print("##################### ended #####################")
