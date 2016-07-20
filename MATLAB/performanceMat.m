function [ errSort err2 ] = performanceMat( freq, amp, target )
%detect the number of peaks and the length from the target frequencies 
[Y, idex1]=max(amp);
amp(idex1)=0;
[Y, idex2]=max(amp);
SortIdex=sort([idex1 idex2]);
SortTarget=sort(target);
errSort = (SortTarget-freq(SortIdex)).^2/length(target);
for i=1:length(target)
    

    

end

