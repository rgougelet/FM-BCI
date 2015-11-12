
# %matplotlib inline
import pylab
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack
import random
import time
import math

# Number of samplepoints
samples = 256
# sample spacing
sampleSpacing = 1.0 / samples
t = np.linspace(0.0, samples * sampleSpacing, samples)

# voltage simulation 1
sig1 = np.sin(8.0 * 2.0 * np.pi * t)   # f = 8, amplitude = 1
sig2 = 2 * np.sin(12.0 * 2.0 * np.pi * t)   # f = 12, amplitue = 2
# voltage = sig1 + sig2

# voltage simulation 2
fc = 10.  # Hz the carrier frequency
fm = .01  # Hz the modulating frequency
pd = .5  # Hz amplitude of the frequency deviation
voltage = np.sin(2 * np.pi * fc * t + pd * np.sin(2 * np.pi * fm * t) / fm)

# 8 zero paddings for higher fft frequency resolution
fy=scipy.fftpack.fft(voltage, samples * 8)
print ('length of fy ', len(fy))
# finding frequency values for the x axis
fx_step_size=samples * 1.0 / len(fy)
nyq=.5 * samples
total_steps=nyq / fx_step_size
fx_bins=np.linspace(0, nyq, total_steps)
# xf = np.linspace(0.0, samples / 2, samples / 2)

# find peak frequency
maxAmplitude = np.argmax(abs(fy[0:128]))
print('max Amplitude: ', abs(fy[maxAmplitude]))
print('max frequency: ', fx_bins[maxAmplitude])



# plot the figures
fig=plt.figure(figsize=(12, 9))
ax1=fig.add_subplot(211)
# ax1.set_title('axes title')
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Voltage [V]')
ax1.plot(t, voltage)
ax1.grid()

ax2=fig.add_subplot(212)
ax2.set_xlabel('Frequency [Hz]')
ax2.set_ylabel('Amplitude')
# show to top 128 frequencies
ax2.plot(fx_bins[0:128], abs(fy[0:128]))
ax2.plot(fx_bins[maxAmplitude], abs(fy[maxAmplitude]), 'rD')   # highest frequency marker
ax2.grid()

plt.show()
