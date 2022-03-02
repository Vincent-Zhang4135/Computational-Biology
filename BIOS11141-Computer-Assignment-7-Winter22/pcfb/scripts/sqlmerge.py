#! /usr/bin/env python
""" 
sqlmerge.py
using the mysql database 'midwater', with its tables 'ctd' and 'specimens',
look up the dive and depth for each specimen, and extract the corresponding
temperature, salinity, and oxygen from the ctd table

output the combined results as a tab-delimited table
"""

import re        # Load regular expression module
import MySQLdb   # must be installed separately

# Create the database connection
# Often you will want to use a variable instead of a fixed string 
# for the database name
MyConnection = MySQLdb.connect( host = "localhost", user = "root", \
                                passwd = "", db = "midwater")
MyCursor = MyConnection.cursor()

SQL = """SELECT specimen_id,vehicle,dive,date,depth,lat,lon from specimens;"""
SQLLen = MyCursor.execute(SQL)  # returns the number of records retrieved

# MyCursor is now "loaded" with the results of the SQL command
# AllOut will become a list of all the records selected
AllOut = MyCursor.fetchall()   
# print AllOut

# Print the header line
print "Vehicle\tDive\tDate\tDepth\tLatitude\tLongitude\tTemperature\tSalinity\tOxygen"

# Step through each record and create a new SQL command to retrieve 
# the corresponding values from the other DB
for Index in range(SQLLen):
	# two dimensional indexing: 
	# from the Indexed record, take the first item (the primary_key)
	Spec_id = AllOut[Index][0]   
	
	# Other ways to print debugging information
#	vehicle,dive,date,depth,lat,lon = 	AllOut[Index][1:]
#   print "%s\t%d\t%s\t%.1f\t%.4f\t%.4f\t" % AllOut[Index][1:]
#	vehicle,dive,date, depth, lat,lon,

# insert spec_id (the primary key) into each command
	SQL = """SELECT MIN(ctd.depth),ctd.temperature,ctd.salinity,ctd.oxygen 
	from ctd, specimens where 
	specimens.specimen_id=%d and specimens.vehicle=ctd.vehicle and 	
	specimens.dive=ctd.dive and ctd.depth>specimens.depth ; """ % Spec_id
	
	# print SQL   ## Uncomment this line to test the command structure before running

	SQLLen = MyCursor.execute(SQL)
	NewOut = MyCursor.fetchall()

	if SQLLen < 1 or NewOut[0][0]==None:  # Some records don't have CTD data
		print  "%s\t%d\t%s\t%.1f\t%.4f\t%.4f\t" % AllOut[Index][1:] \
		   + "NaN\tNaN\tNaN"
	else:
		print  "%s\t%d\t%s\t%.1f\t%.4f\t%.4f\t" % AllOut[Index][1:] \
		   + "%.2f\t%.3f\t%.2f" % NewOut[0][1:]
# Close the files
MyCursor.close()
MyConnection.close()