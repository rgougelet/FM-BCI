% demo: scatter plots comparing sm with music and esprit
%       it shows that the variance of the sm-estimates is
%       superior to the other two.
%
% simulation example from sesha2 page 38

% Setting up the signal parameters and time interval
% here y=unit variance white noise + .5*sin(.1*t+phi1) + sin(.15*t+phi2)
clear, close all

neigs = 20;
eigv_mag = 0.99;


N=20000; mag0=1; mag1=1; o1=.1; mag2= 1; o2=.15;
t=0:N-1; t=t(:);

% simulating the time series and determining the frequencies of the two
% sinusoids.
IS_count=0;

for i=1:10
    %   y=mag0*randn(N,1)+mag1*sin(o1*t+2*pi*rand)+mag2*sin(o2*t+2*pi*rand);
    y=mag0+mag1*sin(o1*t)+mag2*sin(o2*t);
    % figure(2)
    %   plot(y)
    % estimating sinusoids per music, esprit
    n=4; m=30;
    
    % IS-based estimation
    diff = (o2-o1);
    
    thetamid=o1+diff/2; [Ah,bh]=cjordan([neigs],[eigv_mag*exp(thetamid*j)]);
    
    P=dlsim_complex(Ah,bh,y');
    
    [omega_ss,residues_ss]=sm(P,Ah,bh,n);
    omega_ss=omega_ss(omega_ss<pi);
    omega_ss=sort(omega_ss);omega_ss=omega_ss(end-1:end);
    
    
    
    o1_error = omega_ss(1)-o1;
    o2_error = omega_ss(2)-o2;
    ss = o1_error^2 + o2_error^2;
    mse = ss/2;
    
end


