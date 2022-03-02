#! /usr/bin/env python
# latlon_4.py - for use in Chapter 10 PCfB
# 	
# This program reads in a file containing several columns of data, 
# and returns a file with decimal converted value and selected data fields.
# The process is: Read in each line of the example file, split it into
# separate components, and write certain output to a separate file

import re # Load regular expression module


# Functions must be defined before they are used
def decimalat(DegString):
	# This function requires that the re module is loaded
	# Take a string in the format "34 56.78 N" and return decimal degrees
	SearchStr='(\d+) ([\d\.]+) (\w)'
	Result = re.search(SearchStr, DegString)

	# Get the captured character groups, as defined by the parentheses
	# in the regular expression, convert the numbers to floats, and 
	# assign them to variables with meaningful names
	Degrees = float(Result.group(1))
	Minutes = float(Result.group(2))
	Compass = Result.group(3).upper() # make sure it is capital too

	# Calculate the decimal degrees
	DecimalDegree = Degrees + Minutes/60

	# If the compass direction indicates the coordinate is South or
	# West, make the sign of the coordinate negative

	if Compass == 'S' or Compass == 'W':
		DecimalDegree = -DecimalDegree  
	return DecimalDegree
# End of the function definition

# Set the input file name
InFileName = 'Marrus_claudanielis.txt'

# Derive the output file name from the input file name
OutFileName = 'dec_' + InFileName

# Give the option to write to a file or just print to screen
WriteOutFile = True

# Open the input file
InFile = open(InFileName, 'r')

HeaderLine = 'dive\tdepth\tlatitude\tlongitude\tdate\tcomment'
print HeaderLine

# Open the output file. Do this outside the loop
if WriteOutFile:
	# Open the output file
	OutFile = open(OutFileName, 'w')
	OutFile.write(HeaderLine + '\n')

# Initialize the counter used to keep track of line numbers
LineNumber = 0

# Loop over each line in the file
for Line in InFile:
	# Check the line number, don't consider if it is first line
	if LineNumber > 0:
		# Remove the line ending characters
		# print line  # uncomment for debugging
		Line=Line.strip('\n')

		# Split the line into a list of ElementList, using tab as a delimiter
		ElementList = Line.split('\t')
	
		# Returns a list in this format:
		# ['Tiburon 596', '19-Jul-03', '36 36.12 N', '122 22.48 W', '1190', 'holotype']
		# print "ElementList:", ElementList  # uncomment for debugging

		Dive    = ElementList[0]
		Date    = ElementList[1]
		Depth   = ElementList[4]
		Comment = ElementList[5]

		LatDegrees = decimalat(ElementList[2])
		LonDegrees = decimalat(ElementList[3])
		# Create string to 5 decimal places, padded to 10 total characters
		# (using line continuation character \)
		OutString = "%s\t%4s\t%10.5f\t%10.5f\t%9s\t%s" % \
                         (Dive,Depth,LatDegrees,LonDegrees,Date,Comment)
		print OutString
		if WriteOutFile:
			OutFile.write(OutString + '\n') # remember the line feed!
		
	# another way to say LineNumber=LineNumber+1...
	LineNumber += 1 # this is outside the if, but inside the for loop
	
# Close the files
InFile.close()
if WriteOutFile:
	OutFile.close()