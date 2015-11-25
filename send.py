import time
from pylsl import StreamInfo, StreamOutlet, vectorf
import oscillation as o
import processing as p
import numpy as np

for clearline in range(1,100):
    print('\n')
    
# frequency modulation parameters
alphaCenter = 10.25   # Hz the carrier frequency
alphaModFreq = 0.1  # Hz the modulating frequency
alphaFreqDev = 1    # Hz of the frequency deviation

# generate data to send
sampleRate = 1024.0
numOfChannel = 8
dataLengthSecs = 300
dataLengthSamples = dataLengthSecs*sampleRate
voltageSamples = np.empty([numOfChannel,dataLengthSamples])
for channelIndex in range(0,numOfChannel):
    voltageSamples[channelIndex,:] = o.fm_noisy(dataLengthSamples, sampleRate, alphaCenter, alphaModFreq, alphaFreqDev)
voltageSamples[channelIndex,:] = o.fm(dataLengthSamples, sampleRate, alphaCenter, alphaModFreq, alphaFreqDev) # ground truth

# create outlet for output
info = StreamInfo('SimulatedEEG', 'EEG', numOfChannel, sampleRate, 'float32', 'myuid34234')
outlet = StreamOutlet(info)
print("\n \nSending data...")

for sample in voltageSamples.T:
    outlet.push_sample(sample)
    # wait precisely between samples
    start = time.clock()
    now = time.clock()
    while now < start + 1/sampleRate:
        now = time.clock()
        pass