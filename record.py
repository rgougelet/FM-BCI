import os
import errno
import time
import shutil

class Record(object):

    target = None

    def __init__(self):
        self.create_directory("./recordings")
        # filename = raw_input("Please enter a file name for this recording: ")
        filename = time.strftime("%H:%M:%S-%d-%m-%Y")
        self.target = open (os.path.join("./recordings", filename + ".txt"), 'a') ## a will append, w will over-write
        self.target.write("EEG recorded on "+ time.strftime("%d/%m/%Y")+ " at "+time.strftime("%H:%M:%S")+"\n\n\n")


    def create_directory(self, path):
        """create directories for eeg recordings
        """
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
       
    def write(self, content):
        if self.target != None:
            self.target.write('%s' % content)
            self.target.write("\n")

    def deleteRecordings(self):
        shutil.rmtree('./recordings')


    #providing name for the file to be created
    def begin_recording(self):
        create_directory("./recordings")
        # filename = raw_input("Please enter a file name for this recording: ")
        filename = time.strftime("%H:%M:%S-%d-%m-%Y")
        target = open (os.path.join("./recordings", filename + ".txt"), 'a') ## a will append, w will over-write 
        

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
# # r1.deleteRecordings()
# r1.write("frequency")
