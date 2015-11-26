import pylab
import numpy as np
import scipy as sp
import scipy.fftpack
from scipy import signal
from scipy.signal import butter, lfilter  
import matplotlib.pyplot as plt


def spect_median(voltageSamples, sampleRate, desiredFreqResolution, winLengthSamples, overlapSamples):
    """ voltageSamples is a (numOfChannel X dataLengthSamples) matrix, 
        returns the median spectrum (numOfChannel X len(freqs)) from welch like method 
    """
    # Universal FFT parameters
    sampleRate = float(sampleRate)
    numOfChannel = voltageSamples.shape[0]
    dataLengthSamples = voltageSamples.shape[1]
    dataLengthSecs = dataLengthSamples / sampleRate
    sampleSpacing = 1.0/sampleRate        
    nyq = 0.5 * sampleRate
    fftLengthSamples = int(sampleRate/desiredFreqResolution)
    freqs = np.fft.rfftfreq(fftLengthSamples,sampleSpacing)
    stepSize = overlapSamples
    winSpectra = np.empty([len(freqs),0])
    stepIndex = 0
    winStart = 0

    medianSpecMat = np.empty([numOfChannel, len(freqs)])
    for channelIndex in range(numOfChannel):
        while winStart + winLengthSamples < dataLengthSamples:
            # get next window
            winStart = stepIndex*stepSize
            winStop = winStart + winLengthSamples
            voltageSamplesWin = voltageSamples[channelIndex,winStart:winStop]

            # detrend
            voltageSamplesWin = signal.detrend(voltageSamplesWin, axis=-1, type='linear')
    
            # window window
            windowedWin = voltageSamplesWin * signal.hanning(winLengthSamples)

            # compute fft
            amp = abs(np.fft.rfft(windowedWin,fftLengthSamples))
            winSpectra = np.c_[winSpectra,amp]
            stepIndex+=1 

        medianSpectrum = np.median(winSpectra,1)
        medianSpecMat[channelIndex,:] = medianSpectrum
        
    return medianSpecMat
    

def peak_freq(chanSpec, desiredFreqResolution):
    """ takes in a matrix of median spectrum (numOfChannel X len(freqs)) and returns the peak frequencys """
    numOfChannel = chanSpec.shape[0]
    peak_alpha_freq = np.empty([numOfChannel,])
    for channelIndex in range(numOfChannel):
        medianPeak = chan_peak_freq(chanSpec[channelIndex,:], desiredFreqResolution)
        peak_alpha_freq[channelIndex] = medianPeak
    return peak_alpha_freq


# original mat_spect_median by Robert

# def mat_spect_median(voltageSamples, sampleRate, desiredFreqResolution, winLengthSamples):
#     """ voltageSamples is a (numOfChannel X dataLengthSamples) matrix """

#     # Universal FFT parameters
#     numOfChannel = voltageSamples.shape[0]
#     dataLengthSamples = voltageSamples.shape[1]
#     dataLengthSecs = (int)(dataLengthSamples / sampleRate) 
#     sampleSpacing = 1.0 / sampleRate        
#     nyq = 0.5 * sampleRate
#     fftLengthSamples = int(sampleRate/desiredFreqResolution)
#     freqs = scipy.fftpack.rfftfreq(fftLengthSamples,sampleSpacing) # retrieve frequency axis
#     dataTime = np.arange(0,dataLengthSecs,sampleSpacing)
    
#     # Window data FFT parameters
#     winLengthSecs = winLengthSamples/sampleRate
#     numOfWindows = int(dataLengthSamples/winLengthSamples) # determine number of windows
#     winTime = np.arange(0,winLengthSecs,sampleSpacing)
    
#     # going through each channel to plot fft result
#     channelPeaks = np.empty([numOfChannel, numOfWindows]) # container for peak frequencies for each channel every second
    
#     for channelIndex in range(0,numOfChannel):
#         channelVoltage = voltageSamples[channelIndex,:]
#         channelWinSpectra = np.empty([len(freqs), numOfWindows])
#         for winIndex in range(0,numOfWindows):
#             # get next window of data, detrend
#             channelVoltageWin = channelVoltage[winIndex*winLengthSamples:(winIndex+1)*winLengthSamples]
#             channelVoltageWin = channelVoltageWin - np.mean(channelVoltageWin)
            
