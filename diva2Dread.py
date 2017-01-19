#!/usr/local/bin/python3
'''Functions to read the main Diva 2D input files
'''

import os
import linecache
import numpy as np
import matplotlib.pyplot as plt

def read_contour(ContourFile):
	'''Read the information contained in a DIVA contour file
	'''
	contours = []
	
	# Count number of files and contours
	ncontours = int(linecache.getline(ContourFile, 1))
	nlines = sum(1 for line in open(ContourFile))
	
	# Initialise line to read number
	linenum = 2

	# Loop on the contours
	for n in (np.arange(0, ncontours)):
		
		# Number of points in the current contour
		npoints = int(linecache.getline(ContourFile, linenum))
		nskiplines = linenum + npoints
		
		# Load coordinates (npoints lines to be read)
		coords = np.genfromtxt(ContourFile, skip_header=linenum, skip_footer=nlines - nskiplines)
		contours.append(coords)

		# Update line number
		# (taking into account the number of points already read)
		linenum = nskiplines + 1
	
	return contours
	
def plot_contour(contours):
	for contour in contours:
		# Append first element of the array to close the contour
		plt.plot(contour[:, 0], contour[:, 1])
	
if __name__ == '__main__':
	contourfile = '/home/ctroupin/Software/DIVA/diva-4.7.1/DIVA3D/divastripped/input/coast.cont'
	contours = read_contour(contourfile)
	
	fig = plt.figure()
	plot_contour(contours)
	plt.savefig('./test_contour.png')
	plt.close()
