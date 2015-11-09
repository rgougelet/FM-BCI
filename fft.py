# import matplotlib.pyplot as plt
# import plotly.plotly as py
# import numpy as np
# # Learn about API authentication here: https://plot.ly/python/getting-started
# # Find your api_key here: https://plot.ly/settings/api

# Fs = 150.0;  # sampling rate
# Ts = 1.0/Fs; # sampling interval
# t = np.arange(0,1,Ts) # time vector

# ff = 5;   # frequency of the signal
# y = np.sin(2*np.pi*ff*t)

# n = len(y) # length of the signal
# k = np.arange(n)
# T = n/Fs
# frq = k/T # two sides frequency range
# frq = frq[range(n/2)] # one side frequency range

# Y = np.fft.fft(y)/n # fft computing and normalization
# Y = Y[range(n/2)]

# fig, ax = plt.subplots(2, 1)
# ax[0].plot(t,y)
# ax[0].set_xlabel('Time')
# ax[0].set_ylabel('Amplitude')
# ax[1].plot(frq,abs(Y),'r') # plotting the spectrum
# ax[1].set_xlabel('Freq (Hz)')
# ax[1].set_ylabel('|Y(freq)|')

# plot_url = py.plot_mpl(fig, filename='mpl-basic-fft')

# fft on signal length 1 second, which is every last seconds for the plot
# applying running mediam


# %matplotlib inline
import pylab
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack
import random


# plt.plot(np.arange(0, 1024)/1024., data[10000:11024])
# plt.ylabel('Voltage (uV)')
# plt.xlabel('Time [s]')
# plt.title('ECoG Signal in Time Domain')

# Number of samplepoints
samples = 256
# sample spacing
sampleSpacing = 1.0 / samples
t = np.linspace(0.0, samples * sampleSpacing, samples)

# voltage simulation 1
sig1 = np.sin(8.0 * 2.0 * np.pi * t)
sig2 = np.sin(12.0 * 2.0 * np.pi * t)
voltage = sig1 + sig2

# voltage simulation 2
fc = 10.  # Hz the carrier frequency
fm = .01  # Hz the modulating frequency
pd = .5  # Hz amplitude of the frequency deviation
# voltage = np.sin(2 * np.pi * fc * t + pd * np.sin(2 * np.pi * fm * t) / fm)

fy=scipy.fftpack.fft(voltage, samples * 8)
# fy=scipy.fftpack.fft(voltage)
print ('length of fy ', len(fy))
# finding frequency values for the x axis
fx_step_size=samples * 1.0 / len(fy)
nyq=.5 * samples
total_steps=nyq / fx_step_size
fx_bins=np.linspace(0, nyq, total_steps)
# xf = np.linspace(0.0, samples / 2, samples / 2)


# print(np.amax(fy))


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
# show frequency ranges from 0 to 100
ax2.plot(fx_bins[0:128], abs(fy[0:128]))
ax2.grid()

plt.show()
