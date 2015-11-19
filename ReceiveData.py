import pylab
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack
import random
import time
import math
import sys
sys.path.insert(0, './pylsl')
from pylsl import StreamInlet, resolve_stream, vectorf
import processPAF

# first resolve an EEG stream on the lab network
print("looking for an EEG stream...")
streams = resolve_stream('name', 'SimulatedEEG')

# create a new inlet to read from the stream
inlet = StreamInlet(streams[0])

# populate the array in real time
sampleRate = 1024. # make sure this matches the sampleRate in SendData.py
numOfChannels = 8
dataLengthSecs = 5

dataLengthSamples = dataLengthSecs*sampleRate
voltageSamples = np.empty([numOfChannels,dataLengthSamples])
sampleIndex = 0
sample = vectorf()

bandLow = 8                                # lower alpha band 
bandHigh = 12                              # higher alpha band
orderFilter = 4  

# PAF(numOfChannels, sampleRate, bandLow, bandHigh, orderFilter)
paf = processPAF.PAF(numOfChannels, sampleRate, bandLow, bandHigh, orderFilter)   

try:
    while True:
        # get a new sample (you can also omit the timestamp part if you're not
        # interested in it)
        sample, timestamp = inlet.pull_sample()
        
        # populating the samples
        voltageSamples[:, sampleIndex] = sample
        sampleIndex += 1

        if sampleIndex == dataLengthSamples:
            paf.process_PAF(voltageSamples)
            sampleIndex = 0

except KeyboardInterrupt:
    # Write to file before exit
    paf.output_to_file_before_exit()
    raise


