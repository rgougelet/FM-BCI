import platform
import numpy as np
import sys
from pylsl import StreamInlet, resolve_stream, vectorf, StreamInfo, StreamOutlet
import processing as p
import record

for clearline in range(1,100):
    print('\n')

# initialize data stream
print("Looking for an EEG stream...")
streams = []
while not streams:
    streams = resolve_stream('name', 'SimulatedEEG')
inlet = StreamInlet(streams[0])

# Extract stream info
inf = inlet.info()
sampleRate = inf.nominal_srate()
numOfChannel = inf.channel_count()
#sample = pylsl.vectorf()

# Initialize the recorder 
recorder = record.Recorder()
recorder.filename_suffix = "Frequencies"

# Processing parameters
dataLengthSecs = 1
dataLengthSamples = int(dataLengthSecs * sampleRate)
bandLow = 8                                # lower alpha band 
bandHigh = 12                              # higher alpha band
orderFilter = 4
voltageSamples = np.empty([numOfChannel,dataLengthSamples])
desiredFreqResolution = 0.01
winLengthSamples = 512
overlapSamples = 256

info = StreamInfo('BCI_Stream', 'EEG', 1, dataLengthSecs, 'float32', 'myuid34234')
outlet = StreamOutlet(info)
output = np.empty(1)
print("\n \nSending BCI data...")

print("Collecting data in "+str(dataLengthSecs)+" second stores.")
sampleIndex = 0
storeChanPeakFreqs = np.zeros([numOfChannel,0])
storeChanPeakAmps = np.zeros([numOfChannel,0]) 
storeChanRatios = np.zeros([numOfChannel,0])
while True:

    # populating the samples
    sample, timestamp = inlet.pull_sample()
    voltageSamples[:, sampleIndex] = sample
    sampleIndex += 1

    # process data store
    if sampleIndex == dataLengthSamples:
        voltageSamples = p.butter_bandpass_filter(voltageSamples,bandLow,bandHigh,sampleRate,orderFilter)
        chanPeakFreqs = np.empty([numOfChannel,])
        chanPeakAmps = np.empty([numOfChannel,])
        chanRatios = np.empty([numOfChannel])
        for channelIndex in range(numOfChannel):
            meanSpectrum = p.chan_welch(voltageSamples[channelIndex,:], sampleRate, desiredFreqResolution, winLengthSamples,overlapSamples)
            chanRatio = p.chan_amp_ratio(meanSpectrum, desiredFreqResolution,bandLow,bandHigh)
            chanPeak,chanPeakIndex = p.chan_peak_freq(meanSpectrum, desiredFreqResolution)
            
            chanRatios[channelIndex] = chanRatio
            chanPeakFreqs[channelIndex] = chanPeak
            chanPeakAmps[channelIndex] = meanSpectrum[chanPeakIndex]
            
            storeChanPeakFreqs = np.c_[storeChanPeakFreqs, chanPeakFreqs] # append to storage array
            storeChanPeakAmps = np.c_[storeChanPeakAmps, chanPeakAmps]
            storeChanRatios = np.c_[storeChanRatios, chanRatios]
        print "Channel "+str(np.argmax(chanRatios)+1)+" has the highest alpha amp"
        print chanRatios
        print("Peak Freq: "+str(chanPeakFreqs))

        # Compute input into interface
        #output[:] = np.mean(ChanPeakFreqs)
        output[:] = chanPeakFreqs[np.argmax(chanRatios)]
        output = (12.-output)/4
        output = (1 if (output > 1) else output)
        output = (0 if (output < 0) else output)
        outlet.push_sample(output)
        print("Index:  "+str(output))
        print('\n \n')
        
        sampleIndex = 0 # restart new store