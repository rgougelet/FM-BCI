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
        self.datafn = datetimenow+'_main.csv'
        self.dataf = open(self.datafn,'w')
        self.dataf.write('trialnum,stimtime,saw,delta,val'+'\n')
        self.dataf.close()        
        
    def run(self):
        self.marker("Initialize")
        self.val = 0.5
        self.delta = input("Input old delta: ")
        self.cross = self.crosshair(duration=0.0, block=False, color = (self.val,self.val,self.val,1))
        self.sign = 1
        self.saw = 1
        
        # Clear SNAP setup text
        for clearline in range(1,100):
            print('\n')
        
        # Wait to start
        print "Press space to begin..."
        self.waitfor('space')
        print "Starting..."
        
        for trialNum in range(450):
            # Wait for random length
            self.ISI = 1+3*random.random()
            self.sleep(self.ISI)
            
            # Start trial
            self.marker('Trial_'+str(trialNum)+'_Start')
            
            # Determine delta and flip direction
            #if self.saw:
            #    self.delta = self.delta*0.75
            #else:
            #    self.delta = self.delta*1.25
            if self.sign == 1:
                self.sign = -1
            else:
                self.sign = 1
            self.marker('Trial_'+str(trialNum)+'_Delta_'+str(self.delta))
            self.sleep(0.1)
            self.val = self.val+self.delta*self.sign
            self.marker('Trial_'+str(trialNum)+'_Val_'+str(self.val)) 
            
            # Change crosshair color
            self.pretime = int(round(time.time() * 1000))
            self.marker('Trial_'+str(trialNum)+'_Start_Stim_'+str(self.pretime))
            self.cross = self.crosshair(duration=0.0, block=False, color = (self.val,self.val,self.val,1))
            self.marker('Trial_'+str(trialNum)+'_End_Stim')
            
            # Watch for response
            self.saw = self.watchfor('space',1)
            self.saw = 1 if self.saw else 0
            self.marker('Trial_'+str(trialNum)+'_End_Watch_'+str(self.saw))
            
            # Output data
            print "Trial Num: "+str(trialNum)+" Trial Delta: "+str(self.delta)+" Saw: "+str(self.saw).strip('[]')+" Presentation Time: "+str(self.pretime)+" Val: "+str(self.val)
            strlist = [str(trialNum), str(self.delta), str(self.saw), str(self.pretime), str(self.val)]
            strlist = ",".join(strlist)
            self.dataf = open(self.datafn, 'a')
            self.dataf.write(strlist+'\n')
            self.dataf.close()