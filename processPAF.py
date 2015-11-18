import pylab
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import scipy.fftpack
from scipy import signal
from parabolic import parabolic
import random
import time
import math
from scipy.signal import butter, lfilter  
import record

<<<<<<< HEAD
def processPAF(voltageSamples,sampleRate):

    # Universal FFT parameters
    numOfChannel = voltageSamples.shape[0]
    sampleSpacing = 1.0 / sampleRate        
    desiredFreqResolution = 0.01
    nyq = 0.5*sampleRate
    fftLengthSamples = int(sampleRate/desiredFreqResolution)
    freqs = scipy.fftpack.rfftfreq(fftLengthSamples,sampleSpacing) # retrieve frequency axis
    
    # Full data length FFT paramaters
    dataLengthSamples = voltageSamples.shape[1]
    dataLengthSecs = dataLengthSamples/sampleRate
    dataTime = np.arange(0,dataLengthSecs,sampleSpacing)
    
    # Window data FFT parameters
    winLengthSecs = 1 # predefine length of window.
    winLengthSamples = winLengthSecs*sampleRate # length of window in samples
    # winLengthSamples = 128 # length of window in samples
    # winLengthSecs = winLengthSamples/float(sampleRate)
    numOfWindows = int(dataLengthSamples/winLengthSamples) # determine number of windows
    winTime = np.arange(0,winLengthSecs,sampleSpacing)

    # going through each channel to plot fft result
    channelPeaks = np.empty([numOfChannel, numOfWindows]) # container for peak frequencies for each channel every second
    
    for channelIndex in range(0,numOfChannel):
        channelVoltage = voltageSamples[channelIndex,:]
        channelWinSpectra = np.empty([len(freqs), numOfWindows])
        
        # filter data before parsing
        bandlow =8
        bandhigh=12
        orderfilter=4
        channelVoltage = butter_bandpass_filter(channelVoltage,bandlow, bandhigh,sampleRate,orderfilter)
        
        for winIndex in range(0,numOfWindows):
            # get next window of data, detrend
            channelVoltageWin = channelVoltage[winIndex*winLengthSamples:(winIndex+1)*winLengthSamples] \
            - np.mean(channelVoltage[winIndex*winLengthSamples:(winIndex+1)*winLengthSamples])

            # window next window of data
            #windowed = channelVoltage * signal.blackmanharris(winLengthSamples)
            windowedWin = channelVoltageWin * signal.gaussian(winLengthSamples, std=8,sym=False)

            # compute fft
            nyq = 0.5*sampleRate # maximum possible frequency to measure
            amp = abs(scipy.fftpack.rfft(windowedWin,fftLengthSamples)) # determine amplitude spectrum by taking abs

            # find peak frequency
            maxAmplitudeIndex = np.argmax(amp) # finds simple max amp peak
            true_maxAmplitudeIndex = parabolic(np.log(amp), maxAmplitudeIndex-1)[0] # finds parabolic interpolation
            maxFreq = freqs[maxAmplitudeIndex] # retrieves frequency of peak
            true_maxFreq = nyq * true_maxAmplitudeIndex / fftLengthSamples # retrieves frequency of parabolic peak
            print('Channel '+str(channelIndex+1)+ ', Window '+str(winIndex+1)+':     '+str(true_maxFreq)+'  '+str(maxFreq))
            channelPeaks[channelIndex,winIndex] = true_maxFreq # stores peak frequency for every window
            channelWinSpectra[:,winIndex] = amp
        
        # plot the figures
