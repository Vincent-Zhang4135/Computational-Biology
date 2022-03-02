#!/usr/bin/env python

Usage = """
filestoXYYY.py - version 1.0
Example file for PCfB Chapter 11
Convert a series of X Y tab-delimited files 
to X Y Y Y format and print them to the screen.

Usage:
  filestoXYYY.py *.txt > combinedfile.dat
"""
import sys

if len(sys.argv)<2:
	print Usage	
else:
	FileList= sys.argv[1:]
	# for InfileName in FileList:     # statements done once per file
	# 	print InfileName

	Header = 'lambda'
	LinesToSkip=1

	# change this for comma-delimited files
	Delimiter='\t'
	MasterList=[]

	FileNum=0
	for InfileName in FileList:
		# use the name of the file (w/o extension) as the column Header
		Header += "\t" + InfileName
	
		Infile = open(InfileName, 'r') # it's ok for this to be in the file loop
       # the line number within each file, resets for each file
		LineNumber = 0 # reset for each file
		RecordNum = 0
	
		for Line in Infile: # A in figure
			if LineNumber > (LinesToSkip-1) and len(Line)>3:  # skip first Line and blanks
				Line=Line.strip('\n')
				if FileNum==0:
					MasterList.append(Line)
				else:
					ElementList=Line.split(Delimiter) 
					if len(ElementList)>1:
						MasterList[RecordNum] += "\t" + ElementList[1] 
						RecordNum+=1
					else:
						sys.stderr.write("Line %d not XY format in file %s\n" % (LineNumber,InfileName))
			LineNumber+=1

		FileNum += 1 # the last statement in the file loop
		Infile.close()
	
	# output the results
	# these are indented one level to stay within the first "else:" 
	print Header
	for Item in MasterList:
		print Item

	sys.stderr.write("Converted %d file(s)\n" % FileNum)
