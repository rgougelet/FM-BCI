function [ power ] = welch_manual( signal,windowLengthSamples,OverlapPercent,nfft,maxK )
	%what is maxK?
	FFTX = zeros(1,nfft);
	maxK = 15;
	stepsize = (100-OverlapPercent)*windowLengthSamples;
	for K = 0:maxK-1
		U = sum(hamming(nfft))/nfft;
		startwin = stepsize*K + 1;
		endwin = stepsize*K + windowLengthSamples;
		FFTK = fft(hamming(nfft)'.*signal(startwin:endwin));
		magFFTK = (1/(M*U))*abs(FFTK).^2; %Normalize
		phaFFTK = angle(FFTK);	
		dbFFTK = 20*log10(magFFTK);
		dbFFTK = dbFFTK - max(dbFFTK);
		dbFFTK = dbFFTK./maxK; %Average
		FFTX = FFTX + dbFFTK;
	end
	fn = linspace(-.5,.5,nfft);
	figure;
	plot(fn,fftshift(FFTX)); grid on;
	xlabel('Normalized Frequency (cycles per sample)'); 
	ylabel('Magnitude (dB)');
	axis([-0.5 0.5 -60 0])
   power=fftshift(FFTX);

end

