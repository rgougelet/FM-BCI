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

print("Collecting data in "+str(dataLengthSecs)+" second chunks.")
sampleIndex = 0
chunkChanPeaks = np.zeros([numOfChannel,0])
chunkChanAmps = np.zeros([numOfChannel,0]) 
chunkChanRatios = np.zeros([numOfChannel,0])
while True:

    # populating the samples
    sample, timestamp = inlet.pull_sample()
    voltageSamples[:, sampleIndex] = sample
    sampleIndex += 1

    # process data chunk
    if sampleIndex == dataLengthSamples:
        voltageSamples = p.butter_bandpass_filter(voltageSamples,bandLow,bandHigh,sampleRate,orderFilter)
        chanPeaks = np.empty([numOfChannel,])
        chanAmps = np.empty([numOfChannel,])
        for channelIndex in range(numOfChannel):
            meanSpectrum = p.chan_welch(voltageSamples[channelIndex,:], sampleRate, desiredFreqResolution, winLengthSamples,overlapSamples)
            chanRatio = p.band_amp_ratio(meanSpectrum, desiredFreqResolution,bandLow,bandHigh)
            chanPeak,chanPeakIndex = p.chan_peak_freq(meanSpectrum, desiredFreqResolution)
            
            chanRatios[channelIndex] = chanRatio
            chanPeaks[channelIndex] = chanPeak
            chanAmps[channelIndex] = meanSpectrum[chanPeakIndex]
            
            chunkChanPeaks = np.c_[chunkChanPeaks, chanPeaks] # append to storage array
            chunkChanAmps = np.c_[chunkChanAmps, chanAmps]
            chunkChanRatios = np.c_[chunkChanRatios, chanRatios]
        print chanRatios
        output[:] = np.mean(chanPeaks)
        output = (12.-output)/4
        output = (1 if (output > 1) else output)
        print("Peak Freq: "+str(chanPeaks))
        #print("Peak Amps: "+str(chanAmps))
        print("Index:  "+str(output))
        print('\n \n')
        outlet.push_sample(output)
        sampleIndex = 0 # restart new chunk