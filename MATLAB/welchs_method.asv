% frequency parameters
clear
oscCenter1 = 10.52;
oscCenter2 = 10.54;
dataLengthSecs = 25;
sampleRate = 1000;
nyq = sampleRate/2;
dataLengthSamples = dataLengthSecs*sampleRate;
sampleSpacing = 1/sampleRate;
t = 0:sampleSpacing:(dataLengthSecs-sampleSpacing);

osc1 = chan_osc(dataLengthSamples, sampleRate,oscCenter1);
osc2 = chan_osc(dataLengthSamples, sampleRate,oscCenter2);

data = osc1+osc2;
% plot(data);

%% FFT
nfft = 100*sampleRate;
dataX = fft(data,nfft)/dataLengthSamples;
fft_f = linspace(0,nyq,floor(nfft/2)+1);

dataX = dataX(1:length(fft_f)); %keep only positive frequencies

% similar plot as above, but with an x-axis label
plot(fft_f,2*abs(dataX))
ylabel('Amplitude')

%% Welch
windowLengthSamples = 100;
nOverlap = windowLengthSamples/2;
nfft = 100*sampleRate;
% welch_f = linspace(0,nyq,floor(nfft/2)+1);
[pow, welch_f] = pwelch(data,windowLengthSamples,nOverlap,nfft,sampleRate, 'power', 'onesided');
amp = sqrt(pow);
plot(welch_f,pow);

ylabel('Amplitude')

%%Regina
% Find the minimum dataLengthSamples needed to get a resolution of 0.02
% adjust windowLengthSamples, nOverlap, and nfft