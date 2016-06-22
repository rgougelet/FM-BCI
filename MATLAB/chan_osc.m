function [voltageSamples,instAmp, instFreq, instPhase] = chan_osc(dataLengthSamples, sampleRate, oscCenter, varargin)

    % default params
    oscAmp = 1;
    
    isFM = 0;
    oscModFreq = 1;
    oscFreqDev = 1;
    
    isAM = 0;
    oscAModFreq = 1;
    oscAmpDev = 1;
    
    isNoisy = 0;
    oscMean = 0;
    oscStdDev = 1/sqrt(2);
    snr = 5;
    noiseMean = 0;
    noiseStdDev = 0.5;
    samplingNoiseAmp = 0;
    
    % open help if no arguments provided
    if nargin == 1
        help chan_fm;
        return
    end
    
    % check for minimum required inputs
    if (0 < nargin) && (nargin < 3)
        error('myfuns:somefun2:TooFewInputs', ...
            'Requires at least 3 inputs, 8 optional');
    end
    
    % make sure all keywords have matching values
    if (round(nargin/2) == nargin/2)
        error('Even number of input arguments??')
    end
    
    % Does the user want AM signal?
    for i = 1:2:length(varargin)
        Param = varargin{i};
        Value = varargin{i+1};
        if ~ischar(Param)
            error('Flag arguments must be strings')
        end
        if strcmpi(Param,'isAM')
            isAM = Value;
        end
        if isAM
            for i = 1:2:length(varargin)
                Param = varargin{i};
                Value = varargin{i+1};
                if ~isstr(Param)
                    error('Flag arguments must be strings')
                end
                Param = lower(Param);
                switch Param
                    case 'oscAModFreq'
                        oscAModFreq = Value;
                    case 'oscAmpDev'
                        oscAmpDev = Value;
                end
            end
            break
        end
    end
    
    % Does the user want FM signal?
    for i = 1:2:length(varargin)
        Param = varargin{i};
        Value = varargin{i+1};
        if ~ischar(Param)
            error('Flag arguments must be strings')
        end
        if strcmpi(Param,'isFM')
            isFM = Value;
        end
        if isFM
            for i = 1:2:length(varargin)
                Param = varargin{i};
                Value = varargin{i+1};
                if ~isstr(Param)
                    error('Flag arguments must be strings')
                end
                Param = lower(Param);
                switch Param
                    case 'oscModFreq'
                        oscModFreq = Value;
                    case 'oscFreqDev'
                        oscFreqDev = Value;
                end
            end
            break
        end
    end
    
    % Does the user want noisy signal?
    for i = 1:2:length(varargin)
        Param = varargin{i};
        Value = varargin{i+1};
        if ~ischar(Param)
            error('Flag arguments must be strings')
        end
        if strcmpi(Param,'isNoisy')
            isNoisy = Value;
        end
        if isNoisy
            for i = 1:2:length(varargin)
                Param = varargin{i};
                Value = varargin{i+1};
                if ~isstr(Param)
                    error('Flag arguments must be strings')
                end
                Param = lower(Param);
                switch Param
                    case 'oscMean'
                        oscMean = Value;
                    case 'snr'
                        snr = Value;
                    case 'noiseMean'
                        noiseMean = Value;
                    case 'noiseStdDev' 
                        noiseStdDev = Value;
                    case 'samplingNoiseAmp' 
                        samplingNoiseAmp = Value;
                end
            end
            break
        end
    end
    
    % TODO: add error case where fc-fm cannot be negative
    % TODO: add error case where ac-am cannot be negative
    % TODO: throw error for amplitude provided in noise case, when
    % stddev... is provided
    
    % Signal to noise parameters
    if isNoisy
        oscStdDev = abs(sqrt(snr*(noiseStdDev^2)));
        oscAmp = sqrt(2)*oscStdDev;
    end
    % Constructs 1/f noise by taking CDF of normal dist.
    power = noiseStdDev^2;
    normalNoise = wgn(1,dataLengthSamples, power);
    pinkNoise = noiseMean+cumsum(normalNoise);
    
    % Constructs signal
    sampleSpacing = 1/sampleRate;
    dataLengthSecs = dataLengthSamples/sampleRate;
    t = 0:sampleSpacing:(dataLengthSecs-sampleSpacing);
    h = oscFreqDev/oscModFreq; % Modulation index, FYI < 1 narrowband, > 1 wideband
    instAmp = oscAmp+isAM*oscAmpDev*sin(2*pi*oscAModFreq*t)/oscAModFreq; % mod around center amp
    instFreq = oscCenter + (isFM*oscFreqDev)*sin(2*pi*oscModFreq*t)/oscModFreq; % mod around center freq
    voltageSamples = instAmp.*sin(instFreq*2*pi.*t) + isNoisy*(pinkNoise + samplingNoiseAmp * rand(1,dataLengthSamples));
    
    %Optional output of instaneous phase
    instPhase = sampleRate./diff(instFreq);%unwrapped
end