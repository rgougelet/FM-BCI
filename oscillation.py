import scipy as sp
import numpy as np
from numpy import pi
from scipy.signal import chirp, sawtooth
import random

# def chirp_fun(startFreq = 2.5, endFreq = 15, startTime = 0, endTime = 10., sampleRate = 512, oscAmp = 1, method = \
    # 'logarithmic' ):
    # if (startFreq <= 0) and (method == 'hyperbolic' or method == 'logarithmic'):
        # print("Starting Frequency must by non-zero!!")
        # return 1
    # dataLengthSecs = endTime - startTime
    # dataLengthSamples = sampleRate * dataLengthSecs #number of samples
    # t = np.linspace(startTime, endTime, dataLengthSamples) #start, stop, number of samples within the interval
    # voltageSamples = oscAmp * chirp(t, startFreq, endTime, endFreq, method) #method: 'linear' 'quadratic'
    # # 'hyperbolic'
    # # 'logarithmic'
    # return voltageSamples
    
def chirp_fun(dataLengthSamples, sampleRate, startFreq, endFreq, method = 'logarithmic' ):
    sampleSpacing = 1.0 / sampleRate
    dataLengthSecs = dataLengthSamples/sampleRate
    t = np.arange(0,dataLengthSecs,sampleSpacing)
    if (startFreq <= 0) and (method == 'hyperbolic' or method == 'logarithmic'):
        print("Starting Frequency must be positive!!")
        return 1
    
    dataLengthSamples = sampleRate * dataLengthSecs #number of samples
    #t = np.linspace(startTime, endTime, dataLengthSamples) #start, stop, number of samples within the interval
    voltageSamples = chirp(t, startFreq, dataLengthSecs, endFreq, method) #method: 'linear' 'quadratic'
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

def chan_fm_noisy(dataLengthSamples, sampleRate, oscCenter, oscModFreq, oscFreqDev, snr = 5, oscMean = 0, noiseMean = 0, noiseStdDev = 0.5, samplingNoiseAmp = 0.5): 
    sampleSpacing = 1.0 / sampleRate
    dataLengthSecs = dataLengthSamples/sampleRate
    t = np.arange(0,dataLengthSecs,sampleSpacing)      

    # Signal to noise parameters
    oscStdDev = abs(np.sqrt(snr*(noiseStdDev**2)))
    oscAmp = np.sqrt(2)*oscStdDev
    h = oscFreqDev/oscModFreq # Modulation index, < 1 narrowband, > 1 wideband

    # Constructs 1/f noise by taking CDF of normal dist.
    normalNoise = np.random.normal(noiseMean, noiseStdDev, (1,dataLengthSamples))
    pinkNoise = np.cumsum(normalNoise)
    
    # Frequency modulated oscillation, a sinusoidal baseband signal
    osc = oscAmp*np.cos( oscCenter  * 2.0 * np.pi * t + oscFreqDev*np.cos(2 * np.pi * oscModFreq * t) / oscModFreq)

    # Oscillation + 1/f noise + additional random noise
    voltageSamples = osc + pinkNoise + samplingNoiseAmp * np.random.random([1,dataLengthSamples])  
    voltageSamples = np.reshape(voltageSamples, ((dataLengthSamples,)))
    return voltageSamples

def chan_fm(dataLengthSamples, sampleRate, oscCenter, oscModFreq, oscFreqDev, oscAmp = 1):
    #returns FM sin with frequencies between oscCenter-oscFreqDev, oscCenter+oscFreqDev
    sampleSpacing = 1.0 / sampleRate
    dataLengthSecs = dataLengthSamples/sampleRate
    t = np.arange(0,dataLengthSecs,sampleSpacing)      
    h = oscFreqDev/oscModFreq # Modulation index, < 1 narrowband, > 1 wideband
    fc = oscCenter  * 2.0 * np.pi * t
    fm = (oscFreqDev*np.cos(2 * np.pi * oscModFreq * t) / oscModFreq)
    osc = oscAmp*np.cos(fc + fm)
    voltageSamples = np.reshape(osc, ((dataLengthSamples,)))
    return voltageSamples

def chan_fm_phase(dataLengthSamples, sampleRate, oscCenter, oscModFreq, oscFreqDev, oscAmp = 1):
    sampleSpacing = 1.0 / sampleRate
    dataLengthSecs = dataLengthSamples/sampleRate
    t = np.arange(0,dataLengthSecs,sampleSpacing)      
    h = oscFreqDev/oscModFreq # Modulation index, < 1 narrowband, > 1 wideband
    fc = oscCenter  * 2.0 * np.pi * t
    fm = (oscFreqDev*np.cos(2 * np.pi * oscModFreq * t) / oscModFreq)
    osc = oscAmp*np.cos(fc + fm)
    voltageSamples = np.reshape(osc, ((dataLengthSamples,)))
    inst = fc+fm
    phase = ( inst + np.pi) % (2 * np.pi ) - np.pi
    return phase
    
def chan_fm_freq(dataLengthSamples, sampleRate, oscCenter, oscModFreq, oscFreqDev, oscAmp = 1):
    sampleSpacing = 1.0 / sampleRate
    dataLengthSecs = dataLengthSamples/sampleRate
    t = np.arange(0,dataLengthSecs,sampleSpacing)      
    h = oscFreqDev/oscModFreq # Modulation index, < 1 narrowband, > 1 wideband
    fc = oscCenter  * 2.0 * np.pi * t
    fm = (oscFreqDev*np.cos(2 * np.pi * oscModFreq * t) / oscModFreq)
    osc = oscAmp*np.cos(fc + fm)
    voltageSamples = np.reshape(osc, ((dataLengthSamples,)))
    instFreq = sampleRate/(2*np.pi)*np.diff(fc+fm)
    return instFreq
    
def chan_sin_noisy(dataLengthSamples, sampleRate, oscCenter, snr = 5, oscMean = 0, noiseMean = 0, noiseStdDev = 0.5, samplingNoiseAmp = 0.5): 
    sampleSpacing = 1.0 / sampleRate
    dataLengthSecs = dataLengthSamples/sampleRate
    t = np.arange(0,dataLengthSecs,sampleSpacing)      

    # signal to noise parameters
    oscStdDev = abs(np.sqrt(snr*(noiseStdDev**2)))
    oscAmp = np.sqrt(2)*oscStdDev
    
    # Constructs 1/f noise by taking CDF of normal dist.
    normalNoise = np.random.normal(noiseMean, noiseStdDev, (1,dataLengthSamples))
    pinkNoise = np.cumsum(normalNoise)
    
    # Frequency modulated osc rhythm, a sinusoidal baseband signal
    osc = oscAmp * np.sin(oscCenter * 2.0 * np.pi * t)

    # osc rhythm + 1/f noise + additional random noise
    voltageSamples = osc + pinkNoise + samplingNoiseAmp * np.random.random([1,dataLengthSamples])  
    voltageSamples = np.reshape(voltageSamples, ((dataLengthSamples,)))
    
    return voltageSamples


def chan_sin(dataLengthSamples, sampleRate, oscCenter, oscAmp = 1): 
    sampleSpacing = 1.0 / sampleRate
    dataLengthSecs = dataLengthSamples/sampleRate
    t = np.arange(0,dataLengthSecs,sampleSpacing)      
    osc = oscAmp * np.sin(oscCenter * 2.0 * np.pi * t + 3*np.pi/2)
    voltageSamples = np.reshape(osc, ((dataLengthSamples,)))
    return voltageSamples

def chan_cos(dataLengthSamples, sampleRate, oscCenter, oscAmp = 1): 
    sampleSpacing = 1.0 / sampleRate
    dataLengthSecs = dataLengthSamples/sampleRate
    t = np.arange(0,dataLengthSecs,sampleSpacing)      
    osc = oscAmp * np.cos(oscCenter * 2.0 * np.pi * t)
    voltageSamples = np.reshape(osc, ((dataLengthSamples,)))
    return voltageSamples

