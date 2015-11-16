import pylab
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack
from scipy import signal
from parabolic import parabolic
import random
import time
import math

def processPAF(voltageSamples,sampleRate):
    # Number of samplepoints
    numOfChannel = voltageSamples.shape[0]     # number of channels
    dataLengthSamples = voltageSamples.shape[1]        # sample size
    sampleSpacing = 1.0 / sampleRate        
    dataLengthSecs = dataLengthSamples/sampleRate
    desiredFreqResolution = 1
    paddingMultiple = 1./desiredFreqResolution
    fftLengthSamples = dataLengthSamples*int(paddingMultiple)
    nyq = 0.5*sampleRate
    time = np.arange(0,dataLengthSecs,sampleSpacing)

    # going through each channel to plot fft result 
    for channelIndex in range(0,numOfChannel):

        # detrend and window channel
        channelVoltage = voltageSamples[channelIndex,:] - np.mean(voltageSamples[channelIndex,:])
		
		# filter data
		
		# window data
        windowed = channelVoltage * signal.blackmanharris(dataLengthSamples)
        #windowed = channelVoltage * signal.gaussian(dataLengthSamples, std=8,sym=False)
        
        # compute fft
        amp = abs(scipy.fftpack.rfft(channelVoltage,fftLengthSamples))
        freqs = scipy.fftpack.rfftfreq(fftLengthSamples,sampleSpacing)

        # find peak frequency
        maxAmplitudeIndex = np.argmax(amp)
        true_maxAmplitudeIndex = parabolic(np.log(amp), maxAmplitudeIndex)[0]
        maxFreq = nyq * maxAmplitudeIndex / fftLengthSamples
        true_maxFreq = nyq * true_maxAmplitudeIndex / fftLengthSamples
        print('Channel '+str(channelIndex+1)+':     '+str(true_maxFreq)+'  '+str(maxFreq))

        # do not run this cuz you are gonna get bombarded with plots
        
        # plot the figures
        fig=plt.figure(figsize=(12, 9))
        ax1=fig.add_subplot(211)
        fig.suptitle('Channel '+str(channelIndex+1), fontsize=20)
        ax1.set_xlabel('Time [s]')
        ax1.set_ylabel('Voltage [V]')
        ax1.plot(channelVoltage)
        ax1.grid()

        ax2=fig.add_subplot(212)
        ax2.set_xlabel('Frequency [Hz]')
        ax2.set_ylabel('Amplitude')
        ax2.plot(freqs, amp)
        ax2.plot(freqs[maxAmplitudeIndex], amp[maxAmplitudeIndex], 'rD')   # highest frequency marker
        ax2.grid()

        plt.show()

