import pylab
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import scipy.fftpack
from scipy import signal
from parabolic import parabolic
import random
import time
import math
from scipy.signal import butter, lfilter  
import record
import sys


class PAF:
    """ PAF is used to process the peak alpha frequency giving voltage samples and sample rate"""

    # peak_alpha_freqs = np.empty((8))

    def __init__(self, numOfChannel, sampleRate, bandLow, bandHigh, orderFilter):
        # intialize the filters
        self.bandLow = bandLow
        self.bandHigh = bandHigh
        self.orderFilter = orderFilter
        self.sampleRate = sampleRate
        self.numOfChannel = numOfChannel
        self.peak_alpha_freqs = np.zeros([numOfChannel, 1])       # peak_alpha_freq is a (numOfChannelss X numOfSamples) matrix 

        # Initialize the recorder 
        self.recorder = record.Recorder()
        # self.recorder.record_new()
        # self.recorder.write('Row = Channel \nColumn = true max freq per sample rate \n')

    def process_PAF(self, voltageSamples):
        """ voltageSamples is a (numOfChannel X sampleSize) matrix """

        # Universal FFT parameters
        numOfChannel = voltageSamples.shape[0]

        if numOfChannel != self.numOfChannel:
            self.warning("numOfChannel specified in object creation does not match with that of the voltageSamples.")

        sampleSpacing = 1.0 / self.sampleRate        
        desiredFreqResolution = 0.01
        nyq = 0.5*self.sampleRate
        fftLengthSamples = int(self.sampleRate/desiredFreqResolution)
        freqs = scipy.fftpack.rfftfreq(fftLengthSamples,sampleSpacing) # retrieve frequency axis
        
        # Full data length FFT paramaters
        dataLengthSamples = voltageSamples.shape[1]
        dataLengthSecs = dataLengthSamples/self.sampleRate
        dataTime = np.arange(0,dataLengthSecs,sampleSpacing)
        
        # Window data FFT parameters
        winLengthSecs = 0.25 # predefine length of window.
        winLengthSamples = winLengthSecs*self.sampleRate # length of window in samples
        # winLengthSamples = 128 # length of window in samples
        # winLengthSecs = winLengthSamples/float(self.sampleRate)
        numOfWindows = int(dataLengthSamples/winLengthSamples) # determine number of windows
        winTime = np.arange(0,winLengthSecs,sampleSpacing)
        
        # going through each channel to plot fft result
        channelPeaks = np.empty([numOfChannel, numOfWindows]) # container for peak frequencies for each channel every second
        
        for channelIndex in range(0,numOfChannel):
            channelVoltage = voltageSamples[channelIndex,:]
            channelWinSpectra = np.empty([len(freqs), numOfWindows])
            
            # filter data before parsing
            channelVoltage = self.butter_bandpass_filter(channelVoltage, self.bandLow, self.bandHigh,self.sampleRate,self.orderFilter)
            
            # TODO: Xiang, Kalman filter
            
            for winIndex in range(0,numOfWindows):
                # get next window of data, detrend
                channelVoltageWin = channelVoltage[winIndex*winLengthSamples:(winIndex+1)*winLengthSamples] \
                - np.mean(channelVoltage[winIndex*winLengthSamples:(winIndex+1)*winLengthSamples])

                # window next window of data
                #windowed = channelVoltage * signal.blackmanharris(winLengthSamples)
                windowedWin = channelVoltageWin * signal.gaussian(winLengthSamples, std=8,sym=False)

                # compute fft
                nyq = 0.5*self.sampleRate # maximum possible frequency to measure
                amp = abs(scipy.fftpack.rfft(windowedWin,fftLengthSamples)) # determine amplitude spectrum by taking abs

                # find peak frequency
                maxAmplitudeIndex = np.argmax(amp) # finds simple max amp peak
                maxFreq = freqs[maxAmplitudeIndex] # retrieves frequency of peak
                print('Channel '+str(channelIndex+1)+ ', Window '+str(winIndex+1)+':     '+str(maxFreq))
                #true_maxAmplitudeIndex = parabolic(np.log(amp), maxAmplitudeIndex-1)[0] # finds parabolic interpolation
                #true_maxFreq = nyq * true_maxAmplitudeIndex / fftLengthSamples # retrieves frequency of parabolic peak
                #print('Channel '+str(channelIndex+1)+ ', Window '+str(winIndex+1)+':     '+str(true_maxFreq)+'  '+str(maxFreq))
                channelPeaks[channelIndex,winIndex] = maxFreq # stores peak frequency for every window
                channelWinSpectra[:,winIndex] = amp
                
                # do not run this cuz you are gonna get bombarded with plots
                # self.plot(channelIndex, channelVoltage, freqs, amp, maxAmplitudeIndex)
                # plt.show()
                
        medianChannelsPeaks = np.transpose(np.median(channelPeaks,1))
        meanChannelsPeaks = np.transpose(np.mean(channelPeaks,1))
        
        self.peak_alpha_freq = meanChannelsPeaks
        # self.record_peak(self.peak_alpha_freq)
        
        # append outputColData as column to the peak_alpha_freq array
        self.peak_alpha_freqs = np.c_[ self.peak_alpha_freqs, self.peak_alpha_freq] 

    def plot(self, channelIndex, channelVoltage, freqs, amp, maxAmplitudeIndex):
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

        
    def butter_bandpass(self, lowcut, highcut, fs, order=4):
        #lowcut is the lower bound of the frequency that we want to isolate
        #hicut is the upper bound of the frequency that we want to isolate
        #fs is the sampling rate of our data
        nyq = 0.5 * fs #nyquist frequency - see http://www.dspguide.com/ if you want more info
        low = float(lowcut) / nyq
        high = float(highcut) / nyq
        b, a = sp.signal.butter(order, [low, high], btype='band')
        return b, a

    def butter_bandpass_filter(self, mydata, lowcut, highcut, fs, order=4):
        b, a = self.butter_bandpass(lowcut, highcut, fs, order=order)
        y = sp.signal.filtfilt(b, a, mydata)
        return y

    def record_peak(self, content):
        """ recording the peak at the end of the application all at once in pretty printing"""
        # self.recorder.record_raw(self.peak_alpha_freq)
        self.recorder.write(content)


    def warning (self, message):
        print "Warning: " + str(message)
        exit()

    def output_to_file_before_exit(self):
        """  output alpha peak frequency to file on KeyBoardInterrupt """
        print 'Saved Data:'
        print self.peak_alpha_freq
        self.recorder.record_raw(self.peak_alpha_freqs.transpose())
        



