import scipy as sp
import numpy as np


def FM_noisy(dataLengthSamples, sampleRate, alphaCenter, alphaModFreq, alphaFreqDev, noiseMean = 0, noiseStdDev = 0.5, samplingNoiseAmp = 0.5, alphaMean = 0): 
    sampleSpacing = 1.0 / sampleRate                   # time step
    dataLengthSecs = dataLengthSamples/sampleRate      # total time
    t = np.arange(0,dataLengthSecs,sampleSpacing)      

    # signal to noise parameters
    snr = 5                                            # signal / noise 
    alphaStdDev = abs(np.sqrt(snr*(noiseStdDev**2)))   # std of sine wave
    alphaAmp = np.sqrt(2)*alphaStdDev
    h = alphaFreqDev/alphaModFreq         # Modulation index, tells you spread of sidebands < 1, narrowband, > 1 wideband

    # Constructs 1/f noise by taking CDF of normal dist.
    normalNoise = np.random.normal(noiseMean, noiseStdDev, (1,dataLengthSamples))
    pinkNoise = np.cumsum(normalNoise)
    
    # Frequency modulated alpha rhythm, a sinusoidal baseband signal
    alpha = alphaAmp*np.sin( alphaCenter  * 2.0 * np.pi * t + alphaFreqDev*np.sin(2 * np.pi * alphaModFreq * t) / alphaModFreq)

    # Alpha rhythm + 1/f noise + additional random noise
    voltageSamples = alpha + pinkNoise + samplingNoiseAmp * np.random.random([1,dataLengthSamples])  

    voltageSamples = np.reshape(voltageSamples, ((dataLengthSamples,)))
    
    return voltageSamples

def FM(dataLengthSamples, sampleRate, alphaCenter, alphaModFreq, alphaFreqDev, alphaAmp): 
    sampleSpacing = 1.0 / sampleRate                   # time step
    dataLengthSecs = dataLengthSamples/sampleRate      # total time
    t = np.arange(0,dataLengthSecs,sampleSpacing)      

    h = alphaFreqDev/alphaModFreq         # Modulation index, tells you spread of sidebands < 1, narrowband, > 1 wideband
    
    # Frequency modulated alpha rhythm, a sinusoidal baseband signal
    alpha = alphaAmp*np.sin( alphaCenter  * 2.0 * np.pi * t + alphaFreqDev*np.sin(2 * np.pi * alphaModFreq * t) / alphaModFreq)

    voltageSamples = np.reshape(alpha, ((dataLengthSamples,)))
    
    return voltageSamples


def alpha_noisy(dataLengthSamples, sampleRate, noiseMean = 0, noiseStdDev = 0.5, samplingNoiseAmp = 0.5, alphaMean = 0): 
    sampleSpacing = 1.0 / sampleRate                   # time step
    dataLengthSecs = dataLengthSamples/sampleRate      # total time
    t = np.arange(0,dataLengthSecs,sampleSpacing)      

    # signal to noise parameters
    snr = 5                                            # signal / noise 
    alphaStdDev = abs(np.sqrt(snr*(noiseStdDev**2)))   # std of sine wave
    alphaAmp = np.sqrt(2)*alphaStdDev
    
    # Constructs 1/f noise by taking CDF of normal dist.
    normalNoise = np.random.normal(noiseMean, noiseStdDev, (1,dataLengthSamples))
    pinkNoise = np.cumsum(normalNoise)
    
    # Frequency modulated alpha rhythm, a sinusoidal baseband signal
    alpha = alphaAmp * np.sin(2.0 * np.pi * t)

    # Alpha rhythm + 1/f noise + additional random noise
    voltageSamples = alpha + pinkNoise + samplingNoiseAmp * np.random.random([1,dataLengthSamples])  
    voltageSamples = np.reshape(voltageSamples, ((dataLengthSamples,)))
    
    return voltageSamples


def alpha(dataLengthSamples, sampleRate, alphaAmp): 
    sampleSpacing = 1.0 / sampleRate                   # time step
    dataLengthSecs = dataLengthSamples/sampleRate      # total time
    t = np.arange(0,dataLengthSecs,sampleSpacing)      

    # Frequency modulated alpha rhythm, a sinusoidal baseband signal
    alpha = alphaAmp * np.sin(2.0 * np.pi * t)
    
    voltageSamples = np.reshape(alpha, ((dataLengthSamples,)))
    
    return voltageSamples
