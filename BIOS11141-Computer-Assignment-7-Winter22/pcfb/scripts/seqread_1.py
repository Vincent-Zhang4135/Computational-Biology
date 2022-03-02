#!/usr/bin/env python

InfileName = 'example.fta'
Infile = open(InfileName,'r')

RecordNum = -1
Sequences=[]

for Line in Infile:
	Line = Line.strip()

	# first char of > indicates new sequence
	if Line[0] == '>':
		Name=Line[1:]  # cut off first letter

		# create new list element with [Name,Seq]
		# At this point, Seq is blank
		Sequences.append([Name,''])
		RecordNum += 1
		
		
	else:
		if RecordNum > -1:
			Sequences[RecordNum][1] += Line

Infile.close()
# to create a list of just names
SeqNames = [item[0] for item in Sequences]
SeqSeqs  = [item[1] for item in Sequences]

for Seq in Sequences:
	print Seq[0]+ "\t" +Seq[1]

