#!/usr/local/bin/python3
'''Functions to read the main Diva 2D input files
'''

import os
import linecache
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import netCDF4
import logging


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
	
def read_mesh(MeshFile, MeshTopoFile):
    '''Read the coordinates of the finite element mesh.
    '''
    # Load mesh caracteristics
    datamesh = np.loadtxt(MeshTopoFile)
    nnodes = int(datamesh[0])
    ninterfaces = int(datamesh[1])
    nelements = int(datamesh[2])
    ntotal = int(datamesh.sum())

    # Load mesh nodes
    meshnodes = np.genfromtxt(MeshFile, skip_footer=nelements + ninterfaces)
    meshnodes = np.fromstring(meshnodes)

    # Load mesh elements
    meshelements = np.genfromtxt(MeshFile, skip_header=nnodes + ninterfaces)
    meshelements = np.fromstring(meshelements)
    meshelements = np.int_(meshelements)

    # Extract node coordinates
    xnode = meshnodes[np.arange(1, nnodes * 3, 3)]
    ynode = meshnodes[np.arange(2, nnodes * 3, 3)]

    # Indices of the elements
    i = np.transpose(range(0, nnodes))
    i1 = meshelements[np.arange(0, nelements * 6, 6)] - 1
    i2 = meshelements[np.arange(2, nelements * 6, 6)] - 1
    i3 = meshelements[np.arange(4, nelements * 6, 6)] - 1
    
    return xnode, ynode, i1, i2, i3
    
def read_results(ResultFile):
    '''Read the analyzed field, the error field (if exists) and their coordinates
    from the netCDF file. 
    If the error field doesn't exist, the function return a field full of NaN's.
    '''
    with netCDF4.Dataset(ResultFile) as nc:
        x = nc.variables['x'][:]
        y = nc.variables['y'][:]
        field = nc.variables['analyzed_field'][:]
        try:
            error = nc.variables['error_field'][:]
        except KeyError:
            logging.warning('No error field in the netCDF file (will return nan)')
            error = np.nan * field
        
    return x, y, field, error
	

		
if __name__ == '__main__':
	
	print('')
	
	
