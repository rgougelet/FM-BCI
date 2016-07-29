function [errPerm ] = performanceMat( freq, amp, target )
%detect the number of peaks and the length from the target frequencies

%errSort output
[Y, I]=sort(amp);
IndexFreq= I((end-length(target)+1):end);
Freqs = round(freq(IndexFreq),2);
permFreqs = perms(Freqs);
errs = zeros(1,length(permFreqs));
for row = 1:length(permFreqs)
    errs(row) = mean((permFreqs(row,:)-target).^2);
end
errs = round(errs,6);
errPerm = min(errs);
% SortTarget=sort(target);
%errSort = (SortTarget-freq(IndexFreq)).^2/length(target);
% SubtractMat=zeros(length(target));
% for Ti = 1:length(target)
%     for Fi = 1:length(target)
%         SubtractMat(Ti,Fi) = SortTarget(Ti) - round(freq(IndexFreq(Fi)),2);
%     end
% end
% SubtractMat = round(SubtractMat,2);
% err1 = mean(diag(SubtractMat).^2);
% err2 = mean(diag(SubtractMat).^2);
% for i=1:length(IndexFreq)
%     fi = round(freq(IndexFreq(i)),2)
%     SubtractMat=[SubtractMat, SortTarget-fi];
% end
% 
% SubtractMat=SubtractMat';
% SubtractMat=reshape(SubtractMat',length(target),length(target)); reshape
% will generate column wise mat that's why the diagnal is just flipped 
% errSort1= mean(SubtractMat(1:length(target)+1:end).^2);
% errSort2= mean(SubtractMat(1:length(target)+1:end).^2);
% errPerm = mean(SubtractMat.^2);

end

