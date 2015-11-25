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

for clearline in range(1,100):
    print('\n')

# initialize data stream
print("looking for an EEG stream...")
streams = resolve_stream('name', 'SimulatedEEG')
inlet = StreamInlet(streams[0])

# Extract stream info
inf = inlet.info()
sampleRate = inf.nominal_srate()
numOfChannel = inf.channel_count()
sample = vectorf()

# Initialize the recorder 
recorder = record.Recorder()

# Processing parameters
dataLengthSecs = 1
dataLengthSamples = int(dataLengthSecs * sampleRate)
bandLow = 8                                # lower alpha band 
bandHigh = 12                              # higher alpha band
orderFilter = 4
voltageSamples = np.empty([numOfChannel,dataLengthSamples])
desiredFreqResolution = 0.1
winLengthSamples = 512
overlapSamples = 256

try:
    print("Collecting data in "+str(dataLengthSecs)+" second chunks.")
    sampleIndex = 0
    peak_alpha_freqs = np.zeros([numOfChannel,0]) # grows with every chunk and stores peaks for each channel
    while True:
    
        # populating the samples
        sample, timestamp = inlet.pull_sample()
        voltageSamples[:, sampleIndex] = sample
        sampleIndex += 1

        # process data chunk
        if sampleIndex == dataLengthSamples:
            voltageSamples = p.butter_bandpass_filter(voltageSamples,bandLow,bandHigh,sampleRate,orderFilter)
            peak_alpha_freq = np.empty([numOfChannel,])
            print np.shape(peak_alpha_freq)
            for channelIndex in range(numOfChannel):
                medianSpectrum = p.chan_spect_median(voltageSamples[channelIndex,:], sampleRate, desiredFreqResolution, winLengthSamples, overlapSamples)
                medianPeak = p.chan_peak_freq(medianSpectrum, desiredFreqResolution)

                peak_alpha_freq[channelIndex] = medianPeak
                peak_alpha_freqs = np.c_[peak_alpha_freqs, peak_alpha_freq] # append to storage array
            sampleIndex = 0 # restart new chunk

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
    print 'Saved Data:'
    print peak_alpha_freqs
    recorder.record_raw(peak_alpha_freqs.transpose())
    raise

