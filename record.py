import os
import errno
import time
import shutil
import numpy as np
import platform

# Example Usage: 
# recorder = record.Recorder()  # create the recorder 
# recorder.record_new()         # create new recording txt
# recorder.write('first line')   # to the txt file

class Recorder:

    def __init__(self, nameExtra = "", overrideName = False):
        if platform.system() == "Windows":
            print "Writing on Windows system..."
            self.create_directory(".\\recordings")
            self.saved_directory = ".\\recordings\\"
            if not overrideName:
                self.file_name = self.saved_directory + time.strftime("%Y-%m-%d_%H-%M-%S",)+nameExtra+".txt"
            else:
                self.file_name = self.saved_directory+nameExtra+".txt"

        else:
            self.create_directory("./recordings")
            self.saved_directory = "./recordings/"
            if not overrideName:
                self.file_name = self.saved_directory + time.strftime("%Y-%m-%d_%H-%M-%S",)+nameExtra+".txt"
            else:
                self.file_name = self.saved_directory+nameExtra+".txt"
    def create_directory(self, path):
        """ create directories for eeg recordings"""
        try:
            print "Making directory"
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

    def write(self, content):
        with open(self.file_name, 'a') as self.target_file:
            self.target_file.write('%s' % content)
            self.target_file.write("\n")

    def delete_recordings(self):
        shutil.rmtree('./recordings')

    #providing name for the file to be created
    def record_new(self):
        with open(self.file_name, 'a') as self.target_file: # a will append, w will over-write
            self.target_file.write("EEG recorded on "+ time.strftime("%d/%m/%Y")+ " at "+time.strftime("%H:%M:%S")+"\n\n\n")

    # used to create a raw file quickly
    def record_raw(self, content):
        """ output raw matrix to the file without brackets or commas"""
        np.savetxt(self.file_name,content,fmt='%.5f') # %.5f specifies 5 decimal round
        f = open(self.file_name)
        if f.close == False:
            f.close()
        for clearline in range(1,10):   print('\n')
        print "\nData has been recorded and saved in:   " + str(self.file_name) 
        for clearline in range(1,10):   print('\n')   

    # def write_test(self):
    #     # providing the content for the file
    #     print "provide three lines of content for the file:"
    #     line1 = raw_input("line 1: ")
    #     line2 = raw_input("line 2: ")
    #     line3 = raw_input("line 3: ")
    #     #writing the entered content to the file we just created
    #     print "entered three lines are written to the file"
    #     self.target_file.write(line1)
    #     self.target_file.write("n")
    #     self.target_file.write(line2)
    #     self.target_file.write("n")
    #     self.target_file.write(line3)
    #     self.target_file.write("n")
    #     #providing information that writing task is completed
    #     print "we have added those text to the file"
    #     self.target_file.close()


