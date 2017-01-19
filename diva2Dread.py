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
	
def read_data(DataFile):
	'''Read the information contained in a DIVA data file
	lon, lat, value, (field)
	'''
	lon, lat, field = np.loadtxt(DataFile, unpack=True, usecols=(0, 1, 2))
	#TODO
	# Check performance for huge files
	# Check for files with different number of columns (weight)

	return lon, lat, field
	
def read_parameters(ParamFile):
	'''Read the information contained in a DIVA parameter file
	and extract the analysis parameters
	'''
	lc, icoord, ispec, ireg, xori, yori, dx, dy, nx,\
	ny, valex, snr, varbak = np.loadtxt(ParamFile, 
	                                    comments='#', unpack=True)

	return lc, icoord, ispec, ireg, xori, yori,\
	dx, dy, nx, ny, valex, snr, varbak
	
def plot_contour(contours):
	for contour in contours:
		# Append first element of the array to close the contour
		plt.plot(np.append(contour[:, 0], contour[0, 0]), 
		         np.append(contour[:, 1], contour[0, 1]))
		         
def plot_datapoints(lon, lat, *args, **kwargs):
	if len(args) == 1:
		plt.scatter(lon, lat, c=args[0], **kwargs)
		cbar = plt.colorbar()
	else:
		plt.scatter(lon, lat, **kwargs)
		
def plot_outputgrid(xori, yori, dx, dy, nx, ny, scalefactor=1, **kwargs):
    '''Plot the specified output grid for the analyzed field.
    If the grid is too dense, use a scale factor larger than 1.
    The scale factor is rounded if not chosen as integer.
    '''
    if not(type(scalefactor) == 'int'):
        scalefactor = round(scalefactor)

    # derive xmax and ymax
    xend, yend = xori + (nx + 1) * dx, yori + (ny + 1) * dy
    xx, yy = np.arange(xori, xend, scalefactor * dx), np.arange(yori, yend, scalefactor * dy)
    plt.hlines(yy, xori, xend, **kwargs, linewidth=0.2)
    plt.vlines(xx, yori, yend, **kwargs, linewidth=0.2)
		
	
if __name__ == '__main__':
	contourfile = '/home/ctroupin/Software/DIVA/diva-4.7.1/DIVA3D/divastripped/input/coast.cont'
	datafile = '/home/ctroupin/Software/DIVA/diva-4.7.1/DIVA3D/divastripped/input/data.dat'
	ParamFile = '/home/ctroupin/Software/DIVA/diva-4.7.1/DIVA3D/divastripped/input/param.par'
	
	contours = read_contour(contourfile)
	lon, lat, field = read_data(datafile)
	lc, icoord, ispec, ireg, xori, yori, dx, dy, nx, ny,\
	valex, snr, varbak = read_parameters(ParamFile)
	
	fig = plt.figure()
	plot_contour(contours)
	plot_datapoints(lon, lat, marker='o', color='k')
	plt.savefig('./test_contour_data.png')
	plt.close()
