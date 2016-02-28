import numpy as np
from matplotlib.pyplot import figure, title, xlabel, ylabel, plot, grid, show, axis, xlim, ylim, xticks, yticks
import oscillation as o
from scipy import signal as sig

def low_pass(input, cut_off_freq = .05, transition_band = 0.08, gain = 1):

    # Filter of length M delays for (M-1)/2 samples

    fc = cut_off_freq  # cutoff frequency as a fraction of the sampling rate (in (0,0.5)).
    b = transition_band  # transition band, as a fraction of the sampling rate (in (0,0.5)).
    g = gain
    N = int(np.ceil(4/b)) # the length of the filter
    print (N)
    if not N % 2: N += 1  # make sure that N is odd
    n = np.arange(N)  # array of N, starts at 0, ends at N-1, increment by 1

    # Compute the sinc filter
    h = np.sinc(2 * fc * (n - (N-1) / 2.))
    # h = np.sinc(2 * fc * (n - (N - 1) / 2.))


    # Compute the Blackman window. Both of the 'w' are exactly the same
    # This is the window in with the sinc function is non-zero.
    # Outside this rage the function is zero. This is so that the convolution is finite
    w1 = np.blackman(N)
    w2 = 0.42 - 0.5 * np.cos(2 * np.pi * n / (N-1)) + \
        0.08 * np.cos(4 * np.pi * n / (N-1))

    # multiply the sinc filter with window to get finite sinc function
    h = h * w1

    # Normalize to get unity gain. Then implement the desired gain
    h = (h / np.sum(h)) * gain

    # finally the convolution that filters the signal
    output = np.convolve(input, h)

    # since there is a delay of filter by N/2, this loop shift the
    # entire filtered signal to the appropriate amount
    for x in range(len(output)):
        length = len(output)
        if x < length - N/2:
           output[x] = output[x + N/2]
        else:
            output[x] = 0
    return output


sampleRate = 512. # this many samples per second
dataLengthSecs = 1 # samples will be collected for this many seconds
dataLengthSamples = dataLengthSecs*sampleRate # this is the total number of samples collected

channelVoltage = o.chan_sin(dataLengthSamples, sampleRate,10)
# channelVoltage2 = o.chan_cos(dataLengthSamples, sampleRate, 11)

# s1 = channelVoltage * channelVoltage2
# s2 = channelVoltage
# s3 = o.chan_sin_noisy(dataLengthSamples,sampleRate,12)
# s4 = o.chan_cos
# s4 = -sc.fft(s1)
# s5 = s3 * s1 * s2

# temp1 = low_pass(s1, cut_off_freq= .4, transition_band=.01)
# filt2 = low_pass(s2, transition_band=.01, cut_off_freq=.0097)
# temp3 = low_pass(s3, cut_off_freq=.2)
# temp4 = low_pass(channelVoltage)
# temp5 = low_pass(s5)


# figure("Low Pass")
# plot(s5)
# plot(temp5,'r')
# plot(s4)
# xticks(np.arange(0,2001,200))
# plot(temp1,'r')
# plot(s1, 'c')
# plot(filt2, 'r')
# plot(s2, 'c')
# plot(temp3, 'r')
# plot(s3, 'c')
# plot(channelVoltage)
# plot(temp4)
# grid(True)
# show()

# filtered_data = np.convolve(EEGwindow,bp,'same')

## Generate PM FIR filter coefficients
center = 10
lowcut = center-2
highcut = center+2
transition_bw = 0.5
numtaps = 1024
nyq = 0.5 * sampleRate #nyquist frequency - see http://www.dspguide.com/ if you want more info
bp = sig.remez(numtaps,[0, lowcut - transition_bw, lowcut, highcut, highcut + transition_bw, nyq],[0, 1, 0], Hz=sampleRate, type='bandpass') # FIR
# print ('# of coeffs:', len(bp))
# print ('Filter order:', numtaps)

## Check frequency response
w,h = sig.freqz(bp,1)
# figure
# plot(w*nyq/np.pi, 20*np.log10(abs(h)))
# show()
# delaysamples = 0.5*(len(bp) - 1.) # in samples
# delaysecs = 0.5*(len(bp) - 1.)/srate
# padlength = round(delaysamples)
# EEGtimes = np.linspace(0.0,float(nsamples+padlength)/srate, num=nsamples+padlength)*1000.0
# EEGsectimes = np.linspace(0.0,float(nsamples)/srate, num=nsamples)

	## Check frequency response
		# w,h = sig.freqz(bp,1)
		# figure
		# plot(w*nyq/np.pi, 20*np.log10(abs(h)))
		# show()