#             # window window
#             #windowedWin = channelVoltage * signal.blackmanharris(winLengthSamples)
#             windowedWin = channelVoltageWin * signal.gaussian(winLengthSamples, std=8,sym=False)

#             # compute fft
#             nyq = 0.5 * sampleRate # maximum possible frequency to measure
#             amp = abs(scipy.fftpack.rfft(windowedWin,fftLengthSamples)) # determine amplitude spectrum by taking abs
#             channelWinSpectra[:,winIndex] = amp
            
#         medianSpectrum = np.transpose(np.median(channelWinSpectra,1))
        
#     return medianSpectrum


def chan_welch(voltageSamples, sampleRate, desiredFreqResolution, winLengthSamples, overlapSamples):
    dataLengthSamples = len(voltageSamples)
    dataLengthSecs = dataLengthSamples / sampleRate
    sampleSpacing = 1.0/sampleRate        
    fftLengthSamples = int(sampleRate/desiredFreqResolution)
    f,pspec = sp.signal.welch(voltageSamples, fs=sampleRate, window='hanning', nperseg=fftLengthSamples, noverlap=overlapSamples, nfft=fftLengthSamples, detrend='linear', return_onesided=True, scaling='density')
    return pspec
    

def mat_welch():
    return

    
def chan_spect_median(voltageSamples, sampleRate, desiredFreqResolution, winLengthSamples, overlapSamples):
    """ voltageSamples is an array contains voltage samples, 
        returns the array that contains the median spectrum from welch like method 
    """
    sampleRate = float(sampleRate)
    # Universal FFT parameters
    dataLengthSamples = len(voltageSamples)
    dataLengthSecs = dataLengthSamples / sampleRate
    sampleSpacing = 1.0/sampleRate        
    nyq = 0.5 * sampleRate
    fftLengthSamples = int(sampleRate/desiredFreqResolution)
    freqs = np.fft.rfftfreq(fftLengthSamples,sampleSpacing)
    stepSize = overlapSamples
    winSpectra = np.empty([len(freqs),0])
    stepIndex = 0
    winStart = 0

    while winStart + winLengthSamples < dataLengthSamples:
        # get next window
        winStart = stepIndex*stepSize
        winStop = winStart + winLengthSamples
        voltageSamplesWin = voltageSamples[winStart:winStop]

        # detrend
        voltageSamplesWin = signal.detrend(voltageSamplesWin, axis=-1, type='linear')
        
        # window window
        windowedWin = voltageSamplesWin * signal.hanning(winLengthSamples)

        # compute fft
        amp = abs(np.fft.rfft(windowedWin,fftLengthSamples))
        winSpectra = np.c_[winSpectra,amp]
        stepIndex+=1 

    medianSpectrum = np.median(winSpectra,1)
        
    return medianSpectrum
    

def chan_peak_freq(chanSpec, desiredFreqResolution):
    """ takes in an array of median spectrum and returns the peak frequency """
    freqs = np.empty(len(chanSpec))
    for i in range(0,len(chanSpec)):
        freqs[i] = i*desiredFreqResolution
    maxAmplitudeIndex = np.argmax(chanSpec)
    maxFreq = freqs[maxAmplitudeIndex]
    return maxFreq


def chan_peak_freq_parab(chanSpec, desiredFreqResolution):
    from parabolic import parabolic
    freqs = np.empty(len(chanSpec))
    for i in range(0,len(chanSpec)):
        freqs[i] = i*desiredFreqResolution
    sampleRate = (freqs[-1]*2)
    fftLengthSamples = sampleRate/desiredFreqResolution
    maxAmplitudeIndex = parabolic(np.log(chanSpec), np.argmax(chanSpec)-1)[0]
    maxFreq =  freqs[-1] * maxAmplitudeIndex / fftLengthSamples


def butter_bandpass_filter(mydata, lowcut, highcut, fs, order=4):
    """ takes in a matrix of sample data (numOfChannel X dataLengthSamples) and filter out the alpha freq"""
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
    plt.draw()
    
    
def chan_plot_freq(chanSpec, desiredFreqResolution):
    freqs = np.empty(len(chanSpec))
    for i in range(0,len(chanSpec)):
        freqs[i] = i*desiredFreqResolution
    fig=plt.figure(figsize=(12, 9))
    plt.plot(freqs,chanSpec)
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitude')
    plt.grid()
    plt.draw()



