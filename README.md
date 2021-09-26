# HomeworkSort

This file will parse files directly from Sakai to obtain only the files you are interested in. 

To run this file, 3 variables must be edited in the code

1) path_from_parent_to_source
2) path_from_parent_to_destination
3) Student

The first two variables are the paths from the current directory (i.e. directory that contains HomeworkSorter) to the source files and destination files, respectively. These directories must already exist. 

The 3rd variable is a dictionary that contains private student information. Entries are in the format 'Last, First(netid@duke.edu)': Last. If multiple students have the same last name, the first initial is appended to the value (i.e. Knox becomes KnoxM). To obtain this dictionary, please contact the publisher of this file. 
