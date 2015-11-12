"""Example program to demonstrate how to send a multi-channel time series to
LSL."""

import random
import time
import math
import numpy as np

from pylsl import StreamInfo, StreamOutlet

# first create a new stream info (here we set the name to BioSemi,
# the content-type to EEG, 8 channels, 100 Hz(Sampling Rate/per second), and float-valued data) The
# last value would be the serial number of the device or some other more or
# less locally unique identifier for the stream as far as available (you
# could also omit it but interrupted connections wouldn't auto-recover).
info = StreamInfo('BioSemi', 'EEG', 8, 256, 'float32', 'myuid34234')

# next make an outlet
outlet = StreamOutlet(info)

print("now sending data...")
while True:
    # make a new random 8-channel sample; this is converted into a
    # pylsl.vectorf (the data type that is expected by push_sample)
    # mysample = [random.random(), random.random(), random.random(),
    #             random.random(), random.random(), random.random(),
    #             random.random(), random.random()]

    channel1 = np.sin(1.0 * 2.0 * np.pi * time.time())  
    channel2 = np.cos(1.0 * 2.0 * np.pi * time.time())   
    channel3 = np.sin(10.0 * 2.0 * np.pi * time.time())   
    channel4 = np.cos(10.0 * 2.0 * np.pi * time.time())   
    channel5 = np.sin(15.0 * 2.0 * np.pi * time.time())   
    channel6 = np.cos(15.0 * 2.0 * np.pi * time.time())  
    channel7 = 1/time.time()
    # each channel have a voltage value over time.
    mysample = [channel1, channel2, channel3,
                channel4, channel5, channel6,
                channel7, random.random()]

    # now send it and wait for a bit
    outlet.push_sample(mysample)
    time.sleep(1.0/256.0)
