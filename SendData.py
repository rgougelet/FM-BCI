import random
import time
import math
import numpy as np
from pylsl import StreamInfo, StreamOutlet, vectorf

for clearline in range(1,100):
    print('\n')

# data stream initiliazation
sampleRate = 1024.0
info = StreamInfo('SimulatedEEG', 'EEG', 8, sampleRate, 'float32', 'myuid34234')

# append some meta-data
info.desc().append_child_value("manufacturer", "BrainProducts")
channels = info.desc().append_child("channels")
for c in ["C3", "C4", "Cz", "FPz", "POz", "CPz", "O1", "O2"]:
    channels.append_child("channel")\
        .append_child_value("name", c)\
        .append_child_value("unit", "microvolts")\
        .append_child_value("type", "EEG")
        
# channel weighting
numOfChannel = 8
channelWeights = np.linspace(1./numOfChannel,1,numOfChannel) 
#np.random.shuffle(channelWeights)
print 'Channel weights:', '\n'
for channelIndex in range(numOfChannel):
    print "        ", channelIndex+1, "   ", channelWeights[channelIndex]
    
# frequency modulation parameters
alphaCenter = 10.25   # Hz the carrier frequency
alphaModFreq = 0.1  # Hz the modulating frequency
alphaFreqDev = 1    # Hz of the frequency deviation

# signal to noise parameters
snr = 2             # signal / noise
noiseMean = 0
noiseStdDev = 0.5
alphaMean = 0
alphaStdDev = abs(np.sqrt(snr*(noiseStdDev**2))) # std of sine wave
alphaAmp = np.sqrt(2)*alphaStdDev
h = alphaFreqDev/alphaModFreq         # Modulation index

# create outlet for output
outlet = StreamOutlet(info)
previousRandSample = np.random.normal(noiseMean, noiseStdDev)   # initialize for 1/f noise 
sample = np.empty(numOfChannel)           # create (blank) data array w/ entry for each channel
print("\n \nSending data...")

while True:
    # Constructs 1/f noise by iteratively adding normal random noise, effectively the CDF of normal dist.
    nextRandSample = previousRandSample + np.random.normal(noiseMean, noiseStdDev)
    previousRandSample = nextRandSample
    
    # Frequency modulated alpha rhythm, a sinusoidal baseband signal
    alpha = alphaAmp*np.sin( alphaCenter  * 2.0 * np.pi * time.time() + \
    alphaFreqDev*np.sin(2 * np.pi * alphaModFreq * time.time()) / alphaModFreq)
    
    # assign the weighted alpha rhythm + 1/f noise + additional random noise to each channel in sample
    for channelIndex in range(0,numOfChannel):
        sample[channelIndex] = channelWeights[channelIndex]*alpha + nextRandSample + 0.05*np.random.random()    
    sample[channelIndex] = alpha # change last channel to ground truth alpha
    
    # push sample
    outlet.push_sample(sample)

    # wait precisely between samples
    start = time.clock()
    now = time.clock()

    while now < start + 1/sampleRate:
        now = time.clock()
        pass
