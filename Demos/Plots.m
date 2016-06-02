%% Error1 at: neigs - 62  eigv_mag - 0.97

Z = zeros([99,59]); %Z is MSE
X = [4:1:62]';      %X represents neigs
Y = [0:.01:.98]';   %Y is the eign_mag
for j = 1:58
    for i = 1:99
    Z(i,j) = outMSE(i*j);
    end
end
for j = 1:96
    Z(j,59) = outMSE(5742+j);
end
Z(97,59) = [0.185629088970716];
Z(99,59) = [2.48431986415799];

disp('Error 1: minimum MSE occurs at neigs = 21, eign_mag = 0.95, MSE = [2.81370667385737e-14]')

% figure(1)
% surfc(X,Y,Z)
% title('Error 1')
% xlabel('neigs')
% ylabel('eigv\_mag')
% zlabel('mse')
% hold on

zmax = .0005;

figure(2)
surfl(X,Y,Z)
title('Error 1')
xlabel('neigs')
ylabel('eigv\_mag')
zlabel('mse')
zlim([0,zmax])
hold on

c = uicontrol;
%% Error 2: at negis = 63, eig_mag = .96

% X2 = 63*ones(96,1);     %X2 represents neigs
% Y2 = [0:.01:.95]';      %Y2 is the eign_mag
% Z2 = zeros([96,96]);    %Z2 is MSE
% for j = 1:96
%     for i = 1:96
%         Z2(i,j) = out2MSE(i);
%     end
% end
% 
% disp('Error 2: minimum MSE occurs at neigs = 63, eign_mag = .2, MES = [1.43713002308106e-10]')
% 
% figure(3)
% surfc(X2,Y2,Z2)
% title('Error 2')
% xlabel('neigs')
% ylabel('eigv\_mag')
% zlabel('mse')
% hold on
% 
% figure(4)
% surfl(X2,Y2,Z2)
% title('Error 2')
% xlabel('neigs')
% ylabel('eigv\_mag')
% zlabel('mse')
% hold on