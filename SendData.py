<<<<<<< HEAD
"""Example program to demonstrate how to send a multi-channel time series to
LSL."""

import random 
import time
=======
import random
import time
import math
>>>>>>> aacc66aa8ff55e57a29c499d25a3bbd585a74e6b
import numpy as np

from pylsl import StreamInfo, StreamOutlet


# first create a new stream info (here we set the name to BioSemi,
# the content-type to EEG, 8 channels, 100 Hz(Sampling Rate/per second), and float-valued data) The
# last value would be the serial number of the device or some other more or
# less locally unique identifier for the stream as far as available (you
# could also omit it but interrupted connections wouldn't auto-recover).
<<<<<<< HEAD
info = StreamInfo('BioSemi', 'EEG', 8, 256, 'float32', 'myuid34234')

fc = 10.  # Hz the carrier frequency
fm = .01  # Hz the modulating frequency
pd = .5   # Hz amplitude of the frequency deviation

signal = np.sin(2 * np.pi * fc * time.time() + pd *
                np.sin(2 * np.pi * fm * time.time()) / fm)
=======
sampleRate = 512.0
info = StreamInfo('BioSemi', 'EEG', 8, sampleRate, 'float32', 'myuid34234')
>>>>>>> aacc66aa8ff55e57a29c499d25a3bbd585a74e6b

# next make an outlet
outlet = StreamOutlet(info)

print("now sending data...")
while True:
<<<<<<< HEAD
    # make a new random 8-channel sample; this is converted into a
    # pylsl.vectorf (the data type that is expected by push_sample)
    mysample = [signal + random.random(), 0, 0, 0, 0, 0, 0, 0]
    # now send it and wait for a bit
    outlet.push_sample(mysample)
    time.sleep(1. / 256.)
=======
    
    # channel1 = np.sin(1.0 * 2.0 * np.pi * time.time())  
    # channel2 = np.sin(5.0 * 2.0 * np.pi * time.time())   
    # channel3 = np.sin(10.0 * 2.0 * np.pi * time.time())   
    # channel4 = np.sin(15.0 * 2.0 * np.pi * time.time())   
    # channel5 = np.sin(10.0 * 2.0 * np.pi * time.time())   
    # channel6 = np.sin(25.0 * 2.0 * np.pi * time.time())  
    # channel7 = np.sin(10.0 * 2.0 * np.pi * time.time()) + random.random()
    # channel8 = random.random()
    
    channel1 = 0.1*np.sin(10.0 * 2.0 * np.pi * time.time()) + random.random() 
    channel2 = 0.2*np.sin(15.0 * 2.0 * np.pi * time.time()) + random.random()  
    channel3 = 0.3*np.sin(20.0 * 2.0 * np.pi * time.time()) + random.random()  
    channel4 = 0.4*np.sin(25.0 * 2.0 * np.pi * time.time()) + random.random()  
    channel5 = 0.5*np.sin(30.0 * 2.0 * np.pi * time.time()) + random.random()  
    channel6 = 0.6*np.sin(35.0 * 2.0 * np.pi * time.time()) + random.random()
    channel7 = 0.7*np.sin(40.0 * 2.0 * np.pi * time.time()) + random.random()
    channel8 = 0.8*np.sin(45.0 * 2.0 * np.pi * time.time()) + random.random()
    
    # each channel have a voltage value over time.
    mysample = [channel1, channel2, channel3,
                channel4, channel5, channel6,
                channel7, channel8]

    # now send it and wait for a bit
    outlet.push_sample(mysample)
    time.sleep(1.0/sampleRate)
>>>>>>> aacc66aa8ff55e57a29c499d25a3bbd585a74e6b
