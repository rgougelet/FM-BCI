% demo: scatter plots comparing sm with music and esprit
%       it shows that the variance of the sm-estimates is
%       superior to the other two.
%
% simulation example from sesha2 page 38

% Setting up the signal parameters and time interval
% here y=unit variance white noise + .5*sin(.1*t+phi1) + sin(.15*t+phi2)
clear all, close all

nsecs = 2;
fs=2048;
nyq = fs/2;
mag0=1;mag1=1; hz1=10.52; mag2=1; hz2=10.54;
o1 = 2*pi*hz1/nyq;
o2 = 2*pi*hz2/nyq;
x = linspace(0,nsecs, fs*nsecs);
y = sin(hz1*2*pi*x)+sin(hz2*2*pi*x);
plot(y)
% drawing the target frequency1 vs frequency2 for the subsequently generated
% scatter diagrams
figure(1), clf,
plot(o1,o2,'rx','MarkerSize',12),  hold on,
% subplot(3,1,2), plot(o1,o2,'rx','MarkerSize',12),  hold on,
% subplot(3,1,3), plot(o1,o2,'rx','MarkerSize',12),  hold on,


% simulating the time series and determining the frequencies of the two
% sinusoids.
IS_count=0;
MUSIC_count=0;
ESPRIT_count=0;
o1s = [];
o2s = [];
for i=1:10,
    y = sin(hz1*2*pi*x)+sin(hz2*2*pi*x);
    
    % estimating sinusoids per music, esprit
    n=4; m=30;
    omusic=music(y,n,m); omusic=omusic(omusic>=0);
    omusic=sort(omusic); omusic=omusic(end-1:end);
    oesprit=esprit(y,n,m); oesprit=oesprit(oesprit>=0);
    oesprit=sort(oesprit); oesprit=oesprit(end-1:end);

    % IS-based estimation
    diff = (o2-o1);
    minthresh1 = o1-diff;
    maxthresh1 = o1+diff;
    minthresh2 = o2-diff;
    maxthresh2 = o2+diff;
    thetamid=o1+diff/2; [Ah,bh]=cjordan([4],[0.90*exp(thetamid*j)]);

    P=dlsim_complex(Ah,bh,y');

    [omega_ss,residues_ss]=sm(P,Ah,bh,n);
    omega_ss=omega_ss(omega_ss<pi);
    omega_ss=sort(omega_ss);omega_ss=omega_ss(end-1:end);

    if(omega_ss(1)>minthresh1&&omega_ss(1)<maxthresh1&&omega_ss(2)>minthresh2&&omega_ss(2)<maxthresh2)
        IS_count=IS_count+1;
    end
    if(omusic(1)>0.07&&omusic(1)<0.13&&omusic(2)>0.12&&omusic(2)<0.18)
        MUSIC_count=MUSIC_count+1;
    end
    if(oesprit(1)>0.07&&oesprit(1)<0.13&&oesprit(2)>0.12&&oesprit(2)<0.18)
        ESPRIT_count=ESPRIT_count+1;
    end

    % [omega_ss,omusic oesprit];
%     plot(omega_ss(1),omega_ss(2),'o'),
%     o1s = [o1s omega_ss(1)];
%     o2s = [o2s omega_ss(2)];
    % subplot(3,1,2), plot(omusic(1),omusic(2),'o'),
    % subplot(3,1,3), plot(oesprit(1),oesprit(2),'o'),
end
% mean((o1s-o1))/diff
% mean((o2s-o2))/diff
% figure(1),
% axis([minthresh1 maxthresh1 minthresh2 maxthresh2]); hold on,  legend('sm')
% subplot(3,1,2), axis([.07 .076 .07 .076]); hold on,  legend('music')
% subplot(3,1,3), axis([.07 .076 .07 .076]); hold on,  legend('esprit')