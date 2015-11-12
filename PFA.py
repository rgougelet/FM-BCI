import pylab
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack
from scipy import signal
from parabolic import parabolic
import random
import time
import math

def processingPAF(voltageSamples,sampleRate):

<<<<<<< HEAD
    # Number of samplepoints
    numOfChannel = voltageSamples.shape[0]     # number of channels
    dataLengthSamples = voltageSamples.shape[1]        # sample size
    sampleSpacing = 1.0 / sampleRate        
    dataLengthSecs = dataLengthSamples/sampleRate
    desiredFreqResolution = 0.01
    paddingMultiple = 1/desiredFreqResolution
    fftLengthSamples = dataLengthSamples*int(paddingMultiple)
    nyq = 0.5*sampleRate
    
=======

# voltage = matrix[numOfChannel,numOfSamplesPerSecond]
def processingPAF(voltageSamples, timeStamp):
    # Number of samplepoints
    numOfChannel = voltageSamples.shape[0]     # number of channels
    samples = voltageSamples.shape[1]          # sample size

    sampleSpacing = 1.0 / samples       # sample spacing
    t = np.linspace(0.0, samples * sampleSpacing, samples)

    # print out time stamp
    print("Time: ", timeStamp)

>>>>>>> 8269aee04574e7b156d55170f2f4e5e563106e05
    # going through each channel to plot fft result 
    for channelIndex in range(0,numOfChannel):

        # detrend and window channel
        channelVoltage = voltageSamples[channelIndex,:] - np.mean(voltageSamples[channelIndex,:])
        #windowed = channelVoltage * signal.blackmanharris(dataLengthSamples)
        windowed = channelVoltage * signal.gaussian(dataLengthSamples, std=8,sym=False)
        
        # compute fft
        amp = abs(scipy.fftpack.rfft(channelVoltage,fftLengthSamples))
        freqs = scipy.fftpack.rfftfreq(fftLengthSamples,sampleSpacing)

        # find peak frequency
        maxAmplitudeIndex = np.argmax(amp)
        true_maxAmplitudeIndex = parabolic(np.log(amp), maxAmplitudeIndex)[0]
        maxFreq = sampleRate * maxAmplitudeIndex / fftLengthSamples
        true_maxFreq = sampleRate * true_maxAmplitudeIndex / fftLengthSamples
        print('Channel '+str(channelIndex+1)+':     '+str(true_maxFreq)+'  '+str(maxFreq))

        # do not run this cuz you are gonna get bombarded with plots
<<<<<<< HEAD
        
        # plot the figures
        # fig=plt.figure(figsize=(12, 9))
        # ax1=fig.add_subplot(211)
        # fig.suptitle('Channel '+str(channelIndex+1), fontsize=20)
        # ax1.set_xlabel('Time [s]')
        # ax1.set_ylabel('Voltage [V]')
        # ax1.plot(channelVoltage)
        # ax1.grid()

        # ax2=fig.add_subplot(212)
        # ax2.set_xlabel('Frequency [Hz]')
        # ax2.set_ylabel('Amplitude')
        # ax2.plot(freqs, amp)
        # ax2.plot(freqs[true_maxAmplitudeIndex], amp[true_maxAmplitudeIndex], 'rD')   # highest frequency marker
        # ax2.grid()

        # plt.show()
=======

        # plot the figures
        fig=plt.figure(figsize=(12, 9))
        fig.suptitle(('channel ' + repr(channelIndex + 1)), fontsize=14, fontweight='bold')
        ax1=fig.add_subplot(211)
        # ax1.set_title('axes title')
        ax1.set_xlabel('Time [s]')
        ax1.set_ylabel('Voltage [V]')
        ax1.plot(t, voltage)
        ax1.grid()

        ax2=fig.add_subplot(212)
        ax2.set_xlabel('Frequency [Hz]')
        ax2.set_ylabel('Amplitude')
        # show to top 128 frequencies
        ax2.plot(fx_bins[0:128], abs(fy[0:128]))
        ax2.plot(fx_bins[maxAmplitude], abs(fy[maxAmplitude]), 'rD')   # highest frequency marker
        ax2.grid()

        plt.show()
>>>>>>> 8269aee04574e7b156d55170f2f4e5e563106e05


