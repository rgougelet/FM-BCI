sr=300; 
time_before=0; %ms
time_after=500;
nofilt=0;
ploton=0;
secicaon=0;

%amplitude is in volts need to convert to microvolts (multiply by 1000000).

sampdur=1000./sr;

time_bef_samp=round(time_before./sampdur);
time_aft_samp=round(time_after./sampdur);

eegdat=cog_load('exg_28.cog', 64, 0, 3, 0);
%time_stamps=load_experiment('snd150512c.bin');

%trig1=eegdat(:,69);
%i2=find(trig1>5500);
%d2=find(diff(i2)>10);
%indtrig1=i2(d2+1);

t1=eegdat(:,69);
t2=eegdat(:,69);
t3=eegdat(:,69);


%i1=find(t1==5376);
%d1=find(diff(i1)>1);
%indtrig1=(i3(d1+1));




eegcont=eegdat(:,1:64).*1000000; %change from volt to microvolts
eegcont=eegcont';

acccont=eegdat(:,65:67);
acccont=acccont';


%onset1=indtrig3-time_bef_samp;
%onset2=indtrig3+time_aft_samp-1;

%for i=1:length(indtrig3);
%    eegevent(:,:,i)=eegcont(:,onset1(i):onset2(i));
%end

