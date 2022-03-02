#!/usr/bin/env python

Usage = """
matplottest.py - version 1.0

uses smoothing.py, which i got from the net

plot a bunch of curves

run from within the ctd directory

Use the curl commands in ctd matplot.txt to convert the data
Usage:
 matplottest.py *.txt
"""
import sys


yesPDF=False

import matplotlib
if yesPDF:
	matplotlib.use('PDF')   

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
from pylab import subplot

# smoothing function from internet smoothing.py
def smooth(x,window_len=11,window='hanning'):
	s=np.r_[2*x[0]-x[window_len:1:-1],x,2*x[-1]-x[-1:-window_len:-1]]
	w=eval('np.'+window+'(window_len)')
	y=np.convolve(w/w.sum(),s,mode='same')
	return y[window_len-1:-window_len+1]


[xmin, xmax, ymin, ymax] = [0,350,32.0,34.5] # salinity zoom
[xmin, xmax, ymin, ymax] = [0,300,6,20]

# color to use for plot
mycolor="#00000F"


## CHANGE ALPHA (Transparency) HERE
myalpha=.13
panel=-1  ## 3 by 2 and index

if len(sys.argv)<2:
	print Usage	
else:
	FileList= sys.argv[1:]
	#data values to plot:
	# column 1=temp, 2=sal, 3=oxy
	for column in range(1,4):
		panel += 2
		for InfileName in FileList:
		#  had to do try except because blank entries in 
		#  the ctd would choke genfromtxt before you had a chance to parse it
			try:
				v = np.genfromtxt(InfileName, dtype='float')
		#		plt.plot(v[:,0], v[:,1], color=mycolor,alpha=myalpha)
				y=smooth(v[:,column],44)
				subplot(3,2,panel)
				plt.plot(y, -v[:,0], color=mycolor,alpha=1)
	#			plt.axis([xmin, xmax, ymin, ymax])		
				subplot(3,2,panel+1)
				plt.plot(y,-v[:,0], color=mycolor,alpha=myalpha)
	#			plt.axis([xmin, xmax, ymin, ymax])
			except:
				print "SKIPPING", InfileName
			
	if yesPDF:
		plt.savefig('Myplot_6Panel_'+str(myalpha)+".pdf")
	else:
		plt.show()
			

