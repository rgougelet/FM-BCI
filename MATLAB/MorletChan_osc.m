% frequency parameters
oscCenter = 10;
oscFreqDev = 0.04;
dataLengthSamples = 10*40;%10000
sampleRate = 40;
oscModFreq = 1;%0.02
nTrials=1;

sampleSpacing = 1/sampleRate;
dataLengthSecs = dataLengthSamples/sampleRate;
t = 0:sampleSpacing:(dataLengthSecs-sampleSpacing);

data = chan_osc(dataLengthSamples, sampleRate,oscCenter ,'isFM',1,'oscModFreq',oscModFreq,'oscFreqDev',oscFreqDev);
% data = chan_osc(dataLengthSamples, sampleRate,oscCenter);

%{
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


for fi=1:length(frex)
    
    % create wavelet and get its FFT
    % the wavelet doesn't change on each trial...
    wavelet  = exp(2*1i*pi*frex(fi).*wavtime) .* exp(-wavtime.^2./(2*s(fi)^2));
    waveletX = fft(wavelet,nConv);
    waveletX = waveletX ./ max(waveletX);
    
        dataX = fft(data,nConv);
        % run convolution
        as = ifft(waveletX .* dataX);
        as = as(half_wave+1:end-half_wave);
     % put power data into big matrix
        tf(fi,:) = abs(as).^2;
    
end


    
% plot results
figure(1), clf
contourf(t,frex,tf,40,'linecolor','none')
%set(gca,'clim',[0 5],'ydir','normal','xlim',[-300 1000])
%}


%% comparing fixed number of wavelet cycles

% wavelet parameters
min_freq =  8;
max_freq = 12;

% other wavelet parameters
frex = linspace(min_freq,max_freq,length(num_cycles));
time = -10:1/sampleRate:10;
half_wave = (length(time)-1)/2;

% set a few different wavelet widths ("number of cycles" parameter)
length_wave_secs = length(time)/sampleRate;
max_num_cycles = max_freq*length_wave_secs;
num_cycles = 2:4:max_num_cycles;

% FFT parameters
nKern = length(time);
nData = dataLengthSamples*nTrials;
nConv = nKern+nData-1;

% initialize output time-frequency data
tf = zeros(length(num_cycles),length(frex),dataLengthSamples);

% FFT of data (doesn't change on frequency iteration)
dataX = fft(data,nConv);

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
        as=reshape(as,[dataLengthSamples,nTrials]);
        
        % put power data into big matrix
        tf(cyclei,fi,:) = mean(abs(as).^2,2);
    end
    

end

nPlots = length(num_cycles);
sqPlots = ceil(sqrt(nPlots));
% plot results
figure(3), clf
for cyclei=1:length(num_cycles)
    subplot(sqPlots,sqPlots,cyclei)
    
    contourf(t,frex,squeeze(tf(cyclei,:,:)),40,'linecolor','none')
    set(gca,'ylim',[9.75 10.25])
end


