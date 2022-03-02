#!/usr/bin/env python
# encoding: utf-8

# print a table of hex, binary, unicode values for 0 to 256
# the first 127 characters are also the ascii character set
# uses this built-in module to convert to bin and hex


def int2bin(n, count=8):
    """returns the binary of integer n, using count number of digits"""
    return "".join([str((n >> y) & 1) for y in range(count-1, -1, -1)])

ValuesToPrint = 256
for x in range(ValuesToPrint):
	# split parameters of the % operator across lines
	print "%03d\t%8s\t%s\t%s" % (
	x,              # the decimal value
	int2bin(x),     # binary representation 
	hex(x).upper(), # hexadecimal value
	unichr(x)       # unicode character
	)

