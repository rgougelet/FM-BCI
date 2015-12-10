import pylab
import numpy as np
import scipy as sp
import scipy.fftpack
from scipy import signal
from scipy.signal import butter, lfilter 
from scipy import linalg
from scipy.linalg import toeplitz, eig
import matplotlib.pyplot as plt
#from scikits.talkbox import lpc
import time

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
    
def chan_music(voltageSamples,sampleRate, desiredFreqResolution):
    rxx = np.correlate(voltageSamples,voltageSamples, 'full')
    rxx = rxx[rxx.size/2:]
    Rxx = linalg.toeplitz(rxx)
    sampleSpacing = 1.0/sampleRate 
    # z = np.vstack((voltageSamples,voltageSamples))
    #covv = np.cov(z.T)
    fftLengthSamples = int(sampleRate/desiredFreqResolution)
    M = len(voltageSamples)
    p = 6
    eigenValues,eigenVectors = linalg.eig(Rxx)
    idx = eigenValues.argsort()[::-1]   
    eigenValues = eigenValues[idx]
    eigenVectors = eigenVectors[:,idx]
    print np.shape(eigenVectors)
    #sum(abs(fft(d(:,0:M-2*p),fftLengthSamples)).^2,2)/(M-p)
    #Pxx = sum(abs(np.fft.rfft(eigenVectors[:,:M-2*p],fftLengthSamples)),0)
    Pxx = sum(abs(np.fft.rfft(eigenVectors,fftLengthSamples)),0)
    print np.shape(Pxx)
    freqs = np.fft.rfftfreq(fftLengthSamples,sampleSpacing)
    fig=plt.figure(figsize=(12, 9))
    plt.plot(freqs,Pxx)
    plt.show()
    #print np.shape(covv)
    #print covv
    #plt.imshow(covv)
    #plt.show()
    #print Rxx
    
def chan_per(voltageSamples, sampleRate):
    f, t, Sxx = signal.spectrogram(voltageSamples, sampleRate)
    plt.pcolormesh(t, f, Sxx)
    plt.title('Channel '+str(channelIndex+1))
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.show()
    
def chan_autocorr(voltageSamples, sampleRate, desiredFreqResolution):
        
        voltageSamples = signal.detrend(voltageSamples, axis=-1, type='linear')
        voltageSamples = np.pad(voltageSamples,(2,), 'mean')
        voltageSamples = voltageSamples * signal.hanning(len(voltageSamples))
        
        orderAxis = range(0,len(voltageSamples))
        errors = np.empty([len(orderAxis),])
        for order in orderAxis:
            lpcp, g, k = lpc(voltageSamples,order)
            errors[order] = g
        
        # fig=plt.figure(figsize=(12, 9))
        # plt.plot(orderAxis,np.abs(errors))
        #minError = np.argmax(np.abs(errors))
        #if minError == 0:
        #    minError = 14
        #print minError
        # plt.xlabel('Inverse Filter Order')
        # plt.ylabel('Error')
        # plt.grid()
        # plt.show()
        
        fftLengthSamples = int(sampleRate/desiredFreqResolution)
        # lpcp, g, k = lpc(voltageSamples,minError)
        lpcp, g, k = lpc(voltageSamples,4)
        lpcp = np.array(lpcp)
        rts = np.roots(lpcp)
        rts = rts[np.imag(rts)>=0];
        angz = np.arctan2(np.imag(rts),np.real(rts))
        frqs = np.sort(angz*sampleRate/(2*np.pi))
        pks = np.empty(0)
        for kk in range(len(frqs)):
            if (frqs[kk] > 6 and frqs[kk] < 14):
                pks = np.append(pks,frqs[kk])
        peak_freq = np.mean(pks)
        #print peak_freq
        padLength = fftLengthSamples-len(lpcp)
        padding = np.zeros(padLength)
        Ahat = np.concatenate((lpcp, padding), axis=1)
        FFTAh = np.fft.fft(Ahat,fftLengthSamples)
        halfFFTAh = FFTAh[:((fftLengthSamples/2))]
        magFFTAh = np.square(np.abs(halfFFTAh));
        dbFFTAh = 10*np.log10(1/magFFTAh);
        #freqs = (sampleRate/2)*np.linspace(0,1,fftLengthSamples/2)

        return dbFFTAh

def peak_freq(chanSpec, desiredFreqResolution):
    """ takes in a matrix of median spectrum (numOfChannel X len(freqs))  
        returns the peak frequencys 
    """
    numOfChannel = chanSpec.shape[0]
    peak_alpha_freq = np.empty([numOfChannel,])
    for channelIndex in range(numOfChannel):
        medianPeak = chan_peak_freq(chanSpec[channelIndex,:], desiredFreqResolution)
        peak_alpha_freq[channelIndex] = medianPeak
    return peak_alpha_freq

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
    """ takes in an array of median spectrum 
        returns the peak frequency 
    """
    freqs = np.empty(len(chanSpec))
    for i in range(0,len(chanSpec)):
        freqs[i] = i*desiredFreqResolution
    maxAmplitudeIndex = np.argmax(chanSpec)
    maxFreq = freqs[maxAmplitudeIndex]
    maxFreqAmp = chanSpec[maxAmplitudeIndex]
    return maxFreq, maxAmplitudeIndex
    
def chan_amp_ratio(chanSpec, desiredFreqResolution, lower, upper):
    """ Takes in the spectrum with lower and upper bound.
        Returns the signal to noise ratio for the channel. The biggest 
        signal/noise ratio(the bigger the ratio means the smaller the noise) 
        is used to determine the channel such that the channels' alpha band's
        amplitude is the highest in the spectrum. 
    """
    freqs = np.empty(len(chanSpec))
    for i in range(0,len(chanSpec)):
        freqs[i] = i*desiredFreqResolution
    lowerIndex = np.where(freqs==lower)
    lowerIndex = lowerIndex[0][0]
    upperIndex = np.where(freqs==upper)
    upperIndex = upperIndex[0][0]
    band_amp = np.mean(chanSpec[lowerIndex:upperIndex])
    mean_amp = np.mean(chanSpec)

    return band_amp/mean_amp

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



