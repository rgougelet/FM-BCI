import platform
import numpy as np
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


print("Collecting data in "+str(dataLengthSecs)+" second chunks.")
sampleIndex = 0
peak_alpha_freqs = np.zeros([numOfChannel,0]) # grows with every chunk and stores peaks for each channel
while True:

    # populating the samples
    sample, timestamp = inlet.pull_sample()
    voltageSamples[:, sampleIndex] = sample   # number of channels by dataLengthSamples matrix
    sampleIndex += 1

    # process data chunk
    if sampleIndex == dataLengthSamples:
        voltageSamples = p.butter_bandpass_filter(voltageSamples,bandLow,bandHigh,sampleRate,orderFilter)
        medianSpectrumMat = p.spect_median(voltageSamples, sampleRate, desiredFreqResolution, winLengthSamples, overlapSamples)
        peak_alpha_freq = p.peak_freq(medianSpectrumMat, desiredFreqResolution)
        peak_alpha_freqs = np.c_[peak_alpha_freqs, peak_alpha_freq] # append to storage array

        print peak_alpha_freq
        recorder.write(peak_alpha_freq)
        sampleIndex = 0 # restart new chunk





