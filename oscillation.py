import scipy as sp
import numpy as np

def fm_noisy(dataLengthSamples, sampleRate, oscCenter, oscModFreq, oscFreqDev, oscMean = 0, snr = 5, noiseMean = 0, noiseStdDev = 0.5, samplingNoiseAmp = 0.5): 
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

def fm(dataLengthSamples, sampleRate, oscCenter, oscModFreq, oscFreqDev, oscAmp = 1): 
    sampleSpacing = 1.0 / sampleRate
    dataLengthSecs = dataLengthSamples/sampleRate
    t = np.arange(0,dataLengthSecs,sampleSpacing)      
    h = oscFreqDev/oscModFreq # Modulation index, < 1 narrowband, > 1 wideband
    osc = oscAmp*np.sin( oscCenter  * 2.0 * np.pi * t + oscFreqDev*np.sin(2 * np.pi * oscModFreq * t) / oscModFreq)
    voltageSamples = np.reshape(osc, ((dataLengthSamples,)))
    return voltageSamples

def sin_noisy(dataLengthSamples, sampleRate, oscCenter, oscMean = 0, snr = 5, noiseMean = 0, noiseStdDev = 0.5, samplingNoiseAmp = 0.5): 
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

def sin(dataLengthSamples, sampleRate, oscCenter, oscAmp = 1): 
    sampleSpacing = 1.0 / sampleRate
    dataLengthSecs = dataLengthSamples/sampleRate
    t = np.arange(0,dataLengthSecs,sampleSpacing)      
    osc = oscAmp * np.sin(oscCenter * 2.0 * np.pi * t)
    voltageSamples = np.reshape(osc, ((dataLengthSamples,)))
    return voltageSamples

def make_chunk_of_channelXsample_data():
    return
    
def make_chunk_of_channelXsample_data_with_spatially_distributed_oscillation():
    return