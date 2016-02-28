import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import oscillation as o
import processing as p

from matplotlib.pyplot import figure, title, xlabel, ylabel, plot, grid, show, axis

from numpy import pi





for clearline in range(1,20):
    print('\n')
    
# frequency modulation parameters
alphaCenter = 10   # Hz the carrier frequency
alphaModFreq = 0.01  # Hz the modulating frequency
alphaFreqDev = 2    # Hz of the frequency deviation, BW is 2x this

# generate data to send
sampleRate = 1000
numOfChannel = 1
dataLengthSecs = 10
dataLengthSamples = dataLengthSecs*sampleRate
voltageSamples = np.empty([numOfChannel,dataLengthSamples])
chanSNRs = np.linspace(1./numOfChannel,10,numOfChannel)
#np.random.shuffle(chanSNRs)
#print chanSNRs
#for channelIndex in range(numOfChannel):
#    voltageSamples[channelIndex,:] = o.chan_fm_noisy(dataLengthSamples, sampleRate, alphaCenter, alphaModFreq, alphaFreqDev, chanSNRs[channelIndex])

channelVoltage = o.chan_sin(dataLengthSamples, sampleRate, 11)
channelVoltage2 = o.chan_cos(dataLengthSamples, sampleRate, 10)
# reference = o.chan_sin(dataLengthSamples, sampleRate, 10)
# filter_multiplied = p.butter_bandpass_filter(multiplied, 0, 10, sampleRate, order=4)
f_phi = 10.0
f_step = 0.01
t = 0.0
prev_t = 0.0
prev_mult = 0
t_step = 1.0/sampleRate
ref = 0
ref_array = np.zeros(dataLengthSamples)
prev_diff = 10
mult_array = np.zeros(dataLengthSamples)

for dataIdx in range(dataLengthSamples):
    t += t_step;
    v = channelVoltage[dataIdx]
    multiplied = ref * v
    # diff = np.abs(prev_mult - multiplied)
    # if (diff < prev_diff):
    #     f_step = f_step/10.
    # else:
    #     f_step = f_step*10.
    if (multiplied > 0):
        if (multiplied > 0.99):
            pass
        elif (multiplied < prev_mult):
            f_phi += f_step
        else:
            f_phi -= f_step

    ref = np.sin(f_phi * 2 * pi * t)
    ref_array[dataIdx] = ref
    mult_array[dataIdx] = multiplied
    prev_mult = multiplied
    # prev_diff = diff
    # print v, ref
    # print diff



mult = channelVoltage * channelVoltage2

figure(3)
plot(mult)
plot(channelVoltage,'r')
plot(channelVoltage2,'g')
# plot(multiplied, 'g')
# plot(filter_multiplied, 'k')
grid(True)

show()


# figure(3)
# plot(mult_array)
# plot(channelVoltage,'r')
# plot(ref_array, 'g')
# # plot(multiplied, 'g')
# # plot(filter_multiplied, 'k')
# grid(True)
# title('Input signal & Output signal of VCO')
# xlabel('Samples')
# ylabel('Amplitude')
# show()





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
T = 20.0;    # T is the period
d_phi_1 = 1.0/T;    # d_phi_1 is the frequency because it is 1/period


dataLengthSamples = 100;    #number of data


phi1_reg = np.zeros(dataLengthSamples);  # Store the phase of signal 1
phi2_reg = np.zeros(dataLengthSamples);  # Store the phase of signal 2

phi_error_reg = np.zeros(dataLengthSamples);

reg1_reg = np.zeros(dataLengthSamples);  # array that tracks the phase
reg2_reg = np.zeros(dataLengthSamples);  # array that tracks the phase

s1_reg = np.zeros(dataLengthSamples);    # Stores the signal 1 voltage (This is the input)
s2_reg = np.zeros(dataLengthSamples);    # Stores the signal 2 voltage (modulated voltage)

s1_reg_imag = np.zeros(dataLengthSamples);    # Stores the signal 1 voltage (This is the input)
s2_reg_imag = np.zeros(dataLengthSamples);    # Stores the signal 2 voltage (modulated voltage)

for dataPoint in range(dataLengthSamples):


    phi1 = reg1 + d_phi_1;  
    phi1_reg[dataPoint] = phi1;   # Store the phase of signal 1


    s1 = np.exp(1j*2.0*pi*reg1); # generating the signal 1 and 2 voltage (This is the input)
    s2 = np.exp(1j*2.0*pi*reg2);

    s1_reg[dataPoint] =s1;   # Store signal 1 and 2
    s2_reg[dataPoint] =s2;

    s1_reg_imag[dataPoint] =s1.imag;   # Store signal 1 and 2
    s2_reg_imag[dataPoint] =s2.imag;

    # print "s1 = " + str(s1);
    # print "s2 = " + str(s2);
    # print "channelVoltage = " + str(channelVoltage[dataPoint]);

    t = s1 * s2.conj();   # Detecting the phase by multiplying two sinusoids

    # t = channelVoltage[dataPoint] * s2;

    # print "complex_t = " + str(t);
    # print "real_t = " + str(real_t) + "\n";


    phi_error = np.arctan(t.imag/t.real)/(2.0*pi); # finding phase error
    phi_error_reg[dataPoint] = phi_error;    # store the phase error

    sum1 = Kp*phi_error + phi_error*Ki+reg3;

    reg1_reg[dataPoint] =reg1;
    reg2_reg[dataPoint] = reg2;
    reg1 =phi1;

    reg2=reg2+sum1;
    reg3 =reg3+phi_error*Ki;


    phi2_reg[dataPoint] =reg2;


  




# figure(1)
# title('phase plot');
# xlabel('Samples');
# ylabel('Phase');
# plot(phi1_reg);
# plot(phi2_reg);
# grid(True);
# show();

# figure(2)
# plot(phi_error_reg);
# title('phase Error of phase detector');
# grid(True);
# xlabel('samples(n)');
# ylabel('Phase error(degrees)');
# show();


# figure(3)
# plot(s1_reg_imag);
# plot(s2_reg_imag,'r');
# plot(s1_reg.real, 'g');
# plot(s2_reg.real,'k');
# grid(True);
# title('Input signal & Output signal of VCO');
# xlabel('Samples');
# ylabel('Amplitude');
# show();


# figure(3)
# plot(s1_reg.real);
# plot(channelVoltage,'r');
# grid(True);
# title('Input signal & Output signal of VCO');
# xlabel('Samples');
# ylabel('Amplitude');
# show();



# axis([0 dataLengthSamples -1.1 1.1]);