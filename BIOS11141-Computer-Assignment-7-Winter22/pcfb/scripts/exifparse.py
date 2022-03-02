#! /usr/bin/env python

"""
Generate a table of pixels per micron for TEM 
images, using exiftool. Run from a folder containing
images or subfolders with images...

requires the program exiftool to be installed and in the path:
http://www.sno.phy.queensu.ca/~phil/exiftool/

exifparse.py
"""

import os
import sys

DirList = os.popen('ls -F| grep \/','r').read().split()
DirList.append('./')
#print DirList

for Direct in DirList:
	sys.stderr.write("Directory "+Direct+'-----------------\n')
	FileList=os.popen('ls ' + Direct +" |grep tif").read().split()

	note="""
Exif data are in the format:
Image Description               : AMT Camera System.11/18/09.14:12.8000.7.0.80.1.Imaging.....-79.811.-552.583..XpixCal=65.569.YpixCal=65.569.Unit=micron.##fv3
"""
	if len(FileList)==0:
		sys.stderr.write("No files found in "+Direct+'\n')
	else:
#		print "yes", FileList
		for PathName in FileList:
			ExifData=os.popen('exiftool '+Direct+ PathName +' | grep YpixCal').read()
			SecondHalf=ExifData.split('XpixCal=')[1].strip()
			NumberOnly=SecondHalf.split('.YpixCal')[0].strip()
			print PathName +"\t"+NumberOnly
		

