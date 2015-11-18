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


