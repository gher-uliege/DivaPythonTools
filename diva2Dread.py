#!/usr/local/bin/python3
'''Functions to read the main Diva 2D input files
'''

import os
import linecache
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import netCDF4


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
            logging.warning('No error field in the netCDF file')
            error = np.nan * field
        
    return x, y, field, error
	
def plot_contour(contours, **kwargs):
	for contour in contours:
		# Append first element of the array to close the contour
		plt.plot(np.append(contour[:, 0], contour[0, 0]), 
		         np.append(contour[:, 1], contour[0, 1]))
		         
def plot_datapoints(lon, lat, cmap=plt.cm.RdYlBu_r, *args, **kwargs):
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
    
def plot_mesh(xnode, ynode, i1, i2, i3, ax, **kwargs):
    '''Plot the finite element mesh using the patch function of matplotlib.
    '''
    nelements = len(i1)
    for j in range(0, nelements):
        verts = [(xnode[i1[j]], ynode[i1[j]]),
                 (xnode[i2[j]], ynode[i2[j]]),
                 (xnode[i3[j]], ynode[i3[j]]),
                 (xnode[i1[j]], ynode[i1[j]])]
        path = mpl.path.Path(verts)
        patch = mpl.patches.PathPatch(path, facecolor='none', lw=.2)
        ax.add_patch(patch)
        
def plot_field(x, y, field, cmap=plt.cm.RdYlBu_r, **kwargs):
    pcm = plt.pcolor(x, y, field, cmap=cmap)
    plt.colorbar(pcm)
    
def plot_error(x, y, field, cmap=plt.cm.hot_r, **kwargs):
    pcm = plt.pcolor(x, y, field, cmap=cmap)
    plt.colorbar(pcm)
		
if __name__ == '__main__':
	
	contourfile = '/home/ctroupin/Software/DIVA/diva-4.7.1/DIVA3D/divastripped/input/coast.cont'
	datafile = '/home/ctroupin/Software/DIVA/diva-4.7.1/DIVA3D/divastripped/input/data.dat'
	ParamFile = '/home/ctroupin/Software/DIVA/diva-4.7.1/DIVA3D/divastripped/input/param.par'
	meshfile = '/home/ctroupin/Software/DIVA/diva-4.7.1/DIVA3D/divastripped/output/meshvisu/fort.22'
	meshtopofile = '/home/ctroupin/Software/DIVA/diva-4.7.1/DIVA3D/divastripped/output/meshvisu/fort.23'
	resultfile = '/home/ctroupin/Software/DIVA/diva-4.7.1/DIVA3D/divastripped/output/ghertonetcdf/results.nc'
	
	figdir = '/home/ctroupin/ULg/DIVA/Diva_python_tools/testfigures'
	contours = read_contour(contourfile)
	lon, lat, field = read_data(datafile)
	lc, icoord, ispec, ireg, xori, yori, dx, dy, nx, ny,\
	valex, snr, varbak = read_parameters(ParamFile)
	xnode, ynode, i1, i2, i3 = read_mesh(meshfile, meshtopofile)
	x, y, field, error = read_results(resultfile)
	
	fig = plt.figure()
	ax = fig.add_subplot(111)
	plot_contour(contours, zorder=4)
	plot_datapoints(lon, lat, marker='o', color='k', zorder=2)
	#plot_mesh(xnode, ynode, i1, i2, i3, ax, zorder=3)
	plot_field(x, y, field, zorder=1)
	plt.savefig(os.path.join(figdir, 'contour_data_results.png'), dpi=300)
	plt.close()
