close all
[voltageSamples, instAmp, instPhase, instFreq, instNoise] = chan_osc(1000,1000,10, 'isFM', 1, 'oscFreqDev', 4, 'isAM', 1, 'isNoisy', 1);

hold on
plot(voltageSamples)
plot(instAmp)
plot(instPhase)
plot(instFreq)
plot(instNoise)
plot(voltageSamples-instNoise)