import numpy as np
import scipy as sp
from scipy import signal
from scipy.signal import butter
import matplotlib.pyplot as plt
import oscillation as o
from matplotlib.pyplot import figure, title, xlabel, ylabel, plot, grid, show, axis, legend, xcorr
from numpy import pi
from sklearn.preprocessing import normalize

fig_count = 1

# frequency modulation parameters
alphaCenter = 14   # Hz the carrier frequency
alphaModFreq = 0.2  # Hz the modulating frequency
alphaFreqDev = 0.01    # Hz of the frequency deviation, BW is 2x this

## the step size has to be large enough to account for the deviation in frequency over time

# generate data to send
sampleRate = 512  #this many samples per second
nyq = sampleRate/2.
numOfChannel = 1
dataLengthSecs = 10 #samples will be collected for this many seconds
dataLengthSamples = dataLengthSecs*sampleRate #this is the total number of samples collected

#channelVoltage = o.chan_sin(dataLengthSamples, sampleRate, alphaCenter)
channelVoltage = o.chan_fm(dataLengthSamples, sampleRate, alphaCenter, alphaModFreq, alphaFreqDev)
#channelVoltage = o.chan_fm_noisy(dataLengthSamples, sampleRate, alphaCenter, alphaModFreq, alphaFreqDev, snr=10)
figure(fig_count)
fig_count += 1
#plot((channelVoltage-np.mean(channelVoltage)), 'b')
#plot(channelVoltage, label='Input')
#channelVoltage = o.chirp_fun(dataLengthSamples, sampleRate, 12,18)
actual_freq = o.chan_fm_freq(dataLengthSamples, sampleRate, alphaCenter, alphaModFreq, alphaFreqDev)

filteredPhaseDiff = np.zeros(dataLengthSamples)
scaledFilteredPhaseDiff = np.zeros(dataLengthSamples)
unfilteredPhaseDiff = np.zeros(dataLengthSamples)
udd = np.zeros(dataLengthSamples)
phi = np.zeros(dataLengthSamples)
SCO = np.zeros(dataLengthSamples)
ufb = np.zeros(dataLengthSamples)
#order = 12
#b, a = sp.signal.butter(order, alphaModFreq/nyq, btype='low')
#w,h = signal.freqz(b,a)

order = 4
b, a = sp.signal.bessel(order, alphaModFreq*4/nyq, btype='low')
w,h = signal.freqz(b,a)

#order = sampleRate
#stopfreq = alphaModFreq/nyq
#b = signal.firwin(order, stopfreq)
#w,h = signal.freqz(b)

#order = sampleRate*2
#stopfreq = alphaCenter+alphaCenter/4.
#print stopfreq
#b = sp.signal.remez(order,[0, alphaCenter, stopfreq, sampleRate/2],[1,0], Hz=sampleRate) # FIR
#w,h = signal.freqz(b)
#print b
delaysamples = 0.5*(len(b) - 1.) # in samples
delaysecs = delaysamples/sampleRate
print delaysamples
#padlength = round(delaysamples)

figure(fig_count)
fig_count += 1
plt.plot(0.5*sampleRate*w/np.pi,abs(h))
plt.ylabel('Amplitude [dB]', color='b')
plt.xlabel('Frequency [Hz]')

figure(fig_count)
fig_count += 1

plt.plot(0.5*sampleRate*w[1:]/np.pi,-np.diff(np.unwrap(np.angle(h)))/np.diff(w))
plt.ylabel('Group Delay [seconds]', color='b')
plt.xlabel('Frequency [Hz]')


print 'b=',b, ' len=',len(b)
#print 'a=',a, ' len=',len(a)
chunkSize = order+1


