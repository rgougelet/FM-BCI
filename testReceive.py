import numpy as np
from pylsl import StreamInlet, resolve_stream, vectorf, StreamInfo, StreamOutlet
import processing as p
import oscillation as o

import record
# from scikits.talkbox import lpc
from scipy import signal
from time import time
import sys
import matplotlib.pyplot as plt


for clearline in range(1,20):
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
record.delete_recordings() # delte recordings
recordFreq = record.Recorder("_Frequency")
recordFreq.write("       mean             median       meanBenchMark    medianBenchMark ")
recordAmp = record.Recorder("_Amplitude")
recordRatio = record.Recorder("_Ratio")
recordIndex = record.Recorder("_Index")

# Processing parameters
dataLengthSecs = 1
dataLengthSamples = int(dataLengthSecs * sampleRate)
bandLow = 8                                # lower alpha band 
bandHigh = 12                             # higher alpha band
orderFilter = 4
voltageSamples = np.empty([numOfChannel,dataLengthSamples])
# voltageSamples[-1,:] = o.chan_sin_noisy(dataLengthSamples, sampleRate, alphaCenter)
desiredFreqResolution = 0.01
winLengthSamples = 512
overlapSamples = 256

info = StreamInfo('BCI_Stream', 'EEG', numOfChannel, dataLengthSecs, 'float32', 'myuid34234')
outlet = StreamOutlet(info)
output = np.empty(1)
print("\n \nSending BCI data...")

print("Collecting data in "+str(dataLengthSecs)+" second stores.")
sampleIndex = 0
storeChanPeakFreqs = np.zeros([numOfChannel,0])
# storeChanPeakAmps = np.zeros([numOfChannel,0]) 
# storeChanRatios = np.zeros([numOfChannel,0])

# Comparisons of the mean and median spectrum and bench marking
meanSpectrumStoreChanPeakFreqs = np.zeros([numOfChannel,0])
meanBenchMark = np.zeros([numOfChannel,0])
medianSpectrumStoreChanPeakFreqs = np.zeros([numOfChannel,0])
medianBenchMark = np.zeros([numOfChannel,0])

start_time = time()
elapsed_time = 0
end_time =  60.0 if len(sys.argv) == 1 else float(sys.argv[1])

while True:
    # break out and save the mean and the medians 
    if elapsed_time > end_time:
        recordFreq.write("\n\n\n")
        recordFreq.write("Average:\n       mean             median       meanBenchMark    medianBenchMark")
        meanChanComparison = np.empty([4,]) 
        meanChanComparison[0] = np.mean(meanSpectrumStoreChanPeakFreqs)
        meanChanComparison[1] = np.mean(medianSpectrumStoreChanPeakFreqs)
        meanChanComparison[2] = np.mean(meanBenchMark)
        meanChanComparison[3] = np.mean(medianBenchMark)
        recordFreq.write(meanChanComparison)
        print "mean: ", np.mean(meanSpectrumStoreChanPeakFreqs), "    ", "median: ", np.mean(medianSpectrumStoreChanPeakFreqs), "    ", "meanBenchMark: ", np.mean(meanBenchMark), "    ", "medianBenchMark: ", np.mean(medianBenchMark)
        break

    # populating the samples
    sample, timestamp = inlet.pull_sample()
    voltageSamples[:, sampleIndex] = sample
    sampleIndex += 1
    # process data store
    if sampleIndex == dataLengthSamples:
        print "\nBatch collected at ", time()-start_time, " second"

        meanChanPeakFreqs = np.empty([numOfChannel,])
        medianChanPeakFreqs = np.empty([numOfChannel,])
        # chanPeakAmps = np.empty([numOfChannel,])
        # chanRatios = np.empty([numOfChannel])
        voltageSamples = p.butter_bandpass_filter(voltageSamples,bandLow,bandHigh,sampleRate,orderFilter)
            
        for channelIndex in range(numOfChannel):
            print "Channel ", channelIndex+1

            # Get mean and median spectrum and their time
            t0 = time()
            meanSpectrum = p.chan_welch(voltageSamples[channelIndex,:], sampleRate, desiredFreqResolution, winLengthSamples,overlapSamples)
            tMean = time() - t0
            meanBenchMark = np.c_[meanBenchMark, tMean]

            t0 = time()
            medianSpectrum = p.chan_spect_median(voltageSamples[channelIndex,:], sampleRate, desiredFreqResolution, winLengthSamples, overlapSamples)
            tMeidan = time() - t0
            medianBenchMark = np.c_[medianBenchMark, tMeidan]

            # Find peak then record it
            meanChanPeak,meanChanPeakIndex = p.chan_peak_freq(meanSpectrum, desiredFreqResolution)
            meanChanPeakFreqs[channelIndex] = meanChanPeak
            meanSpectrumStoreChanPeakFreqs = np.c_[meanSpectrumStoreChanPeakFreqs, meanChanPeakFreqs] 


            medianChanPeak,medianChanPeakIndex = p.chan_peak_freq(medianSpectrum, desiredFreqResolution)
            medianChanPeakFreqs[channelIndex] = medianChanPeak
            medianSpectrumStoreChanPeakFreqs = np.c_[medianSpectrumStoreChanPeakFreqs, medianChanPeakFreqs] 

            print "mean: ", meanChanPeak, "    ", "median: ", medianChanPeak, "    ", "meanBenchMark: ", tMean, "    ", "medianBenchMark: ", tMeidan
            # chanComparison = [mean, median, meanTime, medianTime]
            chanComparison = np.empty([4,]) 
            chanComparison[0] = meanChanPeak
            chanComparison[1] = medianChanPeak
            chanComparison[2] = tMean
            chanComparison[3] = tMeidan
            recordFreq.write(chanComparison)


            # chanRatio = p.chan_amp_ratio(meanSpectrum, desiredFreqResolution,bandLow,bandHigh)
            # chanPeak,chanPeakIndex = p.chan_peak_freq(meanSpectrum, desiredFreqResolution)
            
            # chanPeakFreqs[channelIndex] = chanPeak
            # chanPeakAmps[channelIndex] = meanSpectrum[chanPeakIndex]
            # chanRatios[channelIndex] = chanRatio

            # storeChanPeakFreqs = np.c_[storeChanPeakFreqs, chanPeakFreqs] # append to storage array
            # storeChanPeakAmps = np.c_[storeChanPeakAmps, chanPeakAmps]
            # storeChanRatios = np.c_[storeChanRatios, chanRatios]
        
        # maxChannelIndex = np.argmax(chanRatios)
        # print "Channel "+str(np.argmax(chanRatios)+1)+" has the highest alpha amp"
        # print chanRatios
        # print("Peak Freq: "+str(chanPeakFreqs[maxChannelIndex]))

        # Compute input into interface
        #output[:] = np.mean(ChanPeakFreqs)
        # output[:] = chanPeakFreqs[maxChannelIndex]
        # output = -((12.-output)/4)+1
        # output = (1 if (output > 1) else output)
        # output = (0 if (output < 0) else output)
        # outlet.push_sample(output)
        # print("Index:  "+str(output))
        # print('\n \n')

        # Record to file
        # recordFreq.write(storeChanPeakFreqs)
        # recordAmp.write(storeChanPeakAmps)
        # recordRatio.write(storeChanRatios)
        # recordIndex.write(output)

        sampleIndex = 0 # restart new store

    elapsed_time = time() - start_time # in seconds
