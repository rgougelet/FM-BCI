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
phaseOffsets = 0:0.1:2*pi;


%% FFT
fft_errors= [];
fft_rts = [];
fft_dls = 1:5:200;

% insert for loop averaging phase offsets 0:0.1:2pi, see the average error
% and average runtime
for dataLengthSecs = fft_dls;
	dataLengthSecs
	fft_errors_dls = [];
	fft_rts_dls = [];
	for phaseOffset = phaseOffsets;
		% Approximately 50sec
		dataLengthSamples = dataLengthSecs*sampleRate;
		osc1 = chan_osc(dataLengthSamples, sampleRate,oscCenter1,'phaseOffset',phaseOffset);
		osc2 = chan_osc(dataLengthSamples, sampleRate,oscCenter2);
		data = osc1+osc2;
		t = 0:sampleSpacing:(dataLengthSecs-sampleSpacing);
		
		%figure;plot(t,data)
		tic
		nfft = 100*sampleRate;
		dataX = fft(data,nfft)/dataLengthSamples;
		fft_f = linspace(0,nyq,floor(nfft/2)+1);
		dataX = dataX(1:length(fft_f)); %keep only positive frequencies
		amp = 2*abs(dataX);
		fft_rt = toc;
		fft_error = performanceMat(fft_f,amp,[oscCenter1,oscCenter2]);
		fft_errors_dls = [fft_errors_dls fft_error];
		fft_rts_dls = [fft_rts_dls fft_rt];
		
		%     plot(fft_f,2*abs(dataX))
		%     xlim([10.5 10.56])
		%     ylabel('Amplitude')
		%     title(['Data Length = ', num2str(fft_dls),' sec'])
		%     pause(0.5)
	end
	
	% (length(fft_dls)) x (length(phaseOffsets)) matrix
	fft_errors = [fft_errors; fft_errors_dls];
	fft_rts = [fft_rts; fft_rts_dls];
end

% REGINA Save output matrix, fft_errors and fft_rts

close all
figure;
plot(fft_dls,fft_errors_avg);
% figure;
% plot(fft_dls,fft_rts);

%% Welch
% figure;
welch_errors = [];
welch_rts = [];
welch_wls = [];
%welch_dls = 1:50:250;
welch_dls = 1:0.25:200;
welch_errors_mat= [];

welch_rts_mat = [];

for phaseOffset = 0:0.1:2*pi;
	i=i+1;
	welch_errors = [];
	welch_rts = [];
	for dataLengthSecs = welch_dls
		dls_errors = [];
		dls_rts = [];
		wls = 1:50:dataLengthSecs;
		for windowLengthSecs = wls;
			dataLengthSamples = dataLengthSecs*sampleRate;
			osc1 = chan_osc(dataLengthSamples, sampleRate,oscCenter1,'phaseOffset',phaseOffset);
			osc2 = chan_osc(dataLengthSamples, sampleRate,oscCenter2);
			data = osc1+osc2;
			
			tic
			windowLengthSamples = windowLengthSecs*sampleRate;
			overlapSecs = 0;
			nOverlap = overlapSecs*sampleRate;
			nfft = 100*sampleRate;
			[pow, welch_f] = pwelch(data,windowLengthSamples,nOverlap,nfft,sampleRate, 'power', 'onesided');
			amp = sqrt(pow);
			dls_rt = toc;
			
			dls_error = performanceMat(welch_f,amp,[oscCenter1,oscCenter2]);
			dls_errors = [dls_errors dls_error];
			dls_rts= [dls_rts dls_rt];
			
			%     plot(welch_f,amp);
			%     xlim([10.5 10.56])
			%     ylabel('Amplitude')
			%     title(['Data Length = ', num2str(welch_dls),' sec'])
			%     pause(0.25)
		end
		
		[welch_error, ind] = min(dls_errors);
		welch_wls = [welch_wls wls(ind)];
		welch_rt = dls_rts(ind);
		welch_errors = [welch_errors welch_error];
		welch_rts= [welch_rts welch_rt];
	end
	welch_errors_mat = [welch_errors_mat; welch_errors];
	welch_rts_mat = [welch_rts_mat; welch_rts];
end
welch_errors_avg = mean(welch_errors_mat);
welch_rts_avg = mean(welch_rts_mat);
close all
figure;
plot(welch_dls,welch_errors_avg);
%%
close all
figure;
% plot(fft_errors);
%plot(fft_dls,fft_errors);
%hold on; plot(welch_dls,welch_errors);


% legend('FFT','Welch')
% figure;
% plot(welch_rts);

%% Regina
% plot FFT vs Welch on the same plot, save the figures, use full range of
% values, 1:0.25:200. Also plot wls for welch, or figure out trend.

%%
% pmusic(data,4,nfft,sampleRate)
