#!/usr/bin/env python

# diva_plot_data.py
# 
# Plot the data points with a color corresponding to the value
# (scatter plot)
#
# http://modb.oce.ulg.ac.be/mediawiki/index.php/Diva_python
#------------------------------------------------------------------------------

import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib  import colors

# Clean 
os.system('clear')

#-------------
# User options
#-------------

# Resolution for coastline 
basemap_resolution = 'l'

# File and directory names
datadir='./Diva_matlab_example/'
figdir='./figures/'
datafile = 'data.dat'

# Figure extension
figbasename = 'data_ex_py'
figtype='.eps'
figname=figdir+figbasename+figtype

# Colormap
cmap=plt.cm.spectral_r

# Region of interest        
lonmin=-7
lonmax=38
latmin=30
latmax=45

# Spacing between x/y labels
dlon = 5
dlat = 3

# Unit of the variable to plot
unitname = ' '

#------------------------------------------------------------------------------------

# Create figure directory if necessary
if not(os.path.exists(figdir)):
    os.makedirs(figdir)
    
# Load data from file
file2load=datadir+datafile
data=np.loadtxt(file2load)
lon=data[:,0]
lat=data[:,1]
field=data[:,2]

# Compute min and max values
vmin=field.min()
vmax=field.max()
norm = colors.Normalize(vmin=vmin,vmax=vmax)


# Make the plot
fig=plt.figure()
ax = fig.add_subplot(111)

m = Basemap(projection='merc',llcrnrlon=lonmin,llcrnrlat=latmin,\
                urcrnrlon=lonmax,urcrnrlat=latmax,  \
                lat_ts=0.5*(lonmin+lonmax),\
                resolution=basemap_resolution)

m.ax=ax
x,y = m(lon, lat)
scat = m.scatter(x, y,c=field,s=15, edgecolor='none',norm=norm,cmap=cmap)

# Add grid, coastline and continent
m.drawcoastlines(ax=ax)
m.fillcontinents(color='black', ax=ax)
meridians=np.arange(lonmin,lonmax,dlon)
parallels=np.arange(latmin,latmax,dlat)
m.drawmeridians(meridians,labels=[0, 0, 1, 0],fontsize=18,fontname='Times New Roman')
m.drawparallels(parallels,labels=[1, 0, 0, 0],fontsize=18,fontname='Times New Roman')

# Add the colorbar
cbar=fig.colorbar(scat,cmap=cmap,orientation='horizontal',fraction=0.1,pad=0.02)
cbar.set_label(unitname,fontsize=18,fontname='Times New Roman')

# Export figure and display it
plt.savefig(figname, dpi=300, facecolor='w', edgecolor='w',
             transparent=False, bbox_inches='tight', pad_inches=0.1)

plt.show()
plt.close()
