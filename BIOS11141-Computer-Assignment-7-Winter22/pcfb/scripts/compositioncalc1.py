#! /usr/bin/env python
DNASeq = "ATGTCTCATTCAAAGCA"
SeqLength = float(len(DNASeq))

BaseList = "ACGT"
for Base in BaseList:
	Percent = 100 * DNASeq.count(Base) / SeqLength
	print "%s: %4.1f" % (Base,Percent)
