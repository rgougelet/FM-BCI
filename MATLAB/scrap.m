N=100;
    a0=1.8; a1=1.5; theta1=1.3; a2=2; theta2=1.35;
    k=1:N; k=k(:);
    y=a0*randn(N,1)+a1*exp(1i*(theta1*k+2*pi*rand))+a2*exp(1i*(theta2*k+2*pi*rand));
    
    


euler1 = a1*exp(1i*theta1*k);
euler2 = a2*exp(1i*theta2*k);
for ind = 1:N
    hold off
    t = 0 : .01 : 2 * pi;
    P = polar(t, 2 * ones(size(t)));
    set(P, 'Visible', 'off')
    hold on
    h = polar([0 angle(euler1(ind))],[0 abs(euler1(ind))],'r-o');
    h = polar([0 angle(euler2(ind))],[0 abs(euler2(ind))],'r-o');
    pause(0.25)
end

