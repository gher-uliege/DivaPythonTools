#!/usr/bin/env python

# diva_plot_mesh.py
#
# Plot the finite-element mesh
#
# http://modb.oce.ulg.ac.be/mediawiki/index.php/Diva_python
# ------------------------------------------------------------------------------

import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib import colors
from matplotlib.path import Path
import matplotlib.patches as patches

# Clean 
os.system('clear')

# -------------
# User options
# -------------

# Resolution for coastline 
basemap_resolution = 'i'

# File and directory names
meshdir = './Diva_matlab_example/'
figdir = './figures/'
meshfile = 'mesh.dat'
meshtopofile = 'meshtopo.dat'

# Figure name
figbasename = 'mesh_ex_py'
figtype = '.eps'
figname = figdir + figbasename + figtype

# Region of interest        
lonmin = -7.
lonmax = 38.
latmin = 30.
latmax = 45.

# Spacing between x/y labels
dlon = 5.
dlat = 3.

# Unit of the variable to plot
unitname = ' '

# ------------------------------------------------------------------------------------

# Create figure directory if necessary
if not (os.path.exists(figdir)):
    os.makedirs(figdir)

# Load mesh information
datamesh = np.loadtxt(meshdir + meshtopofile)
nnodes = int(datamesh[0])
ninterfaces = int(datamesh[1])
nelements = int(datamesh[2])
ntotal = int(datamesh.sum())

# Load mesh nodes
meshnodes = np.genfromtxt(meshdir + meshfile, skip_footer=nelements + ninterfaces)
meshnodes = np.fromstring(meshnodes)

# Load mesh elements
meshelements = np.genfromtxt(meshdir + meshfile, skip_header=nnodes + ninterfaces)
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

# Make the plot
fig = plt.figure()
ax = fig.add_subplot(111)

m = Basemap(projection='merc', llcrnrlon=lonmin, llcrnrlat=latmin,
            urcrnrlon=lonmax, urcrnrlat=latmax,
            lat_ts=0.5 * (lonmin + lonmax),
            resolution=basemap_resolution)
m.ax = ax

# Project nodes
xnode, ynode = m(xnode, ynode)
xnode[xnode == 1e+30] = np.nan
ynode[ynode == 1e+30] = np.nan

# Loop on the elements and patch
# (can probably be optimized if the loop is removed)

for j in range(0, nelements):
    verts = [(xnode[i1[j]], ynode[i1[j]]),
             (xnode[i2[j]], ynode[i2[j]]),
             (xnode[i3[j]], ynode[i3[j]]),
             (xnode[i1[j]], ynode[i1[j]])]
    path = Path(verts)
    patch = patches.PathPatch(path, facecolor='none', lw=1)
    m.ax.add_patch(patch)

# Set axis limits 
m.ax.set_xlim(lonmin, lonmax)
m.ax.set_ylim(latmin, latmax)

# Add grid, coastline and continent
m.drawcoastlines(ax=ax)
m.fillcontinents(color='black', ax=ax)
meridians = np.arange(lonmin, lonmax, dlon)
parallels = np.arange(latmin, latmax, dlat)
m.drawmeridians(meridians, labels=[0, 0, 1, 0], fontsize=18, fontname='Times New Roman')
m.drawparallels(parallels, labels=[1, 0, 0, 0], fontsize=18, fontname='Times New Roman')

# Export figure and display it
plt.savefig(figname, dpi=300, facecolor='w', edgecolor='w',
            transparent=False, bbox_inches='tight', pad_inches=0.1)

plt.show()
plt.close()
