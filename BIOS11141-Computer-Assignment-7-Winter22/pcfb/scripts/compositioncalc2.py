#!/usr/bin/env python	
DNASeq = "ATGTCTCATTCAAAGCA"	
SeqLength = float(len(DNASeq))	

BaseList = list(set(DNASeq))	
for Base in BaseList:	
	Percent = 100 * DNASeq.count(Base) / SeqLength	
	print "%s: %4.1f" % (Base,Percent)