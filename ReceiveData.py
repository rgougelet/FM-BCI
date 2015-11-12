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
from PFA import processingPAF

# first resolve an EEG stream on the lab network
print("looking for an EEG stream...")
streams = resolve_stream('type', 'EEG')

# create a new inlet to read from the stream
inlet = StreamInlet(streams[0])

# the populating the array in real time
numOfSamplesPerSecond = 256
numOfChannel = 8
voltageSamples = np.empty([numOfChannel,numOfSamplesPerSecond])
sampleIndex = 0


while True:
    # get a new sample (you can also omit the timestamp part if you're not
    # interested in it)
    sample, timestamp = inlet.pull_sample()

    # populating the samples
    voltageSamples[:, sampleIndex] = sample
    sampleIndex += 1

    if sampleIndex == 256:
        processingPAF(voltageSamples, timestamp)
        # sampleIndex = 0

    # print voltageSamples
    # print len(voltageSamples)
    # print(timestamp, samples.shape)



