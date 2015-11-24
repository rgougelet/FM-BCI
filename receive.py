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

# initialize data stream
print("looking for an EEG stream...")
streams = resolve_stream('name', 'SimulatedEEG')
inlet = StreamInlet(streams[0])

# Extract stream info
inf = inlet.info()
print("The stream's XML meta-data is: ")
#print(inf.as_xml())
sampleRate = inf.desc().child_value("nominal_srate") # make sure this matches the sampleRate in SendData.py
print sampleRate
numOfChannel = inf.desc().child_value("channel_count")
sample = vectorf()

# Initialize the recorder 
recorder = record.Recorder()

# Processing parameters
chunkLengthSecs = 1
chunkLengthSamples = int(chunkLengthSecs * sampleRate)
bandLow = 8                                # lower alpha band 
bandHigh = 12                              # higher alpha band
orderFilter = 4
dataChunkSamples = np.empty([numOfChannel,chunkLengthSamples])

try:
    print("Collecting data in "+str(chunkLengthSecs)+" second chunks.")
    sampleIndex = 0
    peak_alpha_freqs = np.zeros([numOfChannel, 0]) # grows with every chunk and stores peaks for each channel
    while True:
    
        # populating the samples
        sample, timestamp = inlet.pull_sample()
        voltageSamples[:, sampleIndex] = sample
        sampleIndex += 1

        # process data chunk
        if sampleIndex == dataLengthSamples:
            voltageSamples = p.butter_bandpass_filter(voltageSamples,bandLow,bandHigh,orderFilter)
            peak_alpha_freq = p.spectral_averaging(voltageSamples, sampleRate)
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

