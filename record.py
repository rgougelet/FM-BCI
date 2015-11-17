import os
import errno
import time
import shutil
import numpy as np

class Record:
    target = None     # the target file to write to

    def __init__(self):
        self.create_directory("./recordings")


    def create_directory(self, path):
        """ create directories for eeg recordings"""
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
       

    def write(self, content):
        if self.target != None:
            self.target.write('%s' % content)
            self.target.write("\n")


    def record_raw(self, content):
        filename = time.strftime("./recordings/%H:%M:%S-%d-%m-%Y")
        # %.5f specifies 5 decimal round
        np.savetxt(filename,content,fmt='%.5f')    


    def delete_recordings(self):
        shutil.rmtree('./recordings')


    #providing name for the file to be created
    def record_new(self):
        # filename = raw_input("Please enter a file name for this recording: ")
        filename = time.strftime("%H:%M:%S-%d-%m-%Y")
        self.target = open (os.path.join("./recordings", filename + ".txt"), 'a') ## a will append, w will over-write
        self.target.write("EEG recorded on "+ time.strftime("%d/%m/%Y")+ " at "+time.strftime("%H:%M:%S")+"\n\n\n")
        

    # def writeTest(self):
    #     # providing the content for the file
    #     print "provide three lines of content for the file:"
    #     line1 = raw_input("line 1: ")
    #     line2 = raw_input("line 2: ")
    #     line3 = raw_input("line 3: ")
    #     #writing the entered content to the file we just created
    #     print "entered three lines are written to the file"
    #     self.target.write(line1)
    #     self.target.write("n")
    #     self.target.write(line2)
    #     self.target.write("n")
    #     self.target.write(line3)
    #     self.target.write("n")
    #     #providing information that writing task is completed
    #     print "we have added those text to the file"
    #     self.target.close()


# r1 = Record()
# # r1.delete_recordings()
# r1.write("frequency")
