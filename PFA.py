import pylab
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack
import random
import time
import math



# voltage = matrix[numOfChannel,numOfSamplesPerSecond]
def processingPAF(voltageSamples):
    # Number of samplepoints
    numOfChannel = voltageSamples.shape[0]     # number of channels
    samples = voltageSamples.shape[1]          # sample size

    sampleSpacing = 1.0 / samples       # sample spacing
    t = np.linspace(0.0, samples * sampleSpacing, samples)

    # going through each channel to plot fft result 
    for channelIndex in range(0,numOfChannel):
        # print voltage[channelIndex,:]
        voltage = voltageSamples[channelIndex,:]
        # print voltage.shape

        # 8 zero paddings for higher fft frequency resolution
        fy=scipy.fftpack.fft(voltage, samples * 8)
        # print ('length of fy ', len(fy))
        # finding frequency values for the x axis
        fx_step_size=samples * 1.0 / len(fy)
        nyq=.5 * samples
        total_steps=nyq / fx_step_size
        fx_bins=np.linspace(0, nyq, total_steps)
        # xf = np.linspace(0.0, samples / 2, samples / 2)

        # find peak frequency
        frequencybins = 128# 1 to 16 frequency,  128 is most optimal
        maxAmplitude = np.argmax(abs(fy[0:frequencybins]))
        print('channel: ', channelIndex+1)
        print('max Amplitude: ', abs(fy[maxAmplitude]))
        print('max frequency: ', fx_bins[maxAmplitude])



        # # plot the figures
        # fig=plt.figure(figsize=(12, 9))
        # ax1=fig.add_subplot(211)
        # # ax1.set_title('axes title')
        # ax1.set_xlabel('Time [s]')
        # ax1.set_ylabel('Voltage [V]')
        # ax1.plot(t, voltage)
        # ax1.grid()

        # ax2=fig.add_subplot(212)
        # ax2.set_xlabel('Frequency [Hz]')
        # ax2.set_ylabel('Amplitude')
        # # show to top 128 frequencies
        # ax2.plot(fx_bins[0:128], abs(fy[0:128]))
        # ax2.plot(fx_bins[maxAmplitude], abs(fy[maxAmplitude]), 'rD')   # highest frequency marker
        # ax2.grid()

        # plt.show()


