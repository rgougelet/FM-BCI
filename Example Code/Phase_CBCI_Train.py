from framework.latentmodule import LatentModule
import    pylsl.pylsl    as    pylsl
import scipy as sp
import numpy as np
import pylab as pyl
import matplotlib.pyplot as plt
from scipy import signal as sig
from spectrum import *
import random, datetime, os, sys
import time as tm
from numpy import NaN, Inf, arange, isscalar, asarray, array
from scipy.optimize import curve_fit

class Main(LatentModule):
	def __init__(self):
		LatentModule.__init__(self)
		self.implicit_markers = False
		self.extensive_markers = False
		datetimenow = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
		datenow = datetime.datetime.now().strftime("%Y-%m-%d")
		self.datafn = datetimenow+'_training.csv'
		self.dataf = open(self.datafn,'w')
		self.dataf.write('trialnum,delta,saw,stimtime,stimval'+'\n')
		self.dataf.close()        
		base.win.setClearColor((0.5, 0.5, 0.5, 1))
		return
		
	def peakdet(self, input_vector, delta):
		maxtab = []
		mintab = []
		domain = arange(len(input_vector))
		input_vector = asarray(input_vector)
		nearest_min, nearest_max = Inf, -Inf
		nearest_min_pos, nearest_max_pos = NaN, NaN
		lookformax = True
		
		for sample_index in domain:
			sample = input_vector[sample_index]
			if sample > nearest_max:
				nearest_max = sample
				nearest_max_pos = domain[sample_index]
			if sample < nearest_min:
				nearest_min = sample
				nearest_min_pos = domain[sample_index]
			if lookformax:
					if sample < nearest_max-delta: # if passes vertical threshold
						# if not maxtab:
						maxtab.append(nearest_max_pos)
						nearest_min = sample
						nearest_min_pos = domain[sample_index]
						lookformax = False
						# else:
							# if (sample_index - maxtab[-1] > 136):
								# maxtab.append(nearest_max_pos)
								# nearest_min = sample
								# nearest_min_pos = domain[sample_index]
								# lookformax = False
			else:
				if sample > nearest_min+delta:
					# if not mintab:
					mintab.append(nearest_min_pos)
					nearest_max = sample
					nearest_max_pos = domain[sample_index]
					lookformax = True
					# else:
						# if (sample_index - mintab[-1] > 136):
							# mintab.append(nearest_min_pos)
							# nearest_max = sample
							# nearest_max_pos = domain[sample_index]
							# lookformax = True
		return maxtab, mintab # returns list of maxs and mins indices

	def sampledata(self,EEGinlet):
		# Initialize parameters
		EEGsample = pylsl.vectorf()
		srate = 2048.
		nyq = srate/2.0
		nsamples = self.nsamples # Number of samples to collect
		EEGwindow = np.zeros(nsamples)
		time = np.arange(nsamples)*(1.0/srate)
		
		## Clear buffer
		while EEGinlet.pull_sample(EEGsample,0.0): # Clear buffer
			pass
			
		## Sample data
		for sampleIndex in np.arange(0,nsamples):
			EEGinlet.pull_sample(EEGsample)
			EEGwindow[sampleIndex] = EEGsample[29]-EEGsample[48] # Reref, skip 0th channel
		self.before = tm.time()
		#plt.plot(time[:-1],EEGwindow[:-1],'b')
		
		EEGwindow = EEGwindow-np.mean(EEGwindow)
		#plt.figure(1)
		
		#Compute delay
		#window = len(self.bp)
		#delaysamples = 0.5*(window - 1.) # in samples
		#delaysecs = 0.5*(window - 1.)/srate
		
		# Compute alpha/spectrum power ratio
		#plt.plot(time, EEGwindow,'b')
		filtered_data = numpy.convolve(EEGwindow,self.bp,'same')
		f,psd = sp.signal.welch(filtered_data, fs=srate, window='hanning', nperseg=1024., nfft=2048, detrend='linear', return_onesided=True, scaling='density')
		#plt.plot(f,psd)
		#print f[12]
		#plt.show()
		alpha = psd[12] #input peak alpha frequency manually
		print alpha
		rest = np.delete(psd, 3)
		restmean = np.mean(rest)
		self.powers[self.sample] = alpha/restmean
		if alpha/restmean < 250.: #"empirically" determined
			print 'Skipped power'
			return
		
		maxtab, mintab = self.peakdet(filtered_data, 1)
		
		# Data visualization
		print len(self.EEGsectimes), len(filtered_data)
		plt.plot(self.EEGsectimes, EEGwindow,'b')
		plt.plot(self.EEGsectimes, filtered_data,'g')
		plt.plot(self.EEGsectimes[maxtab], filtered_data[maxtab],'ro')
		plt.plot(self.EEGsectimes[mintab], filtered_data[mintab],'bo')
		plt.show()
		
		# Predict next peak via median
		# self.peakdiffs.extend(np.diff(maxtab)) # Update diffs
		peakwidth = np.median(np.diff(maxtab)) # Find median diff from updated
		lastpeak = maxtab[-1]
		next2peak = 1*peakwidth - (self.nsamples - lastpeak) # in samples
		next2peaktime = (next2peak/self.srate) # in seconds
		
		# Predict next trough via median
		#self.troughdiffs.extend(np.diff(mintab)) # Update diffs
		troughwidth = np.median(np.diff(mintab)) # Find median diff from updated
		lasttrough = mintab[-1]
		next2trough = 1*troughwidth - (self.nsamples - lasttrough) # in samples
		next2troughtime = (next2trough/self.srate) # in seconds
		
		# Predict within window
		# self.peakdiffs.extend(np.diff(maxtab[:-2]))
		# lastpeak = maxtab[-3]
		# off1 = (lastpeak + peakwidth)-maxtab[-2]
		# off2 = (lastpeak + 2*peakwidth)-maxtab[-1]
		# print off1, off2
		
		# Samples/cycle = 171
		# Milliseconds/cycle = 83.33
		
		# if not 100 < peakwidth < 120 or not 100 < troughwidth < 120:
			# print 'Skipped diff threshold'
			# return
			
		# Send marker at peak or trough
		self.after = tm.time()
		
		now = tm.time()
		if now >= self.before+next2peaktime and now >= self.before+next2troughtime:
			print 'Skipped too late'
			return
		else:
			while True:
				if now < self.before+next2peaktime and now < self.before+next2troughtime:
					now = tm.time()
					pass
				else:
					if now < self.before+next2peaktime:
						print 'Peak'
						self.marker('Peak')
						break
					if now < self.before+next2troughtime:
						print 'Trough'
						self.marker('Trough')
						break
		print (self.after-self.before)*1000.
		
		return
		
	def run(self):
		self.sleep(1)
		## Clear SNAP setup text
		for clearline in range(1,100):
			print('\n')
		
		## Initialize file saving
		datetimenow = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
		datenow = datetime.datetime.now().strftime("%Y-%m-%d")
		self.datafn = '.\\modules\\CBCI\\CSV\\'+datetimenow+'_training.csv'
		self.dataf = open(self.datafn,'w')
		self.dataf.close()
		
		self.srate = 2048.
		self.nyq = self.srate/2.0
		self.nsamples = 2048 # Number of samples to collect
		self.peakdiffs = []
		self.troughdiffs = []
		
		## Generate PM FIR filter coefficients
		self.center = 12
		self.lowcut = self.center-2
		self.highcut = self.center+2
		self.numtaps = 1024
		self.nyq = 0.5 * self.srate #nyquist frequency - see http://www.dspguide.com/ if you want more info
		self.bp = sig.remez(self.numtaps,[0, self.lowcut, self.center, self.center, self.highcut, self.nyq],[0, 1, 0], Hz=self.srate, type='bandpass') # FIR
		print '# of coeffs:', len(self.bp)
		print 'Filter order:', self.numtaps
		self.delaysamples = 0.5*(len(self.bp) - 1.) # in samples
		self.delaysecs = 0.5*(len(self.bp) - 1.)/self.srate
		self.padlength = round(self.delaysamples)
		self.EEGtimes = np.linspace(0.0,float(self.nsamples+self.padlength)/self.srate, num=self.nsamples+self.padlength)*1000.0
		self.EEGsectimes = np.linspace(0.0,float(self.nsamples)/self.srate, num=self.nsamples)
	
		## Check frequency response
		# w,h = sig.freqz(self.bp,1)
		# plt.figure
		# plt.plot(w*self.nyq/np.pi, 20*np.log10(abs(h)))
		# plt.show()
		
		## Probe EEG stream
		print("Looking for EEG...")
		EEG = pylsl.resolve_stream('type','EEG')
		if not EEG:
			print "No EEG stream resolved, operating without it\n"
		else:
			## Initialize EEG stream
			print "EEG stream resolved\n"
			self.powers = numpy.zeros((9999,))
			EEGinlet = pylsl.stream_inlet(EEG[0], 1)
			EEGinlet.open_stream()
			for self.sample in range(0,9999):
				self.sampledata(EEGinlet)
			# q75, q25 = np.percentile(self.powers, [75 ,25])
			# print q25, q75, (q75 - q25)
			# print np.median(self.powers) 
				
		#self.marker("Initialize")
		#self.val = 0.5
		#self.delta = 0.1
		#self.cross = self.crosshair(duration=0.0, block=False, color = (0,0,0,1), size=0.15) #Psychtoolbox
		#self.sign = 1
		#self.saw = 1
		
		#plt.figure(2)
		#plt.show()
		
		# Positions
		# #self.righttop = self.rectangle(duration=0.0, block=False, color = (self.val,self.val,self.val,1), rect=(-0.75,-0.5, 0.5, -0.5))
		# #self.rightmiddle = self.rectangle(duration=0.0, block=False, color = (self.val,self.val,self.val,1), rect=(-0.75,-0.5, 0.5, -0.5))
		# #self.rightbottom = self.rectangle(duration=0.0, block=False, color = (self.val,self.val,self.val,1), rect=(-0.75,-0.5, 0.5, -0.5))
		
		# # Wait to start
		#print "Press space to begin..."
		#self.waitfor('space')
		#print "Starting..."
		#for trialNum in range(450):
		
			# # Wait for random length
		#	self.ITI = random.random()
		#	self.sleep(self.ITI)
			
			# # Determine stimval
		#	self.trialrand = random.random()
		#	if self.trialrand < 0.2:
		#		self.stimval = self.val
		#		self.marker('Trial_'+str(trialNum)+'_Display_'+str(0)) 
		#	else:
		#		self.stimval = self.val+self.delta
		#		self.marker('Trial_'+str(trialNum)+'_Display_'+str(1))
		#	if self.stimval > 1:
		#		self.stimval = 1
		#	self.sleep(0.1)
		#	self.marker('Trial_'+str(trialNum)+'_Delta_'+str(self.delta))        
		#	self.sleep(0.1)
		#	self.marker('Trial_'+str(trialNum)+'_StimVal_'+str(self.stimval))
			
			# # Start trial
			#self.now = int(round(tm.time() * 1000))
			#self.marker('Trial_'+str(trialNum)+'_Start_'+str(self.now))
			#self.lefttop = self.rectangle(duration=0.0, block=False, color = (0,0,0,1), rect=(-0.91,-0.89, 0.25, 0.125)) #Psychtoolbox
			#self.leftbottom = self.rectangle(duration=0.0, block=False, color = (0,0,0,1), rect=(-0.91,-0.89, -0.25, -0.125)) #Psychtoolbox
			#self.pretime = int(round(tm.time() * 1000))
			#self.sleep(1+0.96*random.random())
			#self.marker('Trial_'+str(trialNum)+'_Start_Stim_'+str(self.pretime))
			#self.leftmiddle = self.rectangle(duration=0.04, block=True, color = (self.stimval,self.stimval,self.stimval,1), rect=(-0.904,-0.896, 0.004, -0.004)) #Psychtoolbox
			#self.now = int(round(tm.time() * 1000))
			#self.marker('Trial_'+str(trialNum)+'_End_Stim_'+str(self.now))
			#self.timeleft = (2500.0 - (self.now - self.pretime))/1000.0
			
			# # Watch for response
			#self.saw = self.watchfor('space',self.timeleft)
			#self.marker('Trial_'+str(trialNum)+'_End_Watch_'+str(self.saw))
			#self.saw = 1 if self.saw else 0
			
			#self.marker('Trial_'+str(trialNum)+'_End_Watch_'+str(self.saw))
			
			#self.lefttop = self.rectangle(duration=0.0, block=False, color = (0.5, 0.5, 0.5, 1), rect=(-0.91,-0.89, 0.25, 0.125)) #Psychtoolbox
			#self.leftbottom = self.rectangle(duration=0.0, block=False, color = (0.5, 0.5, 0.5, 1), rect=(-0.91,-0.89, -0.25, -0.125)) #Psychtoolbox
			#self.marker('Trial_'+str(trialNum)+'_End_Cues_'+str(self.saw))
			
			# # Output data
			#print "Trial Num: "+str(trialNum)+" Trial Delta: "+str(self.delta)+" Saw: "+str(self.saw).strip('[]')+" Presentation Time: "+str(self.pretime)+" StimVal: "+str(self.stimval)
			#strlist = [str(trialNum), str(self.delta), str(self.saw), str(self.pretime), str(self.stimval)]
			#strlist = ",".join(strlist)
			#self.dataf = open(self.datafn, 'a')
			#self.dataf.write(strlist+'\n')
			#self.dataf.close()
			
			# # Determine delta
			#if self.trialrand < 0.2:
			#	self.delta = self.delta
			#else:
			#	if self.saw:
			#		self.delta = self.delta*0.75
			#	else:
			#		self.delta = self.delta*1.25
			#if self.delta > 0.5:
			#	self.delta = 0.5