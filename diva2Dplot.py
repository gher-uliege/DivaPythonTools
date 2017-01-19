import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


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
