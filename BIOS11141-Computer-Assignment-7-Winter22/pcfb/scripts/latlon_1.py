#!/usr/bin/env python

# Set the input file name
# (The program must be run from within the directory 
# that contains this data file)
InFileName = 'Marrus_claudanielis.txt'

# Open the input file for reading
InFile = open(InFileName, 'r')

# Initialize the counter used to keep track of line numbers
LineNumber = 0

# Loop through each line in the file
for Line in InFile:
	# Remove the line-ending characters
	Line=Line.strip('\n')
	# Print the line
	print LineNumber,":", Line
		
	# Index the counter used to keep track of line numbers
	LineNumber = LineNumber + 1

# After the loop is completed, close the file
InFile.close()