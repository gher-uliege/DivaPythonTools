#!/usr/bin/env python

# diva_plot_covafit.py
#
# Plot the fit of the covariance function
#
# http://modb.oce.ulg.ac.be/mediawiki/index.php/Diva_python
# ------------------------------------------------------------------------------

import os
import numpy as np
import matplotlib.pyplot as plt

# -------------
# User options
# -------------

# File and directory names
fitdir = './Diva_matlab_example/'
figdir = './figures/'
covarfile = 'covariance.dat'
covarfitfile = 'covariancefit.dat'

# Figure name
figbasename = 'covafit_ex_py'
figtype = '.eps'
figname = figdir + figbasename + figtype

# ------------------------------------------------------------------------------------

# Create figure directory if necessary
if not (os.path.exists(figdir)):
    os.makedirs(figdir)

covar = np.loadtxt(fitdir + covarfile)
covarfit = np.loadtxt(fitdir + covarfitfile)

# Compute axis limits
xmax = 1.1 * max(covarfit[:, 0])
ymin = min(covar[:, 1])
ymax = max(covar[:, 1])
ymin = (ymin - ymax) / 20


# Make the plot
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(covar[:, 0], covar[:, 1], 'b-', label='sampled covariance')

x = np.concatenate((covar[:, 0], covar[::-1, 0]))
y = np.concatenate((covar[:, 1] - covar[:, 3], covar[::-1, 1] + covar[::-1, 3]))

ax.fill(x, y, facecolor='#BBBBFF', edgecolor="none", label="uncertainty")
ax.plot(covarfit[:, 0], covarfit[:, 1], 'bo-', label='covariance used for fitting', ms=3)
ax.plot(covarfit[:, 0], covarfit[:, 2], 'r', label='fitted Bessel covariance')

ax.axhline(y=0, linestyle=':', color='k')

ax.set_xlabel('distance [degrees]', fontsize=18, fontname='Times New Roman')
ax.set_ylabel('covariance', fontsize=18, fontname='Times New Roman')

ax.set_xlim(0, xmax)
ax.set_ylim(ymin, ymax)

ax.legend()

# Export figure and display it
plt.savefig(figname, dpi=300, facecolor='w', edgecolor='w',
            transparent=False, bbox_inches='tight', pad_inches=0.1)

plt.show()
plt.close()
