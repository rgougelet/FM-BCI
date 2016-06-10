freqres = zeros(32,100);
for N = 1:100;
    for fs = 1:32
        freqres(fs,N) = fs./N;
    end
end
N = 1:100;
fs = 1:32;
% figure;
hold on;
surf(N,fs,freqres)
% zlim([0,0.02])


freqres = zeros(32,100);
for N = 1:100;
    for fs = 1:32
        time(fs,N) = N/fs;
    end
end
N = 1:100;
fs = 1:32;
figure;
surf(N,fs,time)
