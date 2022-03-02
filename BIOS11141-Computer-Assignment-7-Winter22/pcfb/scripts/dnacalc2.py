#!/usr/bin/env python

# This program takes a DNA sequence (without checking)
# and shows its length and the nucleotide composition


DNASeq="ATGTCTCATTCAAAGCA"


# gather user input for sequence
# this overrides the definition of DNASeq above
#DNASeq=raw_input("Enter a sequence: ")
DNASeq = DNASeq.upper()         # convert to uppercase for .count() function
DNASeq = DNASeq.replace(" ","") # remove spaces

print 'Sequence:', DNASeq 

SeqLength = float(len(DNASeq)) 
print "Sequence Length:", SeqLength

Bases = 'ACGTSW'
Number = {}

for Base in Bases:
	Number[Base] = DNASeq.count(Base)
	# Calculate percentage and output to 1 decimal
	print "%s: %5.1f" % (Base,100*Number[Base]/SeqLength)

TotalStrong = Number['G']+Number['C']+Number['S']  # strong nucleotide total
TotalWeak   = Number['A']+Number['T']+Number['W']  # weak nucleotide total

## END of revised chapter 9 section

#formula for sequences less than 14 nucleotides long
teem = (4*TotalStrong) + (2 * TotalWeak) 

#formula for sequences > 14 nucleotides long
teemlong = (64.9 + 41*(TotalStrong-16.4)/(TotalStrong+TotalWeak))

print

#Only print the appropriate value
if SeqLength<14:
	print "Tm Short: %i C" % (teem) # formula if < 14 (always an integer)
else:
	print "Tm Long (>14): %.1f C" % (teemlong)
