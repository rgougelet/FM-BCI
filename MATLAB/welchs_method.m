% frequency parameters
oscCenter1 = 10.52;
oscCenter2 = 10.54;
dataLengthSecs = 100;
sampleRate = 1000;
nyq = sampleRate/2;
dataLengthSamples = dataLengthSecs*sampleRate;
sampleSpacing = 1/sampleRate;
t = 0:sampleSpacing:(dataLengthSecs-sampleSpacing);

osc1 = chan_osc(dataLengthSamples, sampleRate,oscCenter1);
osc2 = chan_osc(dataLengthSamples, sampleRate,oscCenter2);

data = osc1+osc2;
plot(data);

%%

windowLengthSamples = 128;
nOverlap = windowLengthSamples/2;
nfft = 256;
f = linspace(0,nyq,(nfft/2)+1);
pxx = pwelch(data,windowLengthSamples,nOverlap,nfft);

plot(f,10*log10(pxx))

ylabel('Magnitude (dB)')

%%Regina
% Find the minimum dataLengthSamples needed to get a resolution of 0.02
% adjust windowLengthSamples, nOverlap, and nfft