=======
class PAF:
    """ PAF is used to process the peak alpha frequency giving voltage samples and sample rate"""

    sample_rate = 256.                          # sampling rate

    band_low = 8                                # lower alpha band 

    band_high = 12                              # higher alpha band

    order_filter = 4                            # filter order

    peak_alpha_freq = np.zeros([8, 1])          # peak_alpha_freq is a (numOfChanels X numOfSamples) matrix 

    recorder = None                             # used to record paf

    def __init__(self, sampleRate, bandLow, bandHigh, orderFilter):
        # intialize the filters
        self.band_low = bandLow
        self.band_high = bandHigh
        self.order_filter = orderFilter

        self.sample_rate = sampleRate

        # Initialize the recorder 
        self.recorder = record.Record()
        self.recorder.record_new()
        self.recorder.write('Row = Channel \nColumn = true max freq per sample rate \n')


    def process_PAF(self, voltageSamples):
        """ voltageSamples is a (numOfChannel X sampleSize) matrix """

        # Number of samplepoints
        numOfChannel = voltageSamples.shape[0]              # number of channels
        dataLengthSamples = voltageSamples.shape[1]         # sample size
        sampleSpacing = 1.0 / self.sample_rate        
        dataLengthSecs = dataLengthSamples / self.sample_rate
        desiredFreqResolution = 1
        paddingMultiple = 1./desiredFreqResolution
        fftLengthSamples = dataLengthSamples*int(paddingMultiple)
        nyq = 0.5 * self.sample_rate
        time = np.arange(0,dataLengthSecs,sampleSpacing)


        # contains data from all eight channels per sample as a column
        dataPerSampleRate = []

        # going through each channel to plot fft result 
        for channelIndex in range(0,numOfChannel):

            # detrend and window channel
            channelVoltage = voltageSamples[channelIndex,:] - np.mean(voltageSamples[channelIndex,:])
    		
            channelVoltage = self.butter_bandpass_filter(channelVoltage, self.band_low, self.band_high, self.sample_rate, self.order_filter)      		
    		
            # window data
            windowed = channelVoltage * signal.blackmanharris(dataLengthSamples)
            #windowed = channelVoltage * signal.gaussian(dataLengthSamples, std=8,sym=False)
            
            # compute fft
            amp = abs(scipy.fftpack.rfft(channelVoltage,fftLengthSamples))
            freqs = scipy.fftpack.rfftfreq(fftLengthSamples,sampleSpacing)


            # true_maxAmplitudeIndex and true_maxFreq causes divid by 0 exception sometimes so they are commented out

            # find peak frequency
            maxAmplitudeIndex = np.argmax(amp)
            # true_maxAmplitudeIndex = parabolic(np.log(amp), maxAmplitudeIndex)[0]
            maxFreq = nyq * maxAmplitudeIndex / fftLengthSamples
            # true_maxFreq = nyq * true_maxAmplitudeIndex / fftLengthSamples

            # print('Channel '+str(channelIndex+1)+':     '+str(true_maxFreq)+'  '+str(maxFreq))
            print('Channel '+str(channelIndex+1)+':     '+str(maxFreq))

            # save sample to dataPerSampleRate
            dataPerSampleRate.append(maxFreq)    

            # do not run this cuz you are gonna get bombarded with plots
            # self.plot(channelIndex, channelVoltage, freqs, amp, maxAmplitudeIndex)

        # append dataPerSampleRate as column to the peak_alpha_freq array
        self.peak_alpha_freq = np.c_[ self.peak_alpha_freq, dataPerSampleRate] 
        # print self.peak_alpha_freq



    def butter_bandpass_filter(self, mydata, lowcut, highcut, fs, order=4):
        b, a = self.butter_bandpass(lowcut, highcut, fs, order=order)
        y = sp.signal.filtfilt(b, a, mydata)
        return y


    # butter filter funtion       
    def butter_bandpass(self, lowcut, highcut, fs, order=4):
        """ A helper function of butter_bandpass_filter()
            lowcut is the lower bound of the frequency that we want to isolate
            hicut is the upper bound of the frequency that we want to isolate
            fs is the sampling rate of our data
        """
        nyq = 0.5 * fs #nyquist frequency - see http://www.dspguide.com/ if you want more info
        low = float(lowcut) / nyq
        high = float(highcut) / nyq
        b, a = sp.signal.butter(order, [low, high], btype='band')
        return b, a



    def plot(self, channelIndex, channelVoltage, freqs, amp, maxAmplitudeIndex):
        """ plot the figures """
>>>>>>> b2a20f3a49e13764e9c3139a7b9777bfd304396b
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
        ax2.plot(freqs, np.mean(channelWinSpectra,1))
        # ax2.plot(freqs[maxAmplitudeIndex], amp[maxAmplitudeIndex], 'rD')   # highest frequency marker
        ax2.grid()

<<<<<<< HEAD
    # plt.show()
    print np.median(channelPeaks,1)
    print np.mean(channelPeaks,1)
        
#butter filter funtion         
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
=======
        plt.show()


    def record_peak(self):
        """ recording the peak at the end of the application all at once in pretty printing"""
        # self.recorder.record_raw(self.peak_alpha_freq)
        self.recorder.write(self.peak_alpha_freq)

    # def record_peak_2(self, channelIndex, maxFreq):
    #     """ record maxFreq to txt file"""

    #     # populate peak_alpha_freq
    #     # self.peak_alpha_freq.append(maxFreq)

    #     # testing
    #     print('Channel ' + str(channelIndex+1) + ':     ' + str(maxFreq))

    #     #  output frequency to file
    #     self.recorder.write('Channel ' + str(channelIndex+1) + ':     ' + str(maxFreq)) 


    def output_to_file_before_exit(self):
        """  output alpha peak frequency to file on KeyBoardInterrupt """
        self.record_peak()
        # print 'Saved Data:'
        # print self.peak_alpha_freq
        for clearline in range(1,10):   print('\n')
        print '\nData has been recorded and saved in:   ./recordings/' + str(self.recorder.file_name) + '.txt'
        print '\nTo open the recording file on mac:     open ./recordings/' + str(self.recorder.file_name) + '.txt'
        for clearline in range(1,10):   print('\n')

>>>>>>> b2a20f3a49e13764e9c3139a7b9777bfd304396b

