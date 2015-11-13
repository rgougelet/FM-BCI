"""Example program to show how to read a multi-channel time series from LSL."""
import pylab
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack
import random
import time
import math
import sys
sys.path.insert(0, './pylsl')
from pylsl import StreamInlet, resolve_stream
import processPAF

# first resolve an EEG stream on the lab network
print("looking for an EEG stream...")
streams = resolve_stream('type', 'EEG')

# create a new inlet to read from the stream
inlet = StreamInlet(streams[0])

# populate the array in real time
sampleRate = 512 # make sure this matches the sampleRate in SendData.py
numOfChannel = 8
dataLengthSecs = 10
dataLengthSamples = dataLengthSecs*sampleRate
voltageSamples = np.empty([numOfChannel,dataLengthSamples])
sampleIndex = 0

while True:
    # get a new sample (you can also omit the timestamp part if you're not
    # interested in it)
    sample, timestamp = inlet.pull_sample()
    
    # populating the samples
    voltageSamples[:, sampleIndex] = sample
    sampleIndex += 1

    if sampleIndex == dataLengthSamples:
        processPAF(voltageSamples,sampleRate)
        sampleIndex = 0



