import processing as p
import oscillation as o
import numpy as np
import matplotlib.pyplot as plt

sampleRate = 1024.
sampleSpacing = 1./sampleRate
dataLengthSecs = 1
dataLengthSamples = dataLengthSecs * sampleRate
dataTime = np.arange(0,dataLengthSecs,sampleSpacing)
desiredFreqResolution = 0.01
winLengthSamples = 512
overlapSamples = 256

bandLow = 8
bandHigh = 12
orderFilter = 4  

alphaCenter = 10   # Hz the carrier frequency
alphaModFreq = 0.1  # Hz the modulating frequency
alphaFreqDev = 1    # Hz of the frequency deviation

numRuns = 1000
results = np.empty([numRuns,2])

for run in range(0,numRuns):
    # generate alpha rhythm
    voltageSamples = o.fm_noisy(dataLengthSamples, sampleRate, alphaCenter, alphaModFreq, alphaFreqDev)
    #voltageSamples = o.sin_noisy(dataLengthSamples, sampleRate,alphaCenter)
    #p.chan_plot_time(dataTime,voltageSamples)

    # filter
    voltageSamples = p.butter_bandpass_filter(voltageSamples, bandLow, bandHigh, sampleRate, orderFilter)

    medianSpectrum = p.chan_spect_median(voltageSamples, sampleRate, desiredFreqResolution, winLengthSamples, overlapSamples)
    #p.chan_plot_freq(medianSpectrum, desiredFreqResolution)

    meanSpectrum = p.chan_welch(voltageSamples, sampleRate, desiredFreqResolution, winLengthSamples, overlapSamples)
    #p.chan_plot_freq(meanSpectrum, desiredFreqResolution)
    
    medianPeak = p.chan_peak_freq(medianSpectrum, desiredFreqResolution)
    meanPeak = p.chan_peak_freq(meanSpectrum, desiredFreqResolution)
    
    results[run,:] = medianPeak, meanPeak
print np.mean(results,0)
    #plt.show()
