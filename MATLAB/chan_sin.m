function voltageSamples = chan_sin(dataLengthSamples, sampleRate, oscCenter, oscAmp)
    % Check number of inputs.
    if nargin > 4
        error('myfuns:somefun2:TooManyInputs', ...
            'Requires at most 4 inputs, 1 optional');
    end
    
    switch nargin
        case 3
            oscAmp = 1;
    end
    
    sampleSpacing = 1.0 / sampleRate;
    dataLengthSecs = dataLengthSamples/sampleRate;
    t = 0:sampleSpacing:dataLengthSecs;
    voltageSamples = oscAmp * sin(oscCenter*2.0*pi*t);
end