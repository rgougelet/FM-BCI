#here are some common modules:
import scipy as sp #library of scientific functions
import scipy.io
import scipy.signal as signal
import numpy as np #library of math functions
import pandas as pd #library of data analysis functions
import matplotlib.pyplot as plt #functions to plot data
import os #This lets python talk to your opperating system to open and save files.
from parabolic import parabolic
import matplotlib.mlab as mlab
from mpl_toolkits.mplot3d import Axes3D


filename = 'emodat.mat' #adjut file name here\n",
filename = os.path.join('../FM-BCI', filename) #adjust filepath
datafile = sp.io.loadmat(filename) #loading filename
#print datafile.keys()
voltageSamples = datafile['data']
#print voltageSamples.shape, len(voltageSamples)

variances = []
means = []
medians = []
standardDeviations = []
for i in range(len(voltageSamples)):
    variances.append(np.var(voltageSamples[i,:]))
    means.append(np.mean(voltageSamples[i,:]))
    medians.append(np.median(voltageSamples[i,:]))
    standardDeviations.append(np.std(voltageSamples[i,:]))

for i in range(len(voltageSamples)):
    print 'Channel', i+1
    print '\\tmean:', means[i]
    print '\\tmedian:', medians[i]
    print '\\tstandard deviation:', standardDeviations[i]
    print '\\tvariance:', np.var(voltageSamples)
    
fig1 = plt.figure(1, figsize=(9,6))
numBins = 50
n, bins, patches = plt.hist(voltageSamples[0],numBins,alpha=0.8)

fig2 = plt.figure(2, figsize=(9,6))
plt.plot(voltageSamples[0])

sampleRate = 512 # sample rate assumed during recording
sampleSpacing = 1.0 / sampleRate # time between samples in seconds
dataLengthSecs = 30 # length of whole recording
dataLengthSamples = dataLengthSecs*sampleRate # length of whole recording in samples

t = np.arange(0,dataLengthSecs,sampleSpacing) # time vector spanning length in seconds, with approp. num of samples
#numOfChannel = voltageSamples.shape[0] # determine number of channels from data, i.e. not predefined
numOfChannel = 8
voltageSamples = np.empty([numOfChannel, dataLengthSamples])

# channel weighting
channelWeights = np.linspace(1,1./numOfChannel,numOfChannel)
#np.random.shuffle(channelWeights)
print 'Channel weights:'
for channelIndex in range(numOfChannel):
	print \"        \"", channelIndex+1, \"   \"", channelWeights[channelIndex]

# frequency modulation parameters
alphaCenter = 10.25   # Hz the carrier frequency
alphaModFreq = 1  # Hz the modulating frequency
alphaFreqDev = 4   # Hz of the frequency deviation

# signal to noise parameters
snr = 2             # signal / noise
noiseMean = 0
noiseStdDev = 0.5
alphaMean = 0
alphaStdDev = abs(np.sqrt(snr*(noiseStdDev**2))) # std of sine wave
alphaAmp = np.sqrt(2)*alphaStdDev
h = alphaFreqDev/alphaModFreq         # Modulation index

# Constructs 1/f noise by iteratively adding normal random noise, effectively the CDF of normal dist.
normalNoise = np.random.normal(noiseMean, noiseStdDev, (1,dataLengthSamples))
pinkNoise = np.cumsum(normalNoise)

# Frequency modulated alpha rhythm, a sinusoidal baseband signal
alpha = alphaAmp*np.sin( alphaCenter  * 2.0 * np.pi * t + alphaFreqDev*np.sin(2 * np.pi * alphaModFreq * t) / alphaModFreq)

# assign the weighted alpha rhythm + 1/f noise + additional random noise to each channel in sample
for channelIndex in range(0,numOfChannel):
	voltageSamples[channelIndex,:] = channelWeights[channelIndex]*alpha + pinkNoise + 0.5*np.random.random([1,dataLengthSamples])
voltageSamples[channelIndex,:] = alpha # change last channel to ground truth alpha

fig3 = plt.figure(3, figsize=(9,6))
    
channelArray = np.vsplit(voltageSamples,1)
for channelIndex in range(0,numOfChannel):
	plt.plot(voltageSamples[channelIndex,1:sampleRate])
	

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

#winLengthSecs = 1 # predefine length of window.
#winLengthSamples = winLengthSecs*sampleRate # length of window in samples
#numOfWindows = int(dataLengthSamples/winLengthSamples) # determine number of windows
#channelPeaks = np.empty([numOfChannel, numOfWindows]) # container for peak frequencies for each channel every second
desiredFreqResolution = 0.1 # predefine resolution of spectrum
#fftLengthSamples = int(sampleRate/desiredFreqResolution)
#nyq = 0.5*sampleRate # maximum possible frequency to measure
#freqs = scipy.fftpack.rfftfreq(fftLengthSamples,sampleSpacing) # retrieve frequency axis

