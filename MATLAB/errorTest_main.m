%% Error1 at: neigs - 62  eigv_mag - 0.97

% Z = zeros([99,59]); %Z is MSE
% X = [4:1:62]';      %X represents neigs
% Y = [0:.01:.98]';   %Y is the eign_mag
% for j = 1:58
%     for i = 1:99
%         Z(i,j) = outMSE(i*j);
%     end
% end
% for j = 1:96
%     Z(j,59) = outMSE(5742+j);
% end
% Z(97,59) = [0.185629088970716];
% Z(99,59) = [2.48431986415799];
% 
% disp('Error 1: minimum MSE occurs at neigs = 21, eign_mag = 0.95, MSE = [2.81370667385737e-14]')
% 
% % figure(1)
% % surfc(X,Y,Z)
% % title('Error 1')
% % xlabel('neigs')
% % ylabel('eigv\_mag')
% % zlabel('mse')
% % hold on
% 
% zmax = .0005;
% 
% figure(2)
% surfl(X,Y,Z)
% title('Error 1')
% xlabel('neigs')
% ylabel('eigv\_mag')
% zlabel('mse')
% 
% hold on
% 
% c = uicontrol;
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


%% Plot of N vs n vs MSE with fixed minimal neigs and eign_mag
% minimum MSE occurs at neigs = 21, eign_mag = 0.95, MSE = [2.81370667385737e-14]

% min_neigs = 21;
% min_eign_mag = 0.95;
% 
% w = warning ('off','all');
% 
% output_5 = [];
% for N = 200:100:20000
%     for n = 2:20
%         try
%             [e1, e2, mse] = ErrorTest(N, n, min_neigs, min_eign_mag);
%             output_5(end+1,:) = [N , n, mse];
%         catch
%             N, n
%             output_5(end+1,:) = [N , n, 1e8];
%         end
%     end
% end


% Most optimum: N = 18200, n = 4,mse = 1.22996188683398e-14
% That means we did better!!!



%% Obtaining top 10 most optimal pairs from first batch (start_neigs4_eigv1_end_neigs62_eigv97)
% then plot of N vs n vs MSE

% clear;
% load('start_neigs4_eigv1_end_neigs62_eigv97.mat');

warning ('off','all');


% optimal_pair = [];
%
% % Get the top 10 optimal pair
% for i = 1:10
%     [M_output1,I_output2] = min(output(:,5));
%     optimal_pair(end+1, :) = output(I_output2,:);
%     output(I_output2, 5) = 1e8;
% end

% Get the plot of N vs n vs MSE for all 10 optimal pair

% output_for_each_optimal_pair = []; % dim = 3781 X 3
% output_10_pairs = [];
%
% output_10_pairs(1,:,:) = output_4;

% for loop caused Subscripted assignment dimension mismatch.
% for pair = 2:10
%     pair
%     min_neigs = optimal_pair(pair,1);
%     min_eign_mag = optimal_pair(pair,2);
%     for N = 200:100:20000
%         for n = 2:20
%             try
%                 [e1, e2, mse] = ErrorTest(N, n, min_neigs, min_eign_mag);
%                 output_for_each_optimal_pair(end+1,:) = [N , n, mse];
%             catch
% %                 N, n
%                 output_for_each_optimal_pair(end+1,:) = [N , n, 1e8];
%             end
%         end
%     end
%     output_10_pairs(end+1,:,:) = output_for_each_optimal_pair;
%     output_for_each_optimal_pair = [];
% end

% optimal_5 = [];
% 
% min_neigs = optimal_pair(5,1);
% min_eign_mag = optimal_pair(5,2);
% for N = 200:100:20000
%     for n = 2:20
%         try
%             [e1, e2, mse] = ErrorTest(N, n, min_neigs, min_eign_mag);
%             optimal_5(end+1,:) = [N , n, mse];
%         catch
%             optimal_5(end+1,:) = [N , n, 1e8];
%         end
%     end
% end

%% Optimum 1: neig = 21, eig_mag = 0.95 (old MSE = 2.81370667385737e-14)
%   N = 18200, n = 4, MSE = 1.22996188683398e-14

X_N = [200:100:20000]';
Y_n = [2:1:20]';
Z_1 = zeros([19,199]);
 
for i = 1:199
    for j = 1:19
        Z_1(j,i) = optimum_1_MSE(i*j);
    end
end

disp('Optimum 1: neig = 21, eig_mag = 0.95, N = 18200, n = 4, MSE = 1.22996188683398e-14');
zmax = .05;

% figure(1)
% surfl(X_N,Y_n,Z_1)
% title('Optimum 1')
% xlabel('N')
% ylabel('n')
% zlabel('MSE')
% zlim([0,zmax])
% hold on

