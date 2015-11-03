clear all
clf
%% generate sin wave
nSeconds = 120;
sampleRate = 64;
samples = 1:sampleRate*nSeconds;
alpha_p2p = 5; % microvolts
alpha_amp = alpha_p2p/2;
alpha_freq = 10; % hertz

neuralNoise = noise(sampleRate*nSeconds, 1, sampleRate);
EEG.data = (alpha_amp)*sin(2*pi*alpha_freq*samples/sampleRate) + neuralNoise; % in microvolts
plot(samples/sampleRate,EEG.data);
ylabel('Microvolts');xlabel('Time (sec)');

figure; [spectra, freqs] = spectopo(EEG.data, 0, sampleRate);