bandLow = 9.5                                # lower alpha band 
bandHigh = 10.5                              # higher alpha band
orderFilter = 4

# Universal FFT parameters
sampleRate = float(sampleRate)
numOfChannel = voltageSamples.shape[0]
dataLengthSamples = voltageSamples.shape[1]
dataLengthSecs = dataLengthSamples / sampleRate
sampleSpacing = 1.0/sampleRate
nyq = 0.5 * sampleRate
fftLengthSamples = int(sampleRate/desiredFreqResolution)
freqs = np.fft.rfftfreq(fftLengthSamples,sampleSpacing)
winLengthSamples = 512
overlapSamples = 0
stepSize = winLengthSamples

medianSpecMat = np.empty([numOfChannel, len(freqs)])
for channelIndex in range(numOfChannel):
	winSpectra = np.empty(len(freqs))
	stepIndex = 0
	stepIndex = 0
	winStart = 0
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
		stepIndex+=1\
	winSpectra = winSpectra.T
	if channelIndex == 0:
		arrayOfAmps = winSpectra
		numOfWindows = stepIndex+1
	else:
		arrayOfAmps= np.dstack([arrayOfAmps, winSpectra])
arrayOfAmps = np.reshape(arrayOfAmps,(numOfChannel,numOfWindows,len(freqs)))


#print np.median(channelPeaks,1)
#print np.mean(channelPeaks,1)


#chPeakVariances = []
#chPeakMeans = []
#chPeakMedians = []
#chPeakStandardDeviations = []
#for i in range(len(channelPeaks)):
#    chPeakVariances.append(np.var(channelPeaks[i,:]))
#    chPeakMeans.append(np.mean(channelPeaks[i,:]))
#   chPeakMedians.append(np.median(channelPeaks[i,:]))
#    chPeakStandardDeviations.append(np.std(channelPeaks[i,:]))


#for i in range(len(channelPeaks)):
#    print 'Channel ' + str(i+1) + ' Peaks'
#    print '\\tmean:', chPeakMeans[i]
#    print '\\tmedian:', chPeakMedians[i]
#    print '\\tstandard deviation:', chPeakStandardDeviations[i]
#    print '\\tvariance:', chPeakVariances[i]


# Do this for all channels, one figure using subplot, each channel with its own subplot
#fig4 = plt.figure(4, figsize=(9,9))
#numBins = 50

#for channelIndex in range(0, numOfChannel):
#    plt.subplot(np.ceil(np.sqrt(numOfChannel)),np.ceil(np.sqrt(numOfChannel)),channelIndex)
#    n, bins, patches = plt.hist(channelPeaks[channelIndex],numBins,alpha=0.8)
#    y = mlab.normpdf( bins, chPeakMeans[channelIndex],chPeakStandardDeviations[channelIndex] )
#    l = plt.plot(bins, y, 'r--', linewidth=2)

#for channelIndex in range(0, numOfChannel):

#n, bins, patches = plt.hist(channelPeaks[7],numBins,alpha=0.8)


# plot amp for each channel
#for each channel
	#for each window\n",
		#plot 3d figure with time on horizontal, freqs on vertical, and winAmp as the fluctuating value
fig5 = plt.figure(5, figsize=(6,6))

#plt.plot(arrayOfAmps[0,1,:])
#plt.show()
#print arrayOfAmps[0][0]
#ax = Axes3D(fig5)
ax = plt.axes(projection='3d')
#for channelIndex in range(0, numOfChannel):
#print np.shape(arrayOfAmps[0])
x = range(0,numOfWindows)
y = freqs
X,Y = np.meshgrid(x,y)
X,Y = X.T,Y.T
print np.shape(X)
print np.shape(Y)
Z = arrayOfAmps[0]
print Z
Z = Z.reshape(Y.shape)
ax.plot_surface(X,Y,Z)
#plt.ylim(0,12)
plt.show()
#for winIndex in range(0, numOfWindows):
	#for lengthOfAmps in range(0, len(freqs)):
		 #   plt.subplot(ceil(sqrt(numOfChannel)),ceil(sqrt(numOfChannel)),lengthOfAmps)
#        ax.plot_surface( arrayOfAmps[0], arrayOfAmps[0][winIndex], arrayOfAmps[0][winIndex][lengthOfAmps] ,  cmap=plt.cm.jet, rstride=1, cstride=1, linewidth=0)

#for zIndex in range(0, len(freqs)):
#   ax.plot(arrayOfAmps[channelIndex][winIndex], arrayOfAmps[channelIndex], arrayOfAmps[channelIndex][winIndex][zIndex])

