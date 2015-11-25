import oscillation

def fm_noisy(dataLengthSamples, sampleRate, oscCenter = 10, oscModFreq = 0.1, oscFreqDev = 1, //
    noiseMean = 0, noiseStdDev = 0.5, samplingNoiseAmp = 0.5, oscMean = 0): 
    oscillation.fm_noisy(dataLengthSamples, sampleRate, oscCenter, oscModFreq, oscFreqDev, //
    noiseMean, noiseStdDev, samplingNoiseAmp, oscMean)
    
def fm(dataLengthSamples, sampleRate, oscCenter = 10, oscModFreq = 0.1, oscFreqDev = 1, oscAmp = 1): 
    oscillation.fm(dataLengthSamples, sampleRate, oscCenter, oscModFreq, oscFreqDev, oscAmp)
    
def sin_noisy(dataLengthSamples, sampleRate, noiseMean = 0, noiseStdDev = 0.5, samplingNoiseAmp = 0.5, oscMean = 0): 
    oscillation.sin_noisy(dataLengthSamples, sampleRate, noiseMean, noiseStdDev, samplingNoiseAmp, oscMean)
    
def sin(dataLengthSamples, sampleRate, oscAmp):
    oscillation.sin(dataLengthSamples, sampleRate, oscAmp)