% frequency parameters
clear
close all


welch_dls = 5;
med_welch_dls = 5;
pll_dls = 5;
music_dls = 5;
espirit_dls = 5;
max_ent_dls = 5;
burg_dls = 5;
spec_env_dls = 5;

oscCenter1 = 10.52;
oscCenter2 = 10.54;
sampleRate = 1000;
nyq = sampleRate/2;
sampleSpacing = 1/sampleRate;



% plot(data);

%% FFT
figure;
for fft_dls = 45:100; % Approximately 50sec
    dataLengthSecs = fft_dls;
    dataLengthSamples = dataLengthSecs*sampleRate;
    osc1 = chan_osc(dataLengthSamples, sampleRate,oscCenter1);
    osc2 = chan_osc(dataLengthSamples, sampleRate,oscCenter2);
    data = osc1+osc2;
    t = 0:sampleSpacing:(dataLengthSecs-sampleSpacing);

    tic
    nfft = 100*sampleRate;
    dataX = fft(data,nfft)/dataLengthSamples;
    fft_f = linspace(0,nyq,floor(nfft/2)+1);
    dataX = dataX(1:length(fft_f)); %keep only positive frequencies
    fft_rt = toc;

    plot(fft_f,2*abs(dataX))
    xlim([10.5 10.56])
    ylabel('Amplitude')
    title(['Data Length = ', num2str(fft_dls),' sec'])
    pause(0.5)
end

%% Welch
figure;
for welch_dls = 150; % Approximately 50sec
    dataLengthSecs = welch_dls;
    osc1 = chan_osc(dataLengthSamples, sampleRate,oscCenter1);
    osc2 = chan_osc(dataLengthSamples, sampleRate,oscCenter2);
    data = osc1+osc2;
    
    tic
    windowLengthSecs = 75;
    windowLengthSamples = windowLengthSecs*sampleRate;
    overlapSecs = 0;
    nOverlap = overlapSecs*sampleRate;
    nfft = 100*sampleRate;
    % welch_f = linspace(0,nyq,floor(nfft/2)+1);
    [pow, welch_f] = pwelch(data,windowLengthSamples,nOverlap,nfft,sampleRate, 'power', 'onesided');
    amp = sqrt(pow);
    welch_rt = toc;

    plot(welch_f,amp);
    xlim([10.5 10.56])
    ylabel('Amplitude')
    title(['Data Length = ', num2str(welch_dls),' sec'])
    pause(0.25)
end
%%Regina
% Find the minimum dataLengthSamples needed to get a resolution of 0.02
% adjust windowLengthSamples, nOverlap, and nfft
%%
% pmusic(data,4,nfft,sampleRate)