%% Optimum 2: neig = 21, eig_mag = 0.94 (old MSE = 2.65797889990932e-13)
% N = 18200, n = 4, MSE = 1.22996188683398e-14

Z_2 = zeros([19,199]);

for i = 1:199
    for j = 1:19
        Z_2(j,i) = optimum_2_MSE(i*j);
    end
end

disp('Optimum 2: neig = 21, eig_mag = 0.94, N = 18200, n = 4, MSE = 1.22996188683398e-14');
zmax = .05;

% figure(2)
% surfl(X_N,Y_n,Z_2)
% title('Optimum 2')
% xlabel('N')
% ylabel('n')
% zlabel('MSE')
% zlim([0,zmax])
% hold on

%% Optimum 3: nieg = 27, eig_mag = .89 (old MSE = 3.70512747418280e-13)
%   N = 8400, n = 4, MSE = 3.84267677942265e-14

Z_3 = zeros([19,199]);

for i = 1:199
    for j = 1:19
        Z_3(j,i) = optimum_3_MSE(i*j);
    end
end

disp('Optimum 3: nieg = 27, eig_mag = .89,  N = 8400, n = 4, MSE = 3.84267677942265e-14');
zmax = .05;
% 
% figure(3)
% surfl(X_N,Y_n,Z_3)
% title('Optimum 3')
% xlabel('N')
% ylabel('n')
% zlabel('MSE')
% zlim([0,zmax])
% hold on

%% Optimum 4: neig = 17, eig_mag = .94 (old MSE = 4.22492051049978e-13)
%   N = 17500, n = 4, MSE = 4,2.39344394938992e-14

Z_4 = zeros([19,199]);

for i = 1:199
    for j = 1:19
        Z_4(j,i) = optimum_4_MSE(i*j);
    end
end

disp('Optimum 4: neig = 17, eig_mag = .94, N = 17500, n = 4, MSE = 2.39344394938992e-14');
zmax = .001;

% figure(4)
% surfl(X_N,Y_n,Z_4)
% title('Optimum 4')
% xlabel('N')
% ylabel('n')
% zlabel('MSE')
% zlim([0,zmax])
% hold on

%% Optimum 5: neig = 24, eig_mag = .93 (old MSE = 5.37097337256780e-13)
%   N = 17000, n = 4, MSE = 2.34173430089391e-13

Z_5 = zeros([19,199]);

for i = 1:199
    for j = 1:19
        Z_5(j,i) = optimum_5_MSE(i*j);
    end
end

disp('Optimum 5: neig = 24, eig_mag = .93, N = 17000, n = 4, MSE = 2.34173430089391e-13');
zmax = .05;

% figure(5)
% surfl(X_N,Y_n,Z_5)
% title('Optimum 5')
% xlabel('N')
% ylabel('n')
% zlabel('MSE')
% zlim([0,zmax])
% hold on

%%
% btn = uicontrol('Style', 'pushbutton', 'String', 'Clear')
   sld = uicontrol('Style', 'slider',...
        'Min',1,'Max',5,'Value',4, 'Callback', {@slide,X_N, Y_n, Z_1, Z_2, Z_3, Z_4, Z_5});
%     if sld.Value == 1
%         zmax = .05;
% 
%         figure(1)
%         surfl(X_N,Y_n,Z_1)
%         title('Optimum 1')
%         xlabel('N')
%         ylabel('n')
%         zlabel('MSE')
%         zlim([0,zmax])
%         hold on
% 
%     elseif sld.Value == 2
%             zmax = .05;
% 
%             figure(2)
%             surfl(X_N,Y_n,Z_2)
%             title('Optimum 2')
%             xlabel('N')
%             ylabel('n')
%             zlabel('MSE')
%             zlim([0,zmax])
%             hold on
% 
%             elseif sld.Value == 3
%                 zmax = .05;
% 
%                 figure(3)
%                 surfl(X_N,Y_n,Z_3)
%                 title('Optimum 3')
%                 xlabel('N')
%                 ylabel('n')
%                 zlabel('MSE')
%                 zlim([0,zmax])
%                 hold on
%             
%                 elseif sld.Value == 4
%                     zmax = .001;
% 
%                     figure(4)
%                     surfl(X_N,Y_n,Z_4)
%                     title('Optimum 4')
%                     xlabel('N')
%                     ylabel('n')
%                     zlabel('MSE')
%                     zlim([0,zmax])
%                     hold on
%                 
%                     else 
%                         zmax = .05;
% 
%                         figure(5)
%                         surfl(X_N,Y_n,Z_5)
%                         title('Optimum 5')
%                         xlabel('N')
%                         ylabel('n')
%                         zlabel('MSE')
%                         zlim([0,zmax])
%                         hold on
%     end
%                     