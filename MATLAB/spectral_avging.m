clear, clf

srate = 500;
N = 4*srate;    % length of sequence
nTrials =  300;
fourierTime = ((1:N)-1)/N;   % "time" used for sine waves
nyquist = srate/2;           % Nyquist frequency -- the highest frequency you can measure in the data
signal = zeros(N,nTrials);

for trialInd = 1:nTrials
    signal(:,trialInd) = chan_osc(N,srate,10.54,'isNoisy',1, 'snr', 20, 'isPhaseLocked', 0); % sum to simplify
end
subplot(311);
plot(signal);


avg = mean(signal,2);
subplot(312);
plot(avg)

% initialize Fourier output matrix
fourierCoefs = zeros(size(avg)); 

% These are the actual frequencies in Hz that will be returned by the
% Fourier transform. The number of unique frequencies we can measure is
% exactly 1/2 of the number of data points in the time series (plus DC). 
nfft = srate*100;
frequencies = linspace(0,nyquist,srate*100/2);

% Compute fourier transform and scale
fourierCoefsF = fft(avg, srate*100) / N;

figure(2);
subplot(313),hold on
plot(frequencies,abs(fourierCoefsF(1:length(frequencies)))*2, 'b*')
set(gca,'xlim',[0 40])


% take FFT, then average spectrum
for trialInd = 1:nTrials
    % Compute fourier transform and scale
    ffts(:,trialInd) = fft(signal(:,trialInd), srate*100) / N;
end

avgfft = mean(ffts,2);
subplot(313),hold on
plot(frequencies,abs(avgfft(1:length(frequencies))*2) ,'or')
set(gca,'xlim',[0 40])

figure;
plot(ifft(avgfft))

avgfft = mean(abs(ffts)*2,2);
subplot(313),hold on
plot(frequencies,avgfft(1:length(frequencies)) ,'og')
set(gca,'xlim',[0 40])


conc = reshape(signal,1,[]);
concfft = fft(conc, srate*100) / N;
subplot(313),hold on
plot(frequencies,abs(fourierCoefsF(1:length(frequencies)))*2, 'k-')
set(gca,'xlim',[0 40])


