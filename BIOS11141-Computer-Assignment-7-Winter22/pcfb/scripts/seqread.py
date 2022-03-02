#!/usr/bin/env python

Usage="""
seqread.py - version 1
Reads in a file in fasta format into a list
and a dictionary.

The input file has the format 
>name2
sequence1sequence1
>name2
sequence2sequence2
sequence2cont

The resulting list is formatted
[['name1','sequence1sequence1sequence1'],
 ['name2','sequence2sequence2sequence2']]

Usage:
  seqread.py sequence.fta"""


import sys

# Expects a file name as the argument
if len(sys.argv) < 2:
	print Usage
	
else:
	InfileName= sys.argv[1]
	Infile = open(InfileName,'r')
	RecordNum = -1  # don't have the zeroth record yet
	
	# Set up a blank list and blank dictionary
	Sequences=[]
	SeqDict={}
	
	for Line in Infile:
		Line = Line.strip()
		# we have a new record name
		if Line[0]=='>':
			Name=Line[1:]  # chop off the > at the front
			
			# Make a two-item list with the name as the first element, 
			# and an empty string as the second
			
			Sequences.append([Name,''])
			RecordNum += 1 # Now we have a record
			
			# Use the Name for the dictionary key
			SeqKey = Name
			 # create a blank dictionary entry to append later
			SeqDict[SeqKey] = '' 
			
		else:  # this means we are not on a line with a name
			if RecordNum > -1:  # are we past any header lines?
				# Add on to the end of the 2nd element of the list
				Sequences[RecordNum][1] += Line
				# Add to the dictionary value for teh present Key
				SeqDict[SeqKey] += Line
				
	Infile.close()
	# when done with the loop, print the sequences:
	for Seq in Sequences:
		print Seq[0],":", Seq[1]
		
	# could also print a list of all the names (=keys)
	print SeqDict.keys()
