% mikexcohen@gmail.com

%% TF of many trials


% frequency parameters
oscCenter = 10;
oscFreqDev = 0.04;
dataLengthSamples = 200;%10000
sampleRate = 100;
oscModFreq = 0.02;%0.02
nTrials=1;


min_freq = 8;  %generally interested in 2-50 hz 
max_freq = 12;



%only change below 
num_frex = 40;%change it 
frex = linspace(min_freq,max_freq,num_frex);


% other wavelet parameters
range_cycles = 2;%change it 

%s = logspace(log10(range_cycles(1)),log10(range_cycles(end)),num_frex) ./ (2*pi*frex);
s = logspace(log10(range_cycles),log10(range_cycles),num_frex) ./ (2*pi*frex);
wavtime = -0.1:1/sampleRate:0.1;%change it longer wavelet time, higher freq resolution, poorer time resolution
half_wave = (length(wavtime)-1)/2;


% FFT parameters
nWave = length(wavtime);
nData = dataLengthSamples;
nConv = nWave + nData - 1;

% initialize output time-frequency data
tf = zeros(length(frex),dataLengthSamples);

% loop over frequencies
%{
for fi=1:length(frex)
    
    % create wavelet and get its FFT
    % the wavelet doesn't change on each trial...
    wavelet  = exp(2*1i*pi*frex(fi).*wavtime) .* exp(-wavtime.^2./(2*s(fi)^2));
    waveletX = fft(wavelet,nConv);
    waveletX = waveletX ./ max(waveletX);
    
        %dataX = fft(chan_osc(dataLengthSamples, sampleRate,oscCenter ,'isFM',1,'oscModFreq',oscModFreq,'oscFreqDev',oscFreqDev), nConv);
        dataX = fft(chan_osc(dataLengthSamples, sampleRate,oscCenter),nConv);
        % run convolution
        as = ifft(waveletX .* dataX);
        as = as(half_wave+1:end-half_wave);
     % put power data into big matrix
        tf(fi,:) = abs(as).^2;
    
        end
        %}



% other wavelet parameters
frex = linspace(min_freq,max_freq,num_frex);
time = -2:1/EEG.srate:2;
half_wave = (length(time)-1)/2;

% FFT parameters
nKern = length(time);
nData = EEG.pnts*EEG.trials;
nConv = nKern+nData-1;

% initialize output time-frequency data
tf = zeros(length(num_cycles),length(frex),EEG.pnts);

% convert baseline time into indices
[~,baseidx(1)] = min(abs(EEG.times-baseline_window(1)));
[~,baseidx(2)] = min(abs(EEG.times-baseline_window(2)));


% FFT of data (doesn't change on frequency iteration)
dataX = fft(reshape(EEG.data(strcmpi(channel2use,{EEG.chanlocs.labels}),:,:),1,[]),nConv);

% loop over cycles
for cyclei=1:length(num_cycles)
    
    for fi=1:length(frex)
        
        % create wavelet and get its FFT
        s = num_cycles(cyclei)/(2*pi*frex(fi));
        
        cmw  = exp(2*1i*pi*frex(fi).*time) .* exp(-time.^2./(2*s^2));
        cmwX = fft(cmw,nConv);
        cmwX = cmwX./max(cmwX);
        
        % run convolution, trim edges, and reshape to 2D (time X trials)
        as= ifft(cmwX.* dataX);
        half_wav = floor( length(cmw)/2 )+1;
        as=as(half_wav-1:end-half_wav);
        as=reshape(as,[EEG.pnts,EEG.trials]);
        
        % put power data into big matrix
        tf(cyclei,fi,:) = mean(abs(as).^2,2);
    end
    
    % db conversion
    tf(cyclei,:,:) = 10*log10( bsxfun(@rdivide, squeeze(tf(cyclei,:,:)), mean(tf(cyclei,:,baseidx(1):baseidx(2)),3)' ) );
    
end

% plot results
figure(3), clf
for cyclei=1:length(num_cycles)
    subplot(2,2,cyclei)
    
    contourf(EEG.times,frex,squeeze(tf(cyclei,:,:)),40,'linecolor','none')
    set(gca,'clim',[-3 3],'ydir','normal','xlim',[-300 1000])
    title([ 'Wavelet with ' num2str(num_cycles(cyclei)) ' cycles' ])
    xlabel('Time (ms)'), ylabel('Frequency (Hz)')
end

sampleSpacing = 1/sampleRate;
    dataLengthSecs = dataLengthSamples/sampleRate;
    t = 0:sampleSpacing:(dataLengthSecs-sampleSpacing);
    
% plot results
figure(1), clf
contourf(t,frex,tf,40,'linecolor','none')
%set(gca,'clim',[0 5],'ydir','normal','xlim',[-300 1000])

