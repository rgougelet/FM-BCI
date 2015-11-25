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

# returns peak alpha frequency of voltage samples in one second
def chan_spect_median(voltageSamples, sampleRate, winLengthSamples, desiredFreqResolution):
    """ voltageSamples is a (numOfChannel X dataLengthSamples) matrix """

    # Universal FFT parameters
    numOfChannel = voltageSamples.shape[0]
    dataLengthSamples = dataLengthSamples.shape[1]
    dataLengthSecs = (int)(totalNumOfSamples / sampleRate) 
    sampleSpacing = 1.0 / sampleRate        
    nyq = 0.5 * sampleRate
    fftLengthSamples = int(sampleRate/desiredFreqResolution)
    freqs = scipy.fftpack.rfftfreq(fftLengthSamples,sampleSpacing) # retrieve frequency axis
    dataTime = np.arange(0,dataLengthSecs,sampleSpacing)
    
    # Window data FFT parameters
    winLengthSecs = winLengthSamples/sampleRate
    numOfWindows = int(dataLengthSamples/winLengthSamples) # determine number of windows
    winTime = np.arange(0,winLengthSecs,sampleSpacing)
    
    # going through each channel to plot fft result
    channelPeaks = np.empty([numOfChannel, numOfWindows]) # container for peak frequencies for each channel every second
    
    for channelIndex in range(0,numOfChannel):
        channelVoltage = voltageSamples[channelIndex,:]
        channelWinSpectra = np.empty([len(freqs), numOfWindows])
        for winIndex in range(0,numOfWindows):
            # get next window of data, detrend
            channelVoltageWin = channelVoltage[winIndex*winLengthSamples:(winIndex+1)*winLengthSamples]
            channelVoltageWin = channelVoltageWin - np.mean(channelVoltageWin)
            
            # window window
            #windowedWin = channelVoltage * signal.blackmanharris(winLengthSamples)
            windowedWin = channelVoltageWin * signal.gaussian(winLengthSamples, std=8,sym=False)

            # compute fft
            nyq = 0.5 * sampleRate # maximum possible frequency to measure
            amp = abs(scipy.fftpack.rfft(windowedWin,fftLengthSamples)) # determine amplitude spectrum by taking abs
            channelWinSpectra[:,winIndex] = amp
            
        medianSpectrum = np.transpose(np.median(channelWinSpectra,1))
        
    return medianSpectrum
    
def chan_peak_freq(spectrum):
    maxAmplitudeIndex = np.argmax(spectrum)
    maxFreq = freqs[maxAmplitudeIndex]
    
    #maxAmplitudeIndex = parabolic(np.log(amp), np.argmax(amp)-1)[0]
    #maxFreq = nyq * maxAmplitudeIndex / fftLengthSamples
    
    return maxFreq

def butter_bandpass_filter(mydata, lowcut, highcut, fs, order=4):
    nyq = 0.5 * fs
    low = float(lowcut) / nyq
    high = float(highcut) / nyq
    b, a = sp.signal.butter(order, [low, high], btype='band')
    y = sp.signal.filtfilt(b, a, mydata)
    return y

def chan_plot_time(t,channelVoltage):
    fig=plt.figure(figsize=(12, 9))
    plt.plot(t,channelVoltage)
    plt.xlabel('Time [s]')
    plt.ylabel('Voltage [V]')
    plt.grid()
    plt.show()
    
def chan_plot_freq(freqs, chanAmp):
    fig=plt.figure(figsize=(12, 9))
    plt.plot(freqs,chanAmp)
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitude')
    plt.grid()
    plt.show()


