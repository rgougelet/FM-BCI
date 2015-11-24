import pylab
import platform
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack
import random
import time
import math
import sys
sys.path.insert(0, './pylsl')
from pylsl import StreamInlet, resolve_stream, vectorf
import processing as p
import record


def output_to_file_before_exit():
    """  output alpha peak frequency to file on KeyBoardInterrupt """
    print 'Saved Data:'
    print peak_alpha_freqs
    recorder.record_raw(peak_alpha_freqs.transpose())


# first resolve an EEG stream on the lab network
print("looking for an EEG stream...")
streams = resolve_stream('name', 'SimulatedEEG')

# create a new inlet to read from the stream
inlet = StreamInlet(streams[0])

# Initialize the recorder 
recorder = record.Recorder()

# populate the array in real time
sampleRate = 1024. # make sure this matches the sampleRate in SendData.py
numOfChannel = 8
dataLengthSecs = 1
dataLengthSamples = dataLengthSecs * sampleRate
voltageSamples = np.empty([numOfChannel,dataLengthSamples])
sampleIndex = 0
sample = vectorf()

bandLow = 8                                # lower alpha band 
bandHigh = 12                              # higher alpha band
orderFilter = 4  

# peak_alpha_freq is a (numOfChannelss X numOfSamples) matrix , add 1 column of zero padding
peak_alpha_freqs = np.zeros([numOfChannel, 0])       

voltageBatch = np.empty([numOfChannel, 0])
samplesPerBatch = sampleRate * 4

# simulation offline eeg by populating the batch then input into spectral_averaging_batch
try:
    print("Collecting data in "+str(dataLengthSecs)+" second chunks.")
    while True:
        # get a new sample (you can also omit the timestamp part if you're not
        # interested in it)
        sample, timestamp = inlet.pull_sample()
        # populating the batch
        voltageBatch =  np.c_[voltageBatch, sample] 

        sampleIndex += 1

        if sampleIndex == samplesPerBatch:
            peak_alpha_freq = p.spectral_averaging_batch(voltageBatch, sampleRate, numOfChannel)
            # append outputColData as column to the peak_alpha_freq array
            peak_alpha_freqs = np.c_[peak_alpha_freqs, peak_alpha_freq] 
            # sampleIndex = 0

        # equivalent of Keyboard inturrpt on Windows
        if platform.system() == "Windows":
            import msvcrt
            if msvcrt.kbhit():
                if ord(msvcrt.getch()) == 'q':
                    # Write to file before exit
                    output_to_file_before_exit()
                    exit()



except KeyboardInterrupt:
    # Write to file before exit
    output_to_file_before_exit()
    raise

