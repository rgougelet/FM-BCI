import numpy as np
from numpy import pi
from scipy.signal import chirp, sawtooth
from matplotlib.pyplot import figure, title, xlabel, ylabel, plot, grid, show, axis
import random

def chirp_fun(startFreq = 2.5, endFreq = 15, startTime = 0, endTime = 10., sampleRate = 512, oscAmp = 1, method = \
    'logarithmic' ):
    if (startFreq <= 0) and (method == 'hyperbolic' or method == 'logarithmic'):
        print("Starting Frequency must by non-zero!!")
        return 1
    dataLengthSecs = endTime - startTime
    dataLengthSamples = sampleRate * dataLengthSecs #number of samples
    t = np.linspace(startTime, endTime, dataLengthSamples) #start, stop, number of samples within the interval
    voltageSamples = oscAmp * chirp(t, startFreq, endTime, endFreq, method) #method: 'linear' 'quadratic'
    # 'hyperbolic'
    # 'logarithmic'
    return voltageSamples

def sawtooth_fun(sampleRate = 512., startTime = 0., endTime= 10., oscAmp = 1, phase = 0):
    # period = sampleRate
    dataLengthSecs = endTime - startTime #number of waves
    dataLengthSamples = sampleRate * dataLengthSecs #number of samples
    t = np.linspace(startTime,endTime, dataLengthSamples)
    voltageSamples = oscAmp * sawtooth(2*pi*t + phase)
    return voltageSamples

def rand_sin(startFreq, endFreq, dataLengthSamples = 512, oscAmp = 1, phase = 0):
    freqArr = np.zeros(dataLengthSamples)
    for x in range(0,dataLengthSamples):
        freq = random.uniform(startFreq,endFreq)
        freqArr[x] = freq
    osc = oscAmp * np.sin(freqArr*2*pi*10 + phase)
    voltageSamples = np.reshape(osc,dataLengthSamples)
    return voltageSamples

def randfm_sin(startFreq, endFreq, dataLengthSecs, sampleRate, oscAmp = 1, phase = 0):
    dataLengthSamples = sampleRate * dataLengthSecs
    sampleSpacing = 1.0/sampleRate
    freqArr = np.zeros(dataLengthSecs)
    osc = np.zeros(dataLengthSamples)
    t = np.arange(0,dataLengthSecs,sampleSpacing)
    for x in range(0,dataLengthSecs):
        rand = random.random()
        if rand < 0.5:
            freq = random.uniform(startFreq,endFreq/2)
            freqArr[x] = freq
        elif rand >= 0.5:
            freq = random.uniform(endFreq/2,endFreq)
            freqArr[x] = freq
    for x in range(1,dataLengthSecs+1):
        for y in range((x-1)*sampleRate,x*sampleRate):
            osc[y] = np.sin(freqArr[x-1]*2*pi*t[y] + phase)
    voltageSamples = oscAmp * np.reshape(osc, dataLengthSamples)
    return voltageSamples

def squ_fun(dataLengthSecs, sampleRate, oscAmp = 1):
    dataLengthSamples = dataLengthSecs * sampleRate
    osc = np.zeros(dataLengthSamples)
    for x in range(1,dataLengthSecs+1):
        for y in range((x-1)*sampleRate, x*sampleRate):
            if x%2 == 1:
                osc[y] = oscAmp
            else:
                osc[y] = -1*oscAmp
    return osc


y = randfm_sin(2,15,4,512)
figure(1)
plot(y)
grid(True)
show()
