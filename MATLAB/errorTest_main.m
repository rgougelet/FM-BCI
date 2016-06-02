%% parameter space search
% for neigs = 1:1000 (may be not so big) & eigv_mag = 0:0.01:0.99 at a fixed freq difference between the two
% sinusoids, what is the o1 and o2 error. also try and see what theta_mid
% should be, i.e. midpoint between them, or the diff. use try catch, if
% error make mse some fixed value that doesn't disturb the plot

clear, close all
% 
output = [];

% Summaries:
%
%=== Independent:
% neigs: lowerbound - 4, upper bound 134
% eigv_mag: lowerbound - 0, upper bound .99
%
%=== Run together in a nested for loop:
%
% Start Range: neigs - 4, eigv_mag - 0.01
%   Output: M_output1 = 2.8137e-14 (min value for mse)
%           I_output2 = 1779       (min value index)  
%   Output the smallest row: 21.0000    0.9500   -0.0000    0.0000    0.0000
% Error1 at: neigs - 62  eigv_mag - 0.97
%   M_output1 = 4.8825e-11
%   I_output2 = 62
% Error2 at: neigs - 63  eigv_mag - 0.96
%   M_output1 = 4.8825e-11
%   I_output2 = 62
% Error3 at: neigs - 67  eigv_mag - 0.95


for neigs = 1:134
    for eigv_mag = 0.95%0:0.01:0.99
        tic
%         [e1, e2, mse] = ErrorTest(neigs_index, eigv_mag_index);
        N=2000; mag0=1; mag1=1; o1=.1; mag2= 1; o2=.15;
        t=0:N-1; t=t(:);

        %   y=mag0*randn(N,1)+mag1*sin(o1*t+2*pi*rand)+mag2*sin(o2*t+2*pi*rand);
        y=mag0+mag1*sin(o1*t)+mag2*sin(o2*t);

        % estimating sinusoids per music, esprit
        n=5;

        % IS-based estimation
        diff = (o2-o1);

        thetamid=o1+diff/2; [Ah,bh]=cjordan([neigs],[eigv_mag*exp(thetamid*j)]);

        P=dlsim_complex(Ah,bh,y');
        try
            [omega_ss,residues_ss]=sm(P,Ah,bh,n);
            omega_ss=omega_ss(omega_ss<pi);
            omega_ss=sort(omega_ss);omega_ss=omega_ss(end-1:end);
            o1_error = omega_ss(1)-o1;
            o2_error = omega_ss(2)-o2;
            ss = o1_error^2 + o2_error^2;
            mse = ss/2;
        catch
            omega_ss(1) = 0;
            omega_ss(2) = 0;
            o1_error=99;
            o2_error=99;
            ss = o1_error^2 + o2_error^2;
            mse = ss/2;
        end
        runtime = toc;
        output(end+1,:) = [neigs, eigv_mag, omega_ss(1), omega_ss(2), o1_error, o2_error, mse, runtime];
    end
end


% [M_output1,I_output2] = min(output(:,5))
% Output: M_output1 = 2.8137e-14, I_output2 = 1779
% output(1779,:)
% Output the smallest row: 21.0000    0.9500   -0.0000    0.0000    0.0000


