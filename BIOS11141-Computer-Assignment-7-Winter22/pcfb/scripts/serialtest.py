#!/usr/bin/env python

# serialtest.py -- a demo of serial comms within python
# requires pyserial to be installed 

import serial

# find out the port name by using: ls /dev/tty.*
MyPort='/dev/tty.usbserial-08HB1916'

# be sure to put the timeout if you are using the readline() function,
#   in case the line is not terminated properly
# the other option is using ser.read(1), which reads one byte (=char)
Ser = serial.Serial(MyPort, 19200, timeout=1)
if Ser:
	i=0
	while (i<20):
		Line = Ser.readline()	# read a '\n' terminated line 
		print Line.strip()
		i+=1
	Ser.close