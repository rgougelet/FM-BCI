function [o1_error, o2_error, mse] = ErrorTest (N, small_n, neigs, eigv_mag)
    
    % implicitly assume fs = 1024
    % assume 10 secs of data, should give freq res of 0.1Hz, but we want to
    % see if it performs at 5 secs
    N = 5*1024;
    small_n = 4;
    neigs = 8;
    eigv_mag = 0.96;
    mag0= 0; 
    mag1= 1; o1=.1; 
    mag2= 1; o2=.15;
    
    
    
    
    t=0:N-1; t=t(:);
   
    %   y=mag0*randn(N,1)+mag1*sin(o1*t+2*pi*rand)+mag2*sin(o2*t+2*pi*rand);
    y=mag0+mag1*sin(o1*t)+mag2*sin(o2*t);
    figure
    plot(y)

    n=small_n; 
    m=30;
    
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