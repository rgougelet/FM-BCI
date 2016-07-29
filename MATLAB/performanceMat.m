function [ errSort, errPerm ] = performanceMat( freq, amp, target )
%detect the number of peaks and the length from the target frequencies

%errSort output
[Y, I]=sort(amp);
IndexFreq= I((end-length(target)+1):end);
SortTarget=sort(target);
%errSort = (SortTarget-freq(IndexFreq)).^2/length(target);
SubtractMat=[];
for i=1:length(IndexFreq)
    SubtractMat=[SubtractMat, SortTarget-freq(IndexFreq(i))];
end
% SubtractMat=SubtractMat';
% SubtractMat=reshape(SubtractMat',length(target),length(target)); reshape
% will generate column wise mat that's why the diagnal is just flipped 
errSort= mean(SubtractMat(1:length(target)+1:end).^2);
errPerm = mean(SubtractMat.^2);

end

