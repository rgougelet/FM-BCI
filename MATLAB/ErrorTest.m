function [o1_error, o2_error, mse] = ErrorTest(dataLengthSamples, sampleRate, o1, o2, mag1, mag2, small_n, neigs, eigv_mag)
    
    dataLengthSamples = 5000;
    small_n = 4;
    neigs = 36;
    eigv_mag = 0.999;
    mag0= 0;
    mag1= 1; o1=10.54;
    mag2= 1; o2=10.56;
    
    sampleRate = 1024;
    sampleSpacing = 1.0 / sampleRate;
    dataLengthSecs = dataLengthSamples/sampleRate;
    t=0:sampleSpacing:dataLengthSecs; t=t(:);
   
    %   y=mag0*randn(N,1)+mag1*sin(o1*t+2*pi*rand)+mag2*sin(o2*t+2*pi*rand);
    y=mag0+mag1*sin(o1*2*pi*t)+mag2*sin(o2*2*pi*t);
    figure
    plot(y)
    
    n=small_n; 
    m=30;
    
    % IS-based estimation
    diff=(o2-o1);
    thetamid=4.2668;
%     thetamid=(o1+diff/2);
    [Ah,bh]=cjordan([neigs],[eigv_mag*exp(thetamid*j)]);
    
    P=dlsim_complex(Ah,bh,y');
    
    [omega_ss,residues_ss]=sm(P,Ah,bh,n); % returns empty
    omega_ss=omega_ss(omega_ss<pi);
    omega_ss=sort(omega_ss);omega_ss=omega_ss(end-1:end);
    
    o1_error = omega_ss(1)-o1;
    o2_error = omega_ss(2)-o2;
    ss = o1_error^2 + o2_error^2;
    mse = ss/2;
    
end