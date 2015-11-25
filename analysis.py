import processing as p
import oscillation as o
import numpy as np

sampleRate = 1024.
sampleSpacing = 1./sampleRate
dataLengthSecs = 1
dataLengthSamples = dataLengthSecs * sampleRate
dataTime = np.arange(0,dataLengthSecs,sampleSpacing)

bandLow = 8
bandHigh = 12
orderFilter = 4  

alphaCenter = 10.25   # Hz the carrier frequency
alphaModFreq = 0.1  # Hz the modulating frequency
alphaFreqDev = 1    # Hz of the frequency deviation

# generate alpha rhythm
voltageSamples = o.fm_noisy(dataLengthSamples, sampleRate, alphaCenter, alphaModFreq, alphaFreqDev)
p.chan_plot_time(dataTime,voltageSamples)

# filter
voltageSamples = p.butter_bandpass_filter(voltageSamples, bandLow, bandHigh, orderFilter)

# find spectral median
p.chan_spect_median(voltageSamples)    
