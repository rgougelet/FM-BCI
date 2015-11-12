"""Example program to demonstrate how to send a multi-channel time series to
LSL."""

import random
import time
import math

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

    channel1 = math.sin(time.time())  # a function of voltage
    channel2 = math.cos(time.time())
    channel3 = 1/time.time()
    # each channel have a voltage value over time.
    mysample = [channel1, channel2, channel3,
                random.random(), random.random(), random.random(),
                random.random(), random.random()]

    # now send it and wait for a bit
    outlet.push_sample(mysample)
    time.sleep(1.0/256.0)
