import shutil
import sys
import os
from shutil import copyfile
from PIL import Image

# Define this before we run! AKA if you are not Matt Knox, define these values
path_from_parent_to_source = 'Student Work Ungraded'
# As an example, I have a directory that contains this script and a folder called 'Student Work Ungraded'. 
# Within 'Student Work Ungraded' is the file 'Homework #_', which is downloaded straight from Sakai. 
path_from_parent_to_destination = 'Transfer Files'
# As an example, the directory that contains this script contains a directory called 'Transfer Files'
# A directory will be created within 'Transfer Files' that contains the new files


# Make sure we have the right syntax
numargs = len(sys.argv)
if numargs != 3:
    print('Syntax: python StudentSorter.py <HW_num> <part_num>')
    quit()


# check if one text in list is in item
def mychecker(txtsearch, item):
    for txt in txtsearch:
        if txt in item:
            return True
    return False


# Get arguments
input_hw_num = sys.argv[1]
input_part_num = sys.argv[2]

# Parse arguments
try:
    hw_num = int(input_hw_num)
except ValueError:
    print(input_hw_num, 'is not a valid instance of <HW_num>')
    quit()

try:
    part_num = int(input_part_num)
except ValueError:
    print(input_part_num, 'is not a valid instance of <part_num>')

if hw_num < 1 or hw_num > 12:
    print(hw_num, 'is not a valid homework number. Only homeworks 1-12 are valid.')
    quit()
if part_num < 1 or part_num > 3:
    print(part_num, 'is not a valid part number. Only parts 1-3 are valid.')
    quit()

# Create paths
sakai_download_directory = 'Homework #' + str(hw_num)
path_to_parent = os.path.normpath(os.path.join(os.path.realpath(__file__), '..'))
temp_path_to_source = os.path.join(path_to_parent, path_from_parent_to_source)
path_to_source = os.path.join(path_to_parent, path_from_parent_to_source, sakai_download_directory)

# Parse paths
if not os.path.isdir(temp_path_to_source):
    print('It appears that', path_from_parent_to_source,
          'is not a valid relative path to the source files. Please check the first few lines of this code to ensure '
          'it is correct.')
    quit()
if not os.path.isdir(path_to_source):
    print('Homework', hw_num, 'has not been downloaded yet! Please visit Sakai and download to', temp_path_to_source)
    quit()
if not os.path.isdir(os.path.join(path_to_parent, path_from_parent_to_destination)):
    print('It appears that', path_from_parent_to_destination,
          'is not a valid relative path to the destination files. Please check the first few lines of this code to '
          'ensure it is correct.')
    quit()
path_to_destination = os.path.join(path_to_parent, path_from_parent_to_destination,
                                   'HW ' + str(hw_num) + ' Part ' + str(part_num)) + '/'

# Remove directory if it already exists
if os.path.isdir(path_to_destination):
    shutil.rmtree(path_to_destination)
os.mkdir(path_to_destination)

txtsearch = ['part', 'part ', 'part#', 'part #', 'part_', 'pt', 'pt ', 'pt#', 'pt #', 'pt_']
txtsearch = [s + str(part_num) for s in txtsearch]

# Define directory paths
Students = {}

if not Students:
    print('You have not appended student directory paths. Please contact the publisher of this file for private information.')
    quit()

successcount = 0
totalcount = len(Students.values())
studentsThatTurnedIn = []
allmoved = []
try:
    for filename in os.listdir(path_to_source):  # For every student
        if filename == '.DS_Store':
            continue
        lastname = Students.get(filename)
        studentsThatTurnedIn.append(lastname)
        if filename not in Students:  # If we cannot find the student
            print('Could not create file for', filename, ', could not find filename in dictionary')
            continue
        path_to_student_documents = os.path.join(path_to_source, filename,
                                                 'Submission attachment(s)')  # Locate directory of homework files
        for item in os.listdir(path_to_student_documents):  # Go through all three files
            if mychecker(txtsearch, item.lower()):
                # convert to pdf if necessary
                if 'pdf' not in item:
                    if 'jpeg' in item or 'png' in item:
                        extension = 'jpeg'
                        if 'png' in item:
                            extension = 'png'
                        print('Reminder:', lastname, 'should not submit', extension, 'files.')
                        path_to_image = os.path.join(path_to_student_documents, item)
                        image1 = Image.open(path_to_image)
                        im1 = image1.convert('RGB')
                        path_to_pdf = path_to_image.replace(extension, 'pdf')
                        im1.save(path_to_pdf)
                        item = item.replace(extension, 'pdf')
                oldfilepath = os.path.join(path_to_student_documents, item)
                newfilename = lastname + '_HW' + str(hw_num) + '_Part' + str(
                    part_num) + '_feedback.pdf'  # Create the new file name
                newfilepath = os.path.join(path_to_destination, newfilename)
                copyfile(oldfilepath, newfilepath)  # copy the file
                allmoved.append(lastname)
                successcount += 1
                break
except FileNotFoundError:
    print('Homework', hw_num,
          'has not been downloaded yet! Please visit Sakai and download to the appropriate location.')
    quit()
print('Successfully moved', successcount, 'of', totalcount, 'files.')
allmoved.sort()
notmoved = set(Students.values()) - set(allmoved)

if successcount != totalcount:
    print('*******************************')
    print('                               ')
    print('ALERT: THE FOLLOWING FILES WERE NOT MOVED')
    for item in notmoved:
        print(item)
    print('                               ')
    print('*******************************')
    print('Suggestions:')
    for item in notmoved:
        errmsg = item
        if item in studentsThatTurnedIn:
            errmsg += ' formatted incorrectly.'
        else:
            errmsg += ' did not turn in.'
        print(errmsg)
