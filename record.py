import os
import errno

def create_directory(path):
    """create directories for eeg recordings
    """
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
   

#providing name for the file to be created
def begin_recording():
    create_directory("./recordings")
    filename = raw_input("Please enter a file name for this recording: ")
    filename = "1"
    target = open (os.path.join("./recordings", filename + ".txt"), 'a') ## a will append, w will over-write 
    
#providing the content for the file
# print "provide three lines of content for the file:"
# line1 = raw_input("line 1: ")
# line2 = raw_input("line 2: ")
# line3 = raw_input("line 3: ")
# #writing the entered content to the file we just created
# print "entered three lines are written to the file"
# target.write(line1)
# target.write("n")
# target.write(line2)
# target.write("n")
# target.write(line3)
# target.write("n")
# #providing information that writing task is completed
# print "we have added those text to the file"
# target.close()