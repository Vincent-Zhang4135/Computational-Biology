#! /usr/bin/env python
""" 
mylatlon_4.py
import latitude longitude records from a text file, 
format them into an SQL command, and enter the records into a database
"""

import re # Load regular expression module
from datetime import datetime # Load datetime class from the datetime module
import MySQLdb

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

# Open the input file
InFile = open(InFileName, 'r')

# Initialize the counter used to keep track of line numbers
LineNumber = 0

# Create the database connection
# Often you will want to use a variable instead of a fixed string 
# for the database name
MyConnection = MySQLdb.connect( host = "localhost", user = "root", \
     passwd = "", db = "midwater")
MyCursor = MyConnection.cursor()

# Loop over each line in the file
for Line in InFile:
	# Check the line number, process if past the first line (number == 0)
	if LineNumber > 0:
		 # Remove the line ending characters
		 # print line  # uncomment for debugging
		 Line = Line.strip('\n')
		 # Split the line into a list of ElementList, using tab as a delimiter
		 ElementList = Line.split('\t')
		 # Returns a list in this format:
		 # ['Tiburon 596', '19-Jul-03', '36 36.12 N', '122 22.48 W', 
		 # '1190', 'holotype']
		
		 Dive    = ElementList[0] # includes vehicle and dive number
		 Date    = ElementList[1]
		 Depth   = float(ElementList[4])
		 Comment = ElementList[5]
		
		 LatDegrees = decimalat(ElementList[2])
		 LonDegrees = decimalat(ElementList[3])
		
		 #Isolate the vehicle and dive number from the Dive field
		 SearchStr='(.+?) (\d+)'
		 Result = re.search(SearchStr, Dive)
		 Vehicle = Result.group(1)
		 DiveNum = int(Result.group(2))
		
		 #Reformat date
		 # Create a datetime object from a string
		 DateParsed = datetime.strptime(Date, "%d-%b-%y") 
		 # Create a string from a datetime object
		 DateOut = DateParsed.strftime("%Y-%m-%d") 
		 #print Vehicle, DiveNum, DateOut, LatDegrees, LonDegrees, Depth, Comment
		 SQL = """INSERT INTO specimens SET
  vehicle='%s',
  dive=%d,
  date='%s',
  lat=%.4f,
  lon=%.4f,
  depth=%.1f,
  notes='%s'
""" % (Vehicle, DiveNum, DateOut, LatDegrees, LonDegrees, Depth, Comment)
		 print SQL
		#     MyCursor.execute(SQL)
	LineNumber += 1 # This is outside the if, but inside the for loop

# Close the files
InFile.close()
MyCursor.close()
# The .commit() command below is not in the printed book. 
# It is needed by some installations to make the changes stick
MyConnection.commit()
MyConnection.close()

