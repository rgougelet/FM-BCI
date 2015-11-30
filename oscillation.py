import scipy as sp
import numpy as np

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
    osc = oscAmp*np.sin( oscCenter  * 2.0 * np.pi * t + oscFreqDev*np.sin(2 * np.pi * oscModFreq * t) / oscModFreq)

    # Oscillation + 1/f noise + additional random noise
    voltageSamples = osc + pinkNoise + samplingNoiseAmp * np.random.random([1,dataLengthSamples])  
    voltageSamples = np.reshape(voltageSamples, ((dataLengthSamples,)))
    return voltageSamples

def chan_fm(dataLengthSamples, sampleRate, oscCenter, oscModFreq, oscFreqDev, oscAmp = 1): 
    sampleSpacing = 1.0 / sampleRate
    dataLengthSecs = dataLengthSamples/sampleRate
    t = np.arange(0,dataLengthSecs,sampleSpacing)      
    h = oscFreqDev/oscModFreq # Modulation index, < 1 narrowband, > 1 wideband
    osc = oscAmp*np.sin( oscCenter  * 2.0 * np.pi * t + oscFreqDev*np.sin(2 * np.pi * oscModFreq * t) / oscModFreq)
    voltageSamples = np.reshape(osc, ((dataLengthSamples,)))
    return voltageSamples

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
    osc = oscAmp * np.sin(oscCenter * 2.0 * np.pi * t)
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
    osc = oscAmp*np.sin( oscCenter  * 2.0 * np.pi * t + oscFreqDev*np.sin(2 * np.pi * oscModFreq * t) / oscModFreq)

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
    osc = oscAmp * np.sin(oscCenter * 2.0 * np.pi * t)

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