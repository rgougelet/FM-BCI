import random
import time
import math
import numpy as np
from pylsl import StreamInfo, StreamOutlet, vectorf

for clearline in range(1,100):
    print('\n')

sampleRate = 512.0
info = StreamInfo('SimulatedEEG', 'EEG', 8, sampleRate, 'float32', 'myuid34234')

numOfChannelss = 8
channelWeights = np.linspace(1./numOfChannelss,1,numOfChannelss) 
np.random.shuffle(channelWeights)
print 'Channel weights:', '\n'
for channel_index in range(numOfChannelss):

    print "        ", channel_index+1, "   ", channelWeights[channel_index]
alphaCenter = 10.   # Hz the carrier frequency
alphaModFreq = 0.1  # Hz the modulating frequency
alphaFreqDev = 1    # Hz of the frequency deviation

snr = 2             # signal / noise
noiseMean = 0
noiseStdDev = 0.5
alphaMean = 0
alphaStdDev = abs(np.sqrt(snr*(noiseStdDev**2))) # std of sine wave
alphaAmp = np.sqrt(2)*alphaStdDev
h = alphaFreqDev/alphaModFreq         # Modulation index

# next make an outlet
outlet = StreamOutlet(info)
previousRandSample = np.random.normal(noiseMean, noiseStdDev)   # initialize for 1/f noise 
sample = np.empty(numOfChannelss)           # create (blank) data array w/ entry for each channel

print("\n \nSending data...")

while True:

    # Constructs 1/f noise by iteratively adding normal random noise, effectively the CDF of normal dist.
    nextRandSample = previousRandSample + np.random.normal(noiseMean, noiseStdDev)
    
    # Frequency modulated alpha rhythm, a sinusoidal baseband signal
    alpha = alphaAmp*np.sin( alphaCenter  * 2.0 * np.pi * time.time() + \
    alphaFreqDev*np.sin(2 * np.pi * alphaModFreq * time.time()) / alphaModFreq)
    
    # assign the weighted alpha rhythm + 1/f noise + additional random noise to each channel in sample
    for channel_index in range(0,numOfChannelss):
        sample[channel_index] = channelWeights[channel_index]*alpha + nextRandSample + 0.05*np.random.random()    
    
    # push sample
    outlet.push_sample(sample)
    
    previousRandSample = nextRandSample 
    
    start = time.clock()
    now = time.clock()

    while now < start + 1/sampleRate:
        now = time.clock()
        pass
