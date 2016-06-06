function slide(source,callbackdata, X_N, Y_n, Z_1, Z_2, Z_3, Z_4, Z_5) 
val = 6 - source.Value;
     if val == 1
        zmax = .05;

        figure(1)
        surfl(X_N,Y_n,Z_1)
        title('Optimal 1')
        xlabel('N')
        ylabel('n')
        zlabel('MSE')
        zlim([0,zmax])
        hold on

    elseif val == 2
            zmax = .05;

            figure(2)
            surfl(X_N,Y_n,Z_2)
            title('Optimal 2')
            xlabel('N')
            ylabel('n')
            zlabel('MSE')
            zlim([0,zmax])
            hold on

            elseif val == 3
                zmax = .05;

                figure(3)
                surfl(X_N,Y_n,Z_3)
                title('Optimal 3')
                xlabel('N')
                ylabel('n')
                zlabel('MSE')
                zlim([0,zmax])
                hold on
            
                elseif val == 4
                    zmax = .001;

                    figure(4)
                    surfl(X_N,Y_n,Z_4)
                    title('Optimal 4')
                    xlabel('N')
                    ylabel('n')
                    zlabel('MSE')
                    zlim([0,zmax])
                    hold on
                
                    else 
                        zmax = .05;

                        figure(5)
                        surfl(X_N,Y_n,Z_5)
                        title('Optimal 5')
                        xlabel('N')
                        ylabel('n')
                        zlabel('MSE')
                        zlim([0,zmax])
                        hold on
     end
end
