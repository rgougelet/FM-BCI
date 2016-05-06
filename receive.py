<<<<<<< HEAD
import numpy as np
#from numpy import fft
from pylsl import StreamInlet, resolve_stream, vectorf, StreamInfo, StreamOutlet
import processing as p
import record
# from scikits.talkbox import lpc
from scipy import signal
import matplotlib.pyplot as plt


for clearline in range(1,20):
    print('\n')

# initialize data stream
print("Looking for an EEG stream...")
streams = []
while not streams:
    streams = resolve_stream('name', 'SimulatedEEG')
=======
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
>>>>>>> e86d00ecee6bb251e52daf833525f0da615d2865
inlet = StreamInlet(streams[0])

# Extract stream info
inf = inlet.info()
sampleRate = inf.nominal_srate()
numOfChannel = inf.channel_count()
<<<<<<< HEAD
#sample = pylsl.vectorf()

# Initialize the recorder 
recordFreq = record.Recorder("_Frequency")
recordAmp = record.Recorder("_Amplitude")
recordRatio = record.Recorder("_Ratio")
recordIndex = record.Recorder("_Index")
=======
sample = vectorf()

# Initialize the recorder 
recorder = record.Recorder()
>>>>>>> e86d00ecee6bb251e52daf833525f0da615d2865

# Processing parameters
dataLengthSecs = 1
dataLengthSamples = int(dataLengthSecs * sampleRate)
bandLow = 8                                # lower alpha band 
<<<<<<< HEAD
bandHigh = 12                             # higher alpha band
orderFilter = 4
voltageSamples = np.empty([numOfChannel,dataLengthSamples])
desiredFreqResolution = 1
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
        
        # chanPeakFreqs = np.empty([numOfChannel,])
        # chanPeakAmps = np.empty([numOfChannel,])
        # chanRatios = np.empty([numOfChannel])
        #voltageSamples = p.butter_bandpass_filter(voltageSamples,bandLow,bandHigh,sampleRate,orderFilter)
            
        for channelIndex in range(numOfChannel):
            
<<<<<<< HEAD
            #blah = p.chan_autocorr(voltageSamples[channelIndex,:], sampleRate, desiredFreqResolution)
            p.chan_music(voltageSamples[channelIndex,:], sampleRate, desiredFreqResolution)
=======
            # blah = p.chan_autocorr(voltageSamples[channelIndex,:], sampleRate, desiredFreqResolution)
 
>>>>>>> e4f33c72087e7b09fecf43fef6ab883767cd4063
            #p.chan_plot_freq(blah, desiredFreqResolution)
            #print "Channel ", channelIndex+1
            #plt.xlim(0,30)
            #plt.ylim(-50,0)
            #plt.show()
            # meanSpectrum = p.chan_welch(voltageSamples[channelIndex,:], sampleRate, desiredFreqResolution, winLengthSamples,overlapSamples)
            # chanRatio = p.chan_amp_ratio(meanSpectrum, desiredFreqResolution,bandLow,bandHigh)
            # chanPeak,chanPeakIndex = p.chan_peak_freq(meanSpectrum, desiredFreqResolution)
            
            # chanRatios[channelIndex] = chanRatio
            # chanPeakFreqs[channelIndex] = chanPeak
            # chanPeakAmps[channelIndex] = meanSpectrum[chanPeakIndex]
            
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
=======
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
            for channelIndex in range(numOfChannel):
                medianSpectrum = p.chan_spect_median(voltageSamples[channelIndex,:], sampleRate, desiredFreqResolution, winLengthSamples, overlapSamples)
                medianPeak = p.chan_peak_freq(medianSpectrum, desiredFreqResolution)

                peak_alpha_freq[channelIndex] = medianPeak
                
                peak_alpha_freqs = np.c_[peak_alpha_freqs, peak_alpha_freq] # append to storage array
            print peak_alpha_freq
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

>>>>>>> e86d00ecee6bb251e52daf833525f0da615d2865
