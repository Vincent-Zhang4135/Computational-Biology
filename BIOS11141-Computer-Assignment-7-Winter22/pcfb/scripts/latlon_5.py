#! /usr/bin/env python
# latlon_5.py - for use in Chapter 10 PCfB
# 	
# This program reads in a file containing several columns of data, 
# and returns a file with decimal converted value and selected data fields.
# The process is: Read in each line of the example file, split it into
# separate components, and write certain output to a kml file
# that can be read by Google Earth

import re # Load regular expression module
# Functions must be defined before they are used
def decimalat(DegString):
	# This function requires that the re module is loaded
	# Take a string in the format "34 56.78 N" and return decimal degrees
	SearchStr='(\d+) ([\d\.]+) (\w)' 
	Result = re.search(SearchStr, DegString)

	# Get the (captured) character groups from the search
	Degrees = float(Result.group(1))
	Minutes = float(Result.group(2))
	Compass = Result.group(3).upper() # make sure it is capital too

	# Calculate the decimal degrees
	DecimalDegree = Degrees + Minutes/60

	if Compass == 'S' or Compass == 'W':
		DecimalDegree = -DecimalDegree  
	return DecimalDegree
# End of the function definition

# Set the input file name
InFileName = 'Marrus_claudanielis.txt'

# Derive the output file name from the input file name
OutFileName = InFileName + ".kml"

# Give the option to write to a file or just print to screen
WriteOutFile = True

# Open the input file
InFile = open(InFileName, 'r')

# Open the header to the output file. Do this outside the loop
HeadString='''<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<kml xmlns=\"http://earth.google.com/kml/2.2\">
<Document>'''

if WriteOutFile:
	OutFile = open(OutFileName, 'w') 	# Open the output file
	OutFile.write(HeadString)
else:
	print HeadString

# Initiate the counter used to keep track of line numbers
LineNumber = 0

# Loop over each line in the file
for Line in InFile:
	# Check the line number, process if you are past the first line (number == 0)
	if LineNumber > 0:
		# Remove the line ending characters
		# print line  # uncomment for debugging
		Line = Line.strip('\n')

		# Split the line into a list of ElementList, using tab as a delimiter
		ElementList = Line.split('\t')
		
		# Returns a list in this format:
		# ['Tiburon 596', '19-Jul-03', '36 36.12 N', '122 22.48 W', '1190', 'holotype']
		# print "ElementList:", ElementList  # uncomment for debugging

		Dive    = ElementList[0]
		Date    = ElementList[1]
		Depth   = ElementList[4]  # A string, not a number
		Comment = ElementList[5]

		LatDegrees = decimalat(ElementList[2])
		LonDegrees = decimalat(ElementList[3])
# Indentation for triple-quoted strings does not have to 
# follow normal python rules, although the variable name
# itself has to appear on the proper line
		PlacemarkString = '''
<Placemark>
 <name>Marrus - %s</name>
 <description>%s</description>
 <Point>
  <altitudeMode>absolute</altitudeMode>
  <coordinates>%f, %f, -%s</coordinates>
 </Point>
</Placemark>''' % (Dive, Line, LonDegrees, LatDegrees, Depth)
		
		# Write the PlacemarkString to the output file
		if WriteOutFile:
			OutFile.write(PlacemarkString)
		else: 
			print PlacemarkString
		
	LineNumber += 1 # This is outside the if, but inside the for loop
	
# Close the files
InFile.close()
if WriteOutFile:
	print "Saved",LineNumber,"records from",InFileName, "as", OutFileName 
	# After all the records have been printed, 
	# write the closing tags for the kml file
	OutFile.write('\n</Document>\n</kml>\n')
	OutFile.close()
else:
	print '\n</Document>\n</kml>\n'
