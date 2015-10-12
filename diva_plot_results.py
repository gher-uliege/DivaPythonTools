#!/usr/bin/env python

# diva_plot_results.py
#
# Plot the gridded field corresponding to the analysis or the error
# (netCDF file)
#
# For error plotting: change line
# field = nc.variables['analyzed_field'][:]
# into
# field = nc.variables['error_field'][:]
#
# http://modb.oce.ulg.ac.be/mediawiki/index.php/Diva_python
# ------------------------------------------------------------------------------

import os
import numpy as np
import math
import netCDF4 as netcdf
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib import colors

# -------------
# User options
# -------------

# Resolution for coastline 
basemap_resolution = 'l'

# File and directory names
resultdir = './Diva_matlab_example/'
figdir = './figures/'
resultfile = 'results.nc'

# Figure extension
figbasename = 'results_ex_py'
figtype = '.eps'
figname = figdir + figbasename + figtype

# Colormap
cmap = plt.cm.spectral_r

# Region of interest        
lonmin = -7.
lonmax = 38.
latmin = 30.
latmax = 45.

# Spacing between x/y labels
dlon = 5.
dlat = 3.

# Number of levels to plot in the contour plot
nlevels = 50

# Unit of the variable to plot
unitname = ' '

# ------------------------------------------------------------------------------------

# Create figure directory if necessary
if not (os.path.exists(figdir)):
    os.makedirs(figdir)

# Load data from file
nc = netcdf.Dataset(resultdir + resultfile)
lon = nc.variables['x'][:]
lat = nc.variables['y'][:]
field = nc.variables['analyzed_field'][:]
nc.close()

# Mask land values
valex = field.min()
field = np.ma.masked_array(field, field == valex)

# Compute min and max values
vmin = field.min()
vmax = field.max()
norm = colors.Normalize(vmin=vmin, vmax=vmax)

levels2plot = np.arange(vmin, vmax, (vmax - vmin) / (nlevels - 1))
newticks = np.arange(vmin, vmax, (vmax - vmin) / 8)
newticks = newticks.round(2)

# Make the plot
fig = plt.figure()
ax = fig.add_subplot(111)

m = Basemap(projection='merc', llcrnrlon=lonmin, llcrnrlat=latmin,
            urcrnrlon=lonmax, urcrnrlat=latmax,
            lat_ts=0.5 * (latmin + latmax),
            resolution=basemap_resolution)

m.ax = ax

llon, llat = np.meshgrid(lon, lat)
x, y = m(llon, llat)

contour = m.contourf(x, y, field, levels2plot, cmap=cmap, norm=norm)

# Add grid, coastline and continent
m.drawcoastlines(ax=ax)
m.fillcontinents(color='black', ax=ax)
meridians = np.arange(lonmin, lonmax, dlon)
parallels = np.arange(latmin, latmax, dlat)
m.drawmeridians(meridians, labels=[0, 0, 1, 0], fontsize=18, fontname='Times New Roman')
m.drawparallels(parallels, labels=[1, 0, 0, 0], fontsize=18, fontname='Times New Roman')

# Add the colorbar
cbar = fig.colorbar(contour, cmap=cmap, orientation='horizontal', fraction=0.1, pad=0.02)
cbar.set_label(unitname, fontsize=18)
cbar.set_ticks(newticks)

# Export figure and display it
plt.savefig(figname, dpi=300, facecolor='w', edgecolor='w',
            transparent=False, bbox_inches='tight', pad_inches=0.1)

plt.show()
plt.close()
