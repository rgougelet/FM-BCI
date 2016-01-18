import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure, title, xlabel, ylabel, plot, grid, show, axis

from numpy import pi


reg1 = 0; # track the phase
reg2 = 0;
reg3 = 0;

eta = np.sqrt(2)/2.0;           # constant - used to change the gain
theta =2.0*pi*1.0/100.0;        # play around with it - used to change the gain

# Kp and Ki are two parameters about second-order filter.
# you can find the ralation between KP Ki and aquisition bandwidth in gardner's book
Kp = (4.0*eta*theta)/(1.0+2.0*eta*theta+theta**2.0);
Ki = (4.0*theta**2.0)/(1.0+2.0*eta*theta+theta**2.0);

# We don't need d_phi_1 because it is used to generate sig1 or the input
# signal, we will just use the voltage sample collected
d_phi_1 = 1.0/20.0;    #delta phi1


dataLengthSamples = 100;    #number of data


phi1_reg = np.zeros(dataLengthSamples);  # Store the phase of signal 1
phi2_reg = np.zeros(dataLengthSamples);  # Store the phase of signal 2

phi_error_reg = np.zeros(dataLengthSamples);

reg1_reg = np.zeros(dataLengthSamples);  # array that tracks the phase
reg2_reg = np.zeros(dataLengthSamples);  # array that tracks the phase

s1_reg = np.zeros(dataLengthSamples);    # Stores the signal 1 voltage (This is the input)
s2_reg = np.zeros(dataLengthSamples);    # Stores the signal 2 voltage (modulated voltage)

for dataPoint in range(dataLengthSamples):

    phi1 = reg1 + d_phi_1;  
    phi1_reg[dataPoint] = phi1;   # Store the phase of signal 1


    s1 = np.exp(1j*2.0*pi*reg1); # generating the signal 1 and 2 voltage (This is the input)
    s2 = np.exp(1j*2.0*pi*reg2);

    s1_reg[dataPoint] =s1;   # Store signal 1 and 2
    s2_reg[dataPoint] =s2;

    t = s1 * s2.conj();   # Detecting the phase by multiplying two sinusoids
    phi_error = np.arctan(t.imag/t.real)/(2.0*pi); # finding phase error
    phi_error_reg[dataPoint] = phi_error;    # store the phase error

    sum1 = Kp*phi_error + phi_error*Ki+reg3;

    reg1_reg[dataPoint] =reg1;
    reg2_reg[dataPoint] = reg2;
    reg1 =phi1;

    reg2=reg2+sum1;
    reg3 =reg3+phi_error*Ki;


    phi2_reg[dataPoint] =reg2;

  

print phi1_reg;
print phi2_reg;


figure(1)
title('phase plot');
xlabel('Samples');
ylabel('Phase');
plot(phi1_reg);
plot(phi2_reg);
grid(True);
show();

figure(2)
plot(phi_error_reg);
title('phase Error of phase detector');
grid(True);
xlabel('samples(n)');
ylabel('Phase error(degrees)');
show();


figure(3)
plot(s1_reg.real);
plot(s2_reg.real,'r');
grid(True);
title('Input signal & Output signal of VCO');
xlabel('Samples');
ylabel('Amplitude');
show();

# axis([0 dataLengthSamples -1.1 1.1]);