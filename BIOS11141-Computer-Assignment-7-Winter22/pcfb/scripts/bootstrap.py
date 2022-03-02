#!/usr/bin/env python
# coding: utf-8
"""demo of bootstrapping via resample with replacement"""

MyReps = 50  # Number of resamplings to conduct	

# for the demo, create an arbitrary list of numbers 0 to 19	
# normally these would be the original data
MyDataList = range(20)	

# loop repeatedly to create resampled lists:	
def bootstrap(DataList,Samples=10):
	import random
	Bootstraps=[] # List to store the random lists

	for X in range(Samples):	
	   Resample = [random.choice(DataList) for Y in DataList]	
	   Bootstraps.append(Resample)	
	return Bootstraps

Bootstraps = bootstrap(MyDataList,MyReps)

for Z in Bootstraps:	
   print Z	