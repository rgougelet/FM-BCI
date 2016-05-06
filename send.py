import time
from pylsl import StreamInfo, StreamOutlet, vectorf
import oscillation as o
import processing as p
import numpy as np
<<<<<<< HEAD
import random
import matplotlib.pyplot as plt
import math
import scipy.signal
from scipy.signal import hilbert

for clearline in range(1,20):
    print('\n')
    
# frequency modulation parameters
alphaCenter = 10   # Hz the carrier frequency
alphaModFreq = 0.01  # Hz the modulating frequency
alphaFreqDev = 2    # Hz of the frequency deviation, BW is 2x this

# generate data to send
sampleRate = 1024.0
numOfChannel = 1
dataLengthSecs = 3000
dataLengthSamples = dataLengthSecs*sampleRate
voltageSamples = np.empty([numOfChannel,dataLengthSamples])
chanSNRs = np.linspace(1./numOfChannel,10,numOfChannel)
#np.random.shuffle(chanSNRs)
#print chanSNRs
#for channelIndex in range(numOfChannel):
#    voltageSamples[channelIndex,:] = o.chan_fm_noisy(dataLengthSamples, sampleRate, alphaCenter, alphaModFreq, alphaFreqDev, chanSNRs[channelIndex])
<<<<<<< HEAD
voltageSamples[-1,:] = o.chan_sin(dataLengthSamples, sampleRate, alphaCenter)
=======

voltageSamples[-1,:] = o.chan_sin_noisy(dataLengthSamples, sampleRate, alphaCenter)
print voltageSamples.shape
>>>>>>> e4f33c72087e7b09fecf43fef6ab883767cd4063
#voltageSamples = o.chan_sin(dataLengthSamples, sampleRate, alphaCenter) # ground truth
#voltageSamples = o.chan_fm(dataLengthSamples, sampleRate, alphaCenter, alphaModFreq, alphaFreqDev)
#voltageSamples = o.chan_fm_noisy(dataLengthSamples, sampleRate, alphaCenter, alphaModFreq, alphaFreqDev)
    # voltageSamples[channelIndex,:] = o.chan_sin(dataLengthSamples, sampleRate, 10, chanSNRs[channelIndex])
# voltageSamples[7,:] = o.chan_sin(dataLengthSamples, sampleRate, alphaCenter, alphaModFreq, alphaFreqDev) # ground truth
=======

for clearline in range(1,100):
    print('\n')
    
# frequency modulation parameters
alphaCenter = 10.25   # Hz the carrier frequency
alphaModFreq = 0.1  # Hz the modulating frequency
alphaFreqDev = 1    # Hz of the frequency deviation

# generate data to send
sampleRate = 1024.0
numOfChannel = 8
dataLengthSecs = 300
dataLengthSamples = dataLengthSecs*sampleRate
voltageSamples = np.empty([numOfChannel,dataLengthSamples])
for channelIndex in range(0,numOfChannel):
    voltageSamples[channelIndex,:] = o.fm_noisy(dataLengthSamples, sampleRate, alphaCenter, alphaModFreq, alphaFreqDev)
voltageSamples[channelIndex,:] = o.fm(dataLengthSamples, sampleRate, alphaCenter, alphaModFreq, alphaFreqDev) # ground truth
>>>>>>> e86d00ecee6bb251e52daf833525f0da615d2865

# create outlet for output
info = StreamInfo('SimulatedEEG', 'EEG', numOfChannel, sampleRate, 'float32', 'myuid34234')
outlet = StreamOutlet(info)
print("\n \nSending data...")

for sample in voltageSamples.T:
    outlet.push_sample(sample)
    # wait precisely between samples
    start = time.clock()
    now = time.clock()
    while now < start + 1/sampleRate:
        now = time.clock()
        pass