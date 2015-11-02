from framework.latentmodule import LatentModule
import random
import time
import datetime
import os

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
		
	def run(self):
		self.sleep(1)
		self.marker("Initialize")
		self.val = 0.5
		self.delta = 0.1
		self.cross = self.crosshair(duration=0.0, block=False, color = (0,0,0,1), size=0.15)
		self.sign = 1
		self.saw = 1
		
		# Clear SNAP setup text
		for clearline in range(1,100):
			print('\n')
		
		#self.righttop = self.rectangle(duration=0.0, block=False, color = (self.val,self.val,self.val,1), rect=(-0.75,-0.5, 0.5, -0.5))
		#self.rightmiddle = self.rectangle(duration=0.0, block=False, color = (self.val,self.val,self.val,1), rect=(-0.75,-0.5, 0.5, -0.5))
		#self.rightbottom = self.rectangle(duration=0.0, block=False, color = (self.val,self.val,self.val,1), rect=(-0.75,-0.5, 0.5, -0.5))
		
		# Wait to start
		print "Press space to begin..."
		self.waitfor('space')
		print "Starting..."
		
		for trialNum in range(450):
		
			# Wait for random length
			self.ITI = random.random()
			self.sleep(self.ITI)
			
			# Determine stimval
			self.trialrand = random.random()
			if self.trialrand < 0.2:
				self.stimval = self.val
				self.marker('Trial_'+str(trialNum)+'_Display_'+str(0)) 
			else:
				self.stimval = self.val+self.delta
				self.marker('Trial_'+str(trialNum)+'_Display_'+str(1))
			if self.stimval > 1:
				self.stimval = 1
			self.sleep(0.1)
			self.marker('Trial_'+str(trialNum)+'_Delta_'+str(self.delta))        
			self.sleep(0.1)
			self.marker('Trial_'+str(trialNum)+'_StimVal_'+str(self.stimval))
			
			# Start trial
			self.now = int(round(time.time() * 1000))
			self.marker('Trial_'+str(trialNum)+'_Start'+str(self.now))
			self.lefttop = self.rectangle(duration=0.0, block=False, color = (0,0,0,1), rect=(-0.91,-0.89, 0.25, 0.125))
			self.leftbottom = self.rectangle(duration=0.0, block=False, color = (0,0,0,1), rect=(-0.91,-0.89, -0.25, -0.125))
			self.pretime = int(round(time.time() * 1000))
			self.sleep(1+0.96*random.random())
			self.marker('Trial_'+str(trialNum)+'_Start_Stim_'+str(self.pretime))
			self.leftmiddle = self.rectangle(duration=0.04, block=True, color = (self.stimval,self.stimval,self.stimval,1), rect=(-0.904,-0.896, 0.004, -0.004))
			self.now = int(round(time.time() * 1000))
			self.marker('Trial_'+str(trialNum)+'_End_Stim_'+str(self.now))
			self.timeleft = (2500.0 - (self.now - self.pretime))/1000.0
			
			# Watch for response
			self.saw = self.watchfor('space',self.timeleft)
			self.marker('Trial_'+str(trialNum)+'_End_Watch_'+str(self.saw))
			self.saw = 1 if self.saw else 0
			if self.trialrand < 0.2:
				self.delta = self.delta
			else:
				# Determine delta
				if self.saw:
					self.delta = self.delta*0.75
				else:
					self.delta = self.delta*1.25
			if self.delta > 0.5:
				self.delta = 0.5
			self.marker('Trial_'+str(trialNum)+'_End_Watch_'+str(self.saw))
			
			self.lefttop = self.rectangle(duration=0.0, block=False, color = (0.5, 0.5, 0.5, 1), rect=(-0.91,-0.89, 0.25, 0.125))
			self.leftbottom = self.rectangle(duration=0.0, block=False, color = (0.5, 0.5, 0.5, 1), rect=(-0.91,-0.89, -0.25, -0.125))
			self.marker('Trial_'+str(trialNum)+'_End_Cues_'+str(self.saw))
			
			# Output data
			print "Trial Num: "+str(trialNum)+" Trial Delta: "+str(self.delta)+" Saw: "+str(self.saw).strip('[]')+" Presentation Time: "+str(self.pretime)+" StimVal: "+str(self.stimval)
			strlist = [str(trialNum), str(self.delta), str(self.saw), str(self.pretime), str(self.stimval)]
			strlist = ",".join(strlist)
			self.dataf = open(self.datafn, 'a')
			self.dataf.write(strlist+'\n')
			self.dataf.close()