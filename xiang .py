# -*- coding: utf-8 -*-
""" doing the pre processing of the BCI layer stear"""
"""
Created on Sun Nov 08 23:23:07 2015

@author: wang sky
"""
from pylsl import StreamInlet, resolve_stream

# first resolve an EEG stream on the lab network
print("looking for an EEG stream...")
streams = resolve_stream('type', 'EEG')



# createto read from the stream
inlet = StreamInlet(streams[0])
while inlet.pull_sapmle(inlet, 0.0):
     pass 
 
while True:
    sample, timestamp = inlet.pull_sample();
 print(timestamp , sample)
sleep (0.5)   
#==============================================================================
#     SamMa = sample. shape 
#  for i in sample (i,:)
#      channel[i] = sample[i,:]
#==============================================================================
     
#==============================================================================
#     #detrend
#     def detrend(data,degree=10):
#         detrended=[None]*degree
#         for i in range(degree,len(data)-degree):
#                 chunk=data[i-degree:i+degree]
#                 chunk=sum(chunk)/len(chunk)
#                 detrended.append(data[i]-chunk)
#         return detrended+[None]*degree
#     sample  = sample(detrend , degree=3)
#     # filter
# from scipy.signal import butter, lfilter   
# 
# bandlow =1 
# bandhigh=30
# orderfilter=4
#  def butter_bandpass_filter(data, lowcut, highcut, fs, order=2):
#     b, a = butter_bandpass(lowcut, highcut, fs, order)
#     y = lfilter(b, a, data)
#     return y
# 
#  samplilt = butter_bandpass_filter(sample,bandlow, bandhigh, 256,orderfilter)
# import numpy as np
# from numpy.fft import fft
#    data1 = np.fft.fft(samplit, len(data1)*2)
#    
#    np.hstack((spec, data1))
#==============================================================================
#==============================================================================
#    
# alphafre = [i for i in data[1], if 7.5< i < 13];
# new_data = data[alfphafre,:]
#==============================================================================


 