def fm_noisy(dataShape, sampleRate, oscCenter, oscModFreq, oscFreqDev, snr = 5, oscMean = 0, noiseMean = 0, noiseStdDev = 0.5, samplingNoiseAmp = 0.5): 
    """ dataShape is (numOfChannel, dataLengthSamples) matrix """
    numOfChannel = int(dataShape[0])
    dataLengthSamples = int(dataShape[1])
    sampleSpacing = 1.0 / sampleRate
    dataLengthSecs = dataLengthSamples/sampleRate
    t = np.arange(0,dataLengthSecs,sampleSpacing)      

    # Signal to noise parameters
    oscStdDev = abs(np.sqrt(snr*(noiseStdDev**2)))
    oscAmp = np.sqrt(2)*oscStdDev
    h = oscFreqDev/oscModFreq # Modulation index, < 1 narrowband, > 1 wideband

    # Constructs 1/f noise by taking CDF of normal dist.
    normalNoise = np.random.normal(noiseMean, noiseStdDev, (1,dataLengthSamples))
    pinkNoise = np.cumsum(normalNoise)
    
    # Frequency modulated oscillation, a sinusoidal baseband signal
    osc = oscAmp*np.cos( oscCenter  * 2.0 * np.pi * t + oscFreqDev*np.cos(2 * np.pi * oscModFreq * t) / oscModFreq)

    # Oscillation + 1/f noise + additional random noise
    voltageSamples = osc + pinkNoise + samplingNoiseAmp * np.random.random([1,dataLengthSamples])  
    voltageSamples = np.reshape(voltageSamples, ((dataLengthSamples,)))

    voltageChunk = np.empty([numOfChannel,dataLengthSamples])
    for channelIndex in range(0,numOfChannel):
        voltageChunk[channelIndex,:] = voltageSamples

    return voltageChunk
    

def fm(dataShape, sampleRate, oscCenter, oscModFreq, oscFreqDev, oscAmp = 1):
    """ dataShape is (numOfChannel, dataLengthSamples) matrix """ 
    numOfChannel = int(dataShape[0])
    dataLengthSamples = int(dataShape[1])
    voltageSamples = chan_fm(dataLengthSamples, sampleRate, oscCenter, oscModFreq, oscFreqDev, oscAmp)
    voltageChunk = np.empty([numOfChannel,dataLengthSamples])
    for channelIndex in range(0,numOfChannel):
        voltageChunk[channelIndex,:] = voltageSamples

    return voltageChunk


def sin_noisy(dataShape, sampleRate, oscCenter, oscModFreq, oscFreqDev, snr = 5, oscMean = 0,  noiseMean = 0, noiseStdDev = 0.5, samplingNoiseAmp = 0.5): 
    """ dataShape is (numOfChannel, dataLengthSamples) matrix """
    numOfChannel = int(dataShape[0])
    dataLengthSamples = int(dataShape[1])
    sampleSpacing = 1.0 / sampleRate
    dataLengthSecs = dataLengthSamples/sampleRate
    t = np.arange(0,dataLengthSecs,sampleSpacing)      

    # signal to noise parameters
    oscStdDev = abs(np.sqrt(snr*(noiseStdDev**2)))
    oscAmp = np.sqrt(2)*oscStdDev
    
    # Constructs 1/f noise by taking CDF of normal dist.
    normalNoise = np.random.normal(noiseMean, noiseStdDev, (1,dataLengthSamples))
    pinkNoise = np.cumsum(normalNoise)
    
    # Frequency modulated osc rhythm, a sinusoidal baseband signal
    osc = oscAmp * np.cos(oscCenter * 2.0 * np.pi * t)

    # osc rhythm + 1/f noise + additional random noise
    voltageSamples = osc + pinkNoise + samplingNoiseAmp * np.random.random([1,dataLengthSamples])  
    voltageSamples = np.reshape(voltageSamples, ((dataLengthSamples,)))

    voltageChunk = np.empty([numOfChannel,dataLengthSamples])
    for channelIndex in range(0,numOfChannel):
        voltageChunk[channelIndex,:] = voltageSamples
    
    return voltageChunk


def sin(dataShape, sampleRate, oscCenter, oscAmp = 1): 
    """ dataShape is (numOfChannel, dataLengthSamples) matrix """
    numOfChannel = int(dataShape[0])
    dataLengthSamples = int(dataShape[1])
    voltageSamples = chan_sin(dataLengthSamples, sampleRate, oscCenter, oscAmp)
    voltageChunk = np.empty([numOfChannel,dataLengthSamples])
    for channelIndex in range(0,numOfChannel):
        voltageChunk[channelIndex,:] = voltageSamples
    return voltageChunk


def make_chunk_of_channelXsample_data_with_spatially_distributed_oscillation():
    return