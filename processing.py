import pylab
import numpy as np
import scipy as sp
import scipy.fftpack
from scipy import signal
from parabolic import parabolic
import random
import time
import math
from scipy.signal import butter, lfilter  
import matplotlib.pyplot as plt

# returns peak alpha frequencys of voltage over a period of time
def spectral_averaging_batch(dataLengthSamples, sampleRate, numOfChannel, bandLow = 8, bandHigh = 12, orderFilter = 4):
    totalNumOfSamples = dataLengthSamples.shape[1]
    dataLengthSecs = (int)(totalNumOfSamples / sampleRate)  
    # peak_alpha_freq is a (numOfChannelss X numOfSamples) matrix 
    peak_alpha_freqs = np.zeros([numOfChannel, 0])       

    for timeIndex in range(0,dataLengthSecs):
        voltageSamples = dataLengthSamples[:, (sampleRate*timeIndex):(sampleRate*(timeIndex+1)):1]

        peak_alpha_freq = spectral_averaging(voltageSamples, sampleRate, numOfChannel)
        # append outputColData as column to the peak_alpha_freq array
        peak_alpha_freqs = np.c_[peak_alpha_freqs, peak_alpha_freq] 
        # print peak_alpha_freqs

    return peak_alpha_freqs


# returns peak alpha frequency of voltage samples in one second
def spectral_averaging(voltageSamples, sampleRate, numOfChannel, bandLow = 8, bandHigh = 12, orderFilter = 4):
    """ voltageSamples is a (numOfChannel X sampleSize) matrix """

    # Universal FFT parameters
    numOfChannel = voltageSamples.shape[0]

    if numOfChannel != numOfChannel:
        print "Warning: numOfChannel specified in object creation does not match with that of the voltageSamples."
        exit()

    sampleSpacing = 1.0 / sampleRate        
    desiredFreqResolution = 0.01
    nyq = 0.5 * sampleRate
    fftLengthSamples = int(sampleRate/desiredFreqResolution)
    freqs = scipy.fftpack.rfftfreq(fftLengthSamples,sampleSpacing) # retrieve frequency axis
    
    # Full data length FFT paramaters
    dataLengthSamples = voltageSamples.shape[1]
    dataLengthSecs = dataLengthSamples/sampleRate
    dataTime = np.arange(0,dataLengthSecs,sampleSpacing)
    
    # Window data FFT parameters
    winLengthSecs = 0.25 # predefine length of window.
    winLengthSamples = winLengthSecs * sampleRate # length of window in samples
    numOfWindows = int(dataLengthSamples/winLengthSamples) # determine number of windows
    winTime = np.arange(0,winLengthSecs,sampleSpacing)
    
    # going through each channel to plot fft result
    channelPeaks = np.empty([numOfChannel, numOfWindows]) # container for peak frequencies for each channel every second
    
    for channelIndex in range(0,numOfChannel):
        channelVoltage = voltageSamples[channelIndex,:]
        channelWinSpectra = np.empty([len(freqs), numOfWindows])
        
        # filter data before parsing
        channelVoltage = butter_bandpass_filter(channelVoltage, bandLow, bandHigh, sampleRate, orderFilter)
        
        # TODO: Xiang, Kalman filter

        for winIndex in range(0,numOfWindows):
            # get next window of data, detrend
            channelVoltageWin = channelVoltage[winIndex*winLengthSamples:(winIndex+1) * winLengthSamples] \
            - np.mean(channelVoltage[winIndex*winLengthSamples:(winIndex+1)*winLengthSamples])

            # window next window of data
            #windowed = channelVoltage * signal.blackmanharris(winLengthSamples)
            windowedWin = channelVoltageWin * signal.gaussian(winLengthSamples, std=8,sym=False)

            # compute fft
            nyq = 0.5 * sampleRate # maximum possible frequency to measure
            amp = abs(scipy.fftpack.rfft(windowedWin,fftLengthSamples)) # determine amplitude spectrum by taking abs

            # find peak frequency
            maxAmplitudeIndex = np.argmax(amp) # finds simple max amp peak
            maxFreq = freqs[maxAmplitudeIndex] # retrieves frequency of peak
            # print('Channel '+str(channelIndex+1)+ ', Window '+str(winIndex+1)+':     '+str(maxFreq))
            #true_maxAmplitudeIndex = parabolic(np.log(amp), maxAmplitudeIndex-1)[0] # finds parabolic interpolation
            #true_maxFreq = nyq * true_maxAmplitudeIndex / fftLengthSamples # retrieves frequency of parabolic peak
            #print('Channel '+str(channelIndex+1)+ ', Window '+str(winIndex+1)+':     '+str(true_maxFreq)+'  '+str(maxFreq))
            channelPeaks[channelIndex,winIndex] = maxFreq # stores peak frequency for every window
            channelWinSpectra[:,winIndex] = amp


            # plot(channelIndex, channelVoltage, freqs, amp, maxAmplitudeIndex, channelWinSpectra)
            # plt.show()


    # peak alpha frequency from averaging windows, either mean or median
    medianChannelsPeaks = np.transpose(np.median(channelPeaks,1))
    meanChannelsPeaks = np.transpose(np.mean(channelPeaks,1))
        
    return meanChannelsPeaks


def butter_bandpass(lowcut, highcut, fs, order=4):
    #lowcut is the lower bound of the frequency that we want to isolate
    #hicut is the upper bound of the frequency that we want to isolate
    #fs is the sampling rate of our data
    nyq = 0.5 * fs #nyquist frequency - see http://www.dspguide.com/ if you want more info
    low = float(lowcut) / nyq
    high = float(highcut) / nyq
    b, a = sp.signal.butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(mydata, lowcut, highcut, fs, order=4):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = sp.signal.filtfilt(b, a, mydata)
    return y










# used to plot spectral_averaging

def plot(channelIndex, channelVoltage, freqs, amp, maxAmplitudeIndex, channelWinSpectra):
    """ plot the figures """
    fig=plt.figure(figsize=(12, 9))
    fig.suptitle('Channel '+str(channelIndex+1), fontsize=20)

    ax1=fig.add_subplot(211)
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Voltage [V]')
    ax1.plot(channelVoltage)
    ax1.grid()

    ax2=fig.add_subplot(212)
    ax2.set_xlabel('Frequency [Hz]')
    ax2.set_ylabel('Amplitude')
    ax2.plot(freqs, np.mean(channelWinSpectra,1))
    # ax2.plot(freqs[maxAmplitudeIndex], amp[maxAmplitudeIndex], 'rD')   # highest frequency marker

