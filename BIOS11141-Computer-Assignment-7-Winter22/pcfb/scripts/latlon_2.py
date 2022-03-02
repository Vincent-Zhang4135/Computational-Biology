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
	if LineNumber > 0:
		# Remove the line ending characters
 		Line=Line.strip('\n')
 		
 		# Separate the line into a list of its tab-delimited components
 		LineList=Line.split('\t')
 		
		# Print the line
# 		print LineNumber,":", LineList
# 		print LineList[4], LineList[2], LineList[3]
		print "Depth: %s\tLat: %s\t Lon:%s" % (LineList[4], LineList[2], LineList[3])

	# Index the counter used to keep track of line numbers
	LineNumber = LineNumber + 1

# After the loop is completed, close the file
InFile.close()