gains = np.logspace(-5.0, 5.0, num=1)
gain_errors = np.zeros(len(gains))
#for gainIndex in range(len(gains)):
for gainIndex in range(1):
    print gainIndex
    gain = gains[gainIndex]
    for sampleInd in range(chunkSize+1,dataLengthSamples-1):
        unfilteredPhaseDiff[sampleInd] = channelVoltage[sampleInd]*SCO[sampleInd] # phase difference of reference vs. signal
       
        #filter the multiplied signals
        fac = 1
        gain = 0.001
        unfilteredPhase_chunk = unfilteredPhaseDiff[sampleInd:sampleInd-chunkSize:-1] # chunk of unfiltered phase difference
        filteredPhase_chunk = filteredPhaseDiff[sampleInd-1:sampleInd-chunkSize:-1] # chunk of filtered phase difference
        dotted_unfilteredPhase_chunk = np.dot(b,unfilteredPhase_chunk) # convolve b coeffs with currenta and prev unfiltered data
        dotted_filteredPhase_chunk = np.dot(a[1:],filteredPhase_chunk) # convolve a coeffs with prev filtered data
        filteredPhaseDiff[sampleInd] = (dotted_unfilteredPhase_chunk-dotted_filteredPhase_chunk)/fac # identify current filtered sample
        #filteredPhaseDiff[sampleInd] = dotted_unfilteredPhase_chunk
        # Applying IIR filter forward and backward is impossible

        w0 = (alphaCenter)*2*np.pi # best guess as to what freq of SCO is/should be
        Ts = 1./sampleRate

        phi[sampleInd+1]=phi[sampleInd]+w0*Ts+scaledFilteredPhaseDiff[sampleInd] # phase of software controlled oscillator (SCO)
        
        if(phi[sampleInd+1]>np.pi):
            phi[sampleInd+1] = (phi[sampleInd+1]-(2*np.pi))

        # Store SCO (software controled oscillator)
        SCO[sampleInd+1]=np.sin(phi[sampleInd+1])

        # Feedback
        #gain = 0.005
        #Kn = gain
        #ufb[sampleInd+1]=gain*np.sin(Kn*phi[sampleInd+1])
        #ufb[sampleInd+1]=np.sin(Kn*phi[sampleInd+1])
    
    gain_errors[gainIndex] = np.var(channelVoltage-SCO)
print(gain_errors)
print gains


# Input
figure(fig_count)
fig_count += 1
#plot((channelVoltage-np.mean(channelVoltage)), 'b')
plot(channelVoltage, label='Input')

#plot((actual_freq-np.mean(actual_freq)), 'g')
#title('Input Signal and Frequency of Signal')
legend(loc='lower right')

# Phase differences
figure(fig_count)
title('Phase differences')
fig_count += 1
plot(unfilteredPhaseDiff, 'g', label='Unfiltered Phase Diff') # unfiltered phase difference
plot(filteredPhaseDiff, 'r', label='Filtered Phase Diff') # filtered phase difference
title('Phase difference')
legend(loc='lower right')

# Filtered phase difference, relative amplitude of filtered phase diff to SCO phase step size
figure(fig_count)
title('Filtered phase difference')
fig_count += 1
#plot(filteredPhaseDiff/(w0*Ts*2*pi), 'b')
plot((filteredPhaseDiff[1000:]-np.mean(filteredPhaseDiff[1000:]))/(w0*Ts*np.pi), 'b', label='Tracked Freq')
plot((actual_freq[1000:]-np.mean(actual_freq[1000:])), 'g', label='Actual Freq')
legend(loc='lower right')

figure(fig_count)
fig_count += 1
c = np.correlate(filteredPhaseDiff[1000:]-np.mean(filteredPhaseDiff[1000:]), actual_freq[1000:]-np.mean(actual_freq[1000:]), 'same')
plot(c)
#print "peak correlation occurs at:", range(0,dataLengthSamples-1000)[np.argmax(c)]  # -2.02925731433
#print np.corrcoef(filteredPhaseDiff,actual_freq)



# FFT of phase diff
figure(fig_count)
title('FFT of phase diff')
fig_count += 1
f,psd_unfilteredPhaseDiff = sp.signal.welch(unfilteredPhaseDiff, fs=sampleRate, window='hanning', nperseg=1024., nfft=2048, detrend='linear', return_onesided=True, scaling='density')
f,psd_filteredPhaseDiff = sp.signal.welch(filteredPhaseDiff, fs=sampleRate, window='hanning', nperseg=1024., nfft=2048, detrend='linear', return_onesided=True, scaling='density')
plot(f,psd_unfilteredPhaseDiff, 'b', label='Unfiltered')
plot(f,psd_filteredPhaseDiff, 'r', label='Filtered')
legend(loc='lower right')

# Test SCO vs Signal
figure(fig_count)
fig_count += 1
plot(channelVoltage, label='Input')
plot(SCO, 'r', label='SCO')
title('SCO vs Input Signal')
legend(loc='lower right')

# Test SCO vs Signal
#figure(fig_count)
#fig_count += 1
#plot(channelVoltage-SCO)
#title('SCO minus Signal')

# Phase of SCO
#figure(fig_count)
#fig_count += 1
#plot(phi)
#title('Phase of SCO')

# Feedback
#figure(fig_count)
#fig_count += 1
#plot(ufb)
#title('Feedback')

grid(True)
show()

# figure(3)
# plot(mult_array)
# plot(channelVoltage,'r')
# plot(ref_array, 'g')
# # plot(multiplied, 'g')
# # plot(filter_multiplied, 'k')
# grid(True)
# title('Input signal & Output signal of VCO')
# xlabel('Samples')
# ylabel('Amplitude')
# show()



"""

reg1 = 0 # track the phase
reg2 = 0
reg3 = 0

eta = np.sqrt(2)/2.0           # constant - used to change the gain
theta =2.0*pi*1.0/100.0        # play around with it - used to change the gain

# Kp and Ki are two parameters about second-order filter.
# you can find the ralation between KP Ki and aquisition bandwidth in gardner's book
Kp = (4.0*eta*theta)/(1.0+2.0*eta*theta+theta**2.0) # gain
Ki = (4.0*theta**2.0)/(1.0+2.0*eta*theta+theta**2.0) # gain

# We don't need d_phi_1 because it is used to generate sig1 or the input
# signal, we will just use the voltage sample collected
T = 20.0    # T is the period
d_phi_1 = 1.0/T    # d_phi_1 is the frequency because it is 1/period


dataLengthSamples = 100    #number of data


phi1_reg = np.zeros(dataLengthSamples)  # Store the phase of signal 1
phi2_reg = np.zeros(dataLengthSamples)  # Store the phase of signal 2

phi_error_reg = np.zeros(dataLengthSamples) # Store the phase error between the two signal

reg1_reg = np.zeros(dataLengthSamples)  # array that tracks the phase
reg2_reg = np.zeros(dataLengthSamples)  # array that tracks the phase

s1_reg = np.zeros(dataLengthSamples)    # Stores the signal 1 voltage, only the real part (This is the input)
s2_reg = np.zeros(dataLengthSamples)    # Stores the signal 2 voltage, only the real part (modulated voltage)

s1_reg_imag = np.zeros(dataLengthSamples)    # Stores the signal 1 voltage, only the imaginary part (This is the input)
s2_reg_imag = np.zeros(dataLengthSamples)    # Stores the signal 2 voltage, only the imaginary part (modulated voltage)

for dataPoint in range(dataLengthSamples):


    phi1 = reg1 + d_phi_1
    phi1_reg[dataPoint] = phi1   # Store the phase of signal 1


    s1 = np.exp(1j*2.0*pi*reg1) # generating the signal 1 and 2 voltage (This is the input)
    s2 = np.exp(1j*2.0*pi*reg2)
    # print (s2)

    s1_reg[dataPoint] =s1.real   # Store signal 1 and 2
    s2_reg[dataPoint] =s2.real

    s1_reg_imag[dataPoint] =s1.imag   # Store signal 1 and 2
    s2_reg_imag[dataPoint] =s2.imag

    # print "s1 = " + str(s1)
    # print "s2 = " + str(s2)
    # print "channelVoltage = " + str(channelVoltage[dataPoint])

    t = s1 * s2.conj()   # Detecting the phase by multiplying two sinusoids
    # print (s2.conj())
    # t = channelVoltage[dataPoint] * s2

    # print "complex_t = " + str(t)
    # print "real_t = " + str(real_t) + "\n"


    phi_error = np.arctan(t.imag/t.real)/(2.0*pi) # finding phase error
    phi_error_reg[dataPoint] = phi_error    # store the phase error

    sum1 = Kp*phi_error + phi_error*Ki+reg3

    reg1_reg[dataPoint] =reg1
    reg2_reg[dataPoint] = reg2
    reg1 =phi1

    reg2=reg2+sum1
    reg3 =reg3+phi_error*Ki


    phi2_reg[dataPoint] =reg2



"""



# figure(1)
# title('phase plot')
# xlabel('Samples')
# ylabel('Phase')
# plot(phi1_reg, 'r') # phase of the input signal
# plot(phi2_reg, 'b') #phase of the estimated signal
# grid(True)
# show()

# figure(2)
# plot(phi_error_reg)
# title('phase Error of phase detector')
# grid(True)
# xlabel('samples(n)')
# ylabel('Phase error(degrees)')
# show()


# figure(3)
# plot(s1_reg_imag)
# plot(s2_reg_imag,'r')
# # plot(s1_reg.real, 'g')
# # plot(s2_reg.real,'k')
# grid(True)
# title('Input signal & Output signal of VCO')
# xlabel('Samples')
# ylabel('Amplitude')
# show()


# figure(3)
# plot(s1_reg.real)
# plot(channelVoltage,'r')
# grid(True)
# title('Input signal & Output signal of VCO')
# xlabel('Samples')
# ylabel('Amplitude')
# show()



# axis([0 dataLengthSamples -1.1 1.1])
