clear all
close all
%% MUSIC

Fs = 10;      %sampline frequency
T = 1/Fs;       %sampling period
L = 1000;       %length of the signal
t = (0:L-1)*T;  %time vector
Signal = sin(2*pi*t);
alpha = linspace(0,2*pi,2000);
alphaWave = sin(10*pi*alpha);
fou = fft(alphaWave);
fftsignal = fftshift(fou);
% frequency = length(transpose(aplha))/2*linspace(-1,1,2000);
pmusic(alphaWave,2)
% w = 57.2958*pi*w;
% S = pi*S;

% figure(1);
% plot(w,S);
% title('MUSIC Algorithm');
% xlabel('Normalized Frequency ( x pi rad/sample)');
% ylabel('Power Spectral Density (PSD)');
% 
% figure(2);
% plot(1000*linspace(-1,1,2000),abs(fftsignal));
% plot(alphaWave);

%% Example
%{
%Define number of samples to take
fs = 8000;
f = 400; %Hz

%Define signal
t = 0:1/fs:1-1/fs;
signal = sin(2*pi*f*t);

%Plot to illustrate that it is a sine wave
plot(t, signal);
title('Time-Domain signal');

%Take fourier transform
fftSignal = fft(signal);

%apply fftshift to put it in the form we are used to (see documentation)
fftSignal = fftshift(fftSignal);

%Next, calculate the frequency axis, which is defined by the sampling rate
f = fs/2*linspace(-1,1,fs);

%Since the signal is complex, we need to plot the magnitude to get it to
%look right, so we use abs (absolute value)
figure;
plot(f, abs(fftSignal));
title('magnitude FFT of sine');
xlabel('Frequency (Hz)');
ylabel('magnitude');

%noise
noise = 2*randn(size(signal));
figure, plot(t,noise), title('Time-Domain Noise');
fftNoise = fft(noise);
fftNoise = fftshift(fftNoise);
figure, plot(f,abs(fftNoise)), title('Magnitude FFT of noise');
xlabel('Frequency (Hz)');
ylabel('magnitude');

%noisy signal
noisySignal = signal + noise;
figure, plot(t,noisySignal), title('Time-Domain Noisy Signal');
fftNoisySignal = fft(noisySignal);
fftNoisySignal = fftshift(fftNoisySignal);
figure, plot(f,abs(fftNoisySignal)), title('Magnitude FFT of noisy signal');
xlabel('Frequency (Hz)');
ylabel('magnitude');
%}

%% MUSIC example

n=0:99;   
s=exp(1i*pi/2*n)+2*exp(1i*pi/4*n)+exp(1i*pi/3*n)+randn(1,100);  
X=corrmtx(s,12,'mod');   % Estimate the correlation matrix using
                      % the modified covariance method.
pmusic(X,3,'whole')      % Uses the default NFFT of 256.

n=0:99; figure;
s2=sin(pi/3*n)+2*sin(pi/4*n)+randn(1,100);
X2=corrmtx(s2,20,'cov'); % Estimate the correlation matrix using
                      % the covariance method.            
pmusic(X2,4,'whole')     % Use twice the signal space dimension
                      % for real sinusoids.
          
% figure;
% Fs = 10;      %sampline frequency
% T = 1/Fs;       %sampling period
% L = 1000;       %length of the signal
% t = (0:L-1)*T;  %time vector
% alpha = linspace(0,2*pi,2000);
% alphaWave = sin(10*pi*alpha);
% X3=corrmtx(alphaWave,6,'mod');   % Estimate the correlation matrix using
% pmusic(alphaWave,2, 'whole')

 
                      