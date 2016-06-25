% demo: scatter plots comparing sm with music and esprit
%       it shows that the variance of the sm-estimates is
%       superior to the other two.
%
% simulation example from sesha2 page 38

% Setting up the signal parameters and time interval
% here y=unit variance white noise + .5*sin(.1*t+phi1) + sin(.15*t+phi2)
clear, close all
% 1000samples/100secs => srate = 10 samples/secs
% N=1000; mag0=.35; mag1=.5; o1=.1; mag2=1; o2=.15;

N = 1000000;
srate = 1000;
f1 = 10.52;
f2 = 10.56;
o1 = 2*pi*f1; % 66.0991
o2 = 2*pi*f2; % 66.3504
tic
osc1 = chan_osc(N,srate,10.52);
osc2 = chan_osc(N,srate,10.56);


% o1 = 0.1 = 2*pi*f => f = 0.1571
% o2 = 0.15 = 2*pi*f => f = 0.2356
% sin(2*pi*f*t)
t=0:N-1; t=t(:);

% drawing the target frequency1 vs frequency2 for the subsequently generated
% scatter diagrams
figure(1), clf,
subplot(3,1,1), plot(o1,o2,'rx','MarkerSize',12),  hold on,
subplot(3,1,2), plot(o1,o2,'rx','MarkerSize',12),  hold on,
subplot(3,1,3), plot(o1,o2,'rx','MarkerSize',12),  hold on,


% simulating the time series and determining the frequencies of the two
% sinusoids.
IS_count=0;
MUSIC_count=0;
ESPRIT_count=0;
for i=1:100,
    
%   y=mag0*randn(N,1)+mag1*sin(o1*t)+mag2*sin(o2*t);
    y=osc1+osc2;%+mag2*sin(o2*t);
    
% estimating sinusoids per music, esprit
n=4; m=30;
omusic=music(y,n,m); omusic=omusic(omusic>=0);
omusic=sort(omusic); omusic=omusic(end-1:end);
oesprit=esprit(y,n,m); oesprit=oesprit(oesprit>=0);
oesprit=sort(oesprit); oesprit=oesprit(end-1:end);
diff = (o2-o1);
    
thetamid=o1+diff/2;
% IS-based estimation
[Ah,bh]=cjordan([20],[0.99*exp(thetamid*j)]);

P=dlsim_complex(Ah,bh,y');

[omega_ss,residues_ss]=sm(P,Ah,bh,n);
omega_ss=omega_ss(omega_ss<pi);
omega_ss=sort(omega_ss);omega_ss=omega_ss(end-1:end);

if(omega_ss(1)>0.07&&omega_ss(1)<0.13&&omega_ss(2)>0.12&&omega_ss(2)<0.18)
    IS_count=IS_count+1;
end
if(omusic(1)>0.07&&omusic(1)<0.13&&omusic(2)>0.12&&omusic(2)<0.18)
    MUSIC_count=MUSIC_count+1;
end
if(oesprit(1)>0.07&&oesprit(1)<0.13&&oesprit(2)>0.12&&oesprit(2)<0.18)
    ESPRIT_count=ESPRIT_count+1;
end

[omega_ss,omusic oesprit];
subplot(3,1,1), plot(omega_ss(1),omega_ss(2),'o'),
subplot(3,1,2), plot(omusic(1),omusic(2),'o'),
subplot(3,1,3), plot(oesprit(1),oesprit(2),'o'),
end

figure(1),
subplot(3,1,1), axis([66 67 66 67]); hold on,  legend('sm')
subplot(3,1,2), axis([66 67 66 67]); hold on,  legend('music')
subplot(3,1,3), axis([66 67 66 67]); hold on,  legend('esprit')