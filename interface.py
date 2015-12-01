from framework.latentmodule import LatentModule
import imp
#pylsl = imp.load_source('pylsl.py', 'C:\Users\ces\Dropbox\LSE\Code\SNAP\src\modules\FM-BCI\pylsl\pylsl.py')
pylsl = imp.load_source('pylsl.py', 'C:\Users\ces\Documents\SNAP_FMBCI\src\modules\FM-BCI\pylsl\pylsl.py')

import random
import time

class Main(LatentModule):
    def __init__(self):
        LatentModule.__init__(self)

    def run(self):

        for clearline in range(1,100):
            print('\n')
    
        # initialize data stream
        print("Looking for BCI stream...")
        streams = pylsl.resolve_stream('name', 'BCI_Stream')
        print("Stream found.")
        inlet = pylsl.StreamInlet(streams[0])

        # Extract stream info
        inf = inlet.info()
        sampleRate = inf.nominal_srate()
        numOfChannel = inf.channel_count()
        sample = pylsl.vectorf()

        ## Set markers up
        self.implicit_markers = False
        self.extensive_markers = False

        ## Sets background color to gray
        base.win.setClearColor((0.75, 0.75, 0.75, 1))
        cross = self.crosshair(0,size=0.2,width=0.005,block=False)

        while True:
            bci, timestamp = inlet.pull_sample()
            self.marker("NewFrame_"+str(bci)+"_"+str(timestamp))
            rect1 = self.rectangle([-0.4,-0.6,(bci[0]*1.5)-0.75,-0.75],duration=1000,color=[0,0,0,1],block=False)
            rect2 = self.rectangle([0.4,0.6,(bci[0]*1.5)-0.75,-0.75],duration=1,color=[0,0,0,1],block=True)
            rect1.destroy()