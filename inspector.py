import platform
import numpy as np
import imp
pylsl = imp.load_source('pylsl.py', 'C:\Users\ces\Dropbox\LSE\Code\SNAP\src\modules\FM-BCI\pylsl\pylsl.py')
import processing as p
import record

for clearline in range(1,100):
    print('\n')

# initialize data stream
print("looking for an EEG stream...")
streams = pylsl.resolve_stream('name', 'SimulatedEEG')
inlet = pylsl.StreamInlet(streams[0])

# Extract stream info
inf = inlet.info()
sampleRate = inf.nominal_srate()
numOfChannel = inf.channel_count()
#sample = pylsl.vectorf()

# Initialize the recorder 
recorder = record.Recorder()

# Processing parameters
dataLengthSecs = 5
dataLengthSamples = int(dataLengthSecs * sampleRate)
bandLow = 8                                # lower alpha band 
bandHigh = 12                              # higher alpha band
orderFilter = 4
voltageSamples = np.empty([numOfChannel,dataLengthSamples])
desiredFreqResolution = 0.1
winLengthSamples = 512
overlapSamples = 256

info = pylsl.StreamInfo('BCI_Stream', 'EEG', 1, dataLengthSecs, 'float32', 'myuid34234')
outlet = pylsl.StreamOutlet(info)
output = np.empty(1)
print("\n \nSending data...")

print("Collecting data in "+str(dataLengthSecs)+" second chunks.")
sampleIndex = 0
#peak_alpha_freqs = np.zeros([numOfChannel,0]) # grows with every chunk and stores peaks for each channel
while True:

    # populating the samples
    sample, timestamp = inlet.pull_sample()
    voltageSamples[:, sampleIndex] = sample
    sampleIndex += 1

    # process data chunk
    if sampleIndex == dataLengthSamples:
        break
voltageSamples = p.butter_bandpass_filter(voltageSamples,bandLow,bandHigh,sampleRate,orderFilter)
peak_alpha_freq = np.empty([numOfChannel,])
for channelIndex in range(numOfChannel):
    meanSpectrum = p.chan_spect_mean(voltageSamples[channelIndex,:], sampleRate, desiredFreqResolution, winLengthSamples,overlapSamples)
    meanPeak = p.chan_peak_freq(meanSpectrum, desiredFreqResolution)
    peak_alpha_freq[channelIndex] = medianPeak
    peak_alpha_freqs = np.c_[peak_alpha_freqs, peak_alpha_freq] # append to storage array
    p.chan_plot_freq(meanSpectrum, desiredFreqResolution)