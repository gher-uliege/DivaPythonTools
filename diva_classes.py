__author__ = 'ctroupin'
'''User interface for diva in python'''

import logging
import os
import linecache
import numpy as np
import matplotlib.pyplot as plt
import netCDF4
from matplotlib import path
from matplotlib import patches

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class DivaDirectory(object):
    def __init__(self, divadir):

        self.divadir = divadir

        if os.path.isdir(self.divadir):
            logging.debug("{0} exists".format(self.divadir))
            self.divabindir = os.path.join(self.divadir, 'DIVA3D/bin')
            self.divasrcdir = os.path.join(self.divadir, 'DIVA3D/src/Fortan')
            self.diva2ddir = os.path.join(self.divadir, 'DIVA3D/divastripped')
            self.diva4ddir = os.path.join(self.divadir, 'JRA4/Climatology')
            self.diva4dinputdir = os.path.join(self.divadir, 'JRA4/Climatology/input')
            logger.info("Diva binary directory: {0}".format(self.divabindir))
            logger.info("Diva source directory: {0}".format(self.divasrcdir))
            logger.info("Diva 2D directory: {0}".format(self.diva2ddir))
            logger.info("Diva 4D directory: {0}".format(self.diva4ddir))
            logger.info("Diva 4D input directory: {0}".format(self.diva4dinputdir))

        else:
            logging.error("{0} is not a directory or doesn't exist".format(self.divadir))


class Diva2Dfiles(object):
    def __init__(self, diva2ddir):

        self.diva2ddir = diva2ddir

        if os.path.isdir(self.diva2ddir):
            self.contourfile = os.path.join(self.diva2ddir, 'input/coast.cont')
            self.parameterfile = os.path.join(self.diva2ddir, 'input/param.par')
            self.datafile = os.path.join(self.diva2ddir, 'input/data.dat')
            self.valatxyfile = os.path.join(self.diva2ddir, 'input/valatxy.coord')
            self.resultfile = os.path.join(self.diva2ddir, 'output/ghertonetcdf/results.nc')
            self.meshfile = os.path.join(self.diva2ddir, 'meshgenwork/fort.22')
            self.meshtopofile = os.path.join(self.diva2ddir, 'meshgenwork/fort.23')

            logger.info("Contour file: {0}".format(self.contourfile))
            logger.info("Parameter file: {0}".format(self.parameterfile))
            logger.info("Data file: {0}".format(self.datafile))
            logger.info("Valatxy file: {0}".format(self.valatxyfile))
            logger.info("Result file: {0}".format(self.resultfile))
            logger.info("Mesh file: {0}".format(self.meshfile))
            logger.info("Mesh topo file: {0}".format(self.meshtopofile))
        else:
            logging.error("%{0} is not a directory or doesn't exist".format(self.diva2ddir))


class Diva2DData(object):
    """Class to store the properties of a 2D data file
    """

    def __init__(self, x, y, data, weight=None):

        if (len(x) == len(y)) & (len(x) == len(data)):
            self.x = x
            self.y = y
            self.data = data
        else:
            raise Exception("Input vectors have not the same length")

        if not weight:
            self.weight = [1] * len(data)
        else:
            self.weight = weight

    def write_to_file(self, filename):
        with open(filename, 'w') as f:
            for xx, yy, zz, ww in zip(self.x, self.y, self.data, self.weight):
                f.write("%s %s %s %s\n" % (xx, yy, zz, ww))
        logging.info("Written data file {0}".format(filename))

    def read_from_file(self, filename):
        """Read the information contained in a DIVA data file
        lon, lat, value, (field)
        """
        self.x, self.y, self.data = np.loadtxt(filename, unpack=True, usecols=(0, 1, 2))
        # TODO
        # Check performance for huge files
        # Check for files with different number of columns (weight)

    def add_to_plot(self, **kwargs):
        """Add the data points to the plot using a scatter plot.
        :param kwargs:
        """
        plt.scatter(self.x, self.y, c=self.data, **kwargs)

    def add_positions_to_plot(self, **kwargs):
        """Add the data positions to the plot.
        :param kwargs:
        """
        plt.scatter(self.x, self.y, **kwargs)

    @property
    def count_data(self):
        """Count the number of data points in the data file
        :return: ndata: int
        """
        ndata = len(self.x)
        return ndata


class Diva2DContours(object):
    """Class the stores the properties of a contour
    """

    def __init__(self, x=np.array(()), y=np.array(())):

        if len(x):
            if len(x) == len(y):
                self.x = x
                self.y = y
            else:
                Exception("Input vectors have not the same length")

    @property
    def get_contours_number(self):
        """ Return the number of sub-contours
        :return: ncontour: int
        """
        ncontour = len(self.x)
        return ncontour

    def write_to_file(self, filename):
        """Write the contour
        :param filename: string
        :return:
        """
        ncontour = self.get_contours_number
        npoints = self.get_points_number

        logging.debug("Total number of contours: {0}".format(ncontour))
        with open(filename, 'w') as f:
            f.write(str(ncontour) + '\n')
            for i in range(0, ncontour):

                logging.debug("Sub-contour no. {0} has {1} points".format(i, npoints[i]))
                f.write(str(npoints[i]) + '\n')
                for xx, yy in zip(self.x[i], self.y[i]):
                    line = ' '.join((str(xx), str(yy)))
                    f.write(line + '\n')

        logging.info("Written contour file {0}".format(filename))

    def read_from_file(self, filename):
        """Get the coordinates of the contour from an already existing contour file
        :parameter: filename: str
        :return: lon: numpy ndarray
        :return: lat: numpy ndarray
        """

        # Check if the file exist
        if os.path.exists(filename):

            # Count number of contour and lines in the files
            # TODO : find another way to read the 1st line
            # Probably no need to use genfromtxt and linecache

            ncontours = int(linecache.getline(filename, 1))

            with open(filename) as f:
                nlines = sum(1 for _ in f)

            logger.debug("Number of contours: {0}".format(ncontours))

            # Initialise lon and lat as list of lists
            lon = [[]] * ncontours
            lat = [[]] * ncontours

            # Initialise line to read number
            linenum = 2

            # Loop on the contours
            for n in range(0, ncontours):
                # Number of points in the current contour
                npoints = int(linecache.getline(filename, linenum))
                nskiplines = linenum + npoints

                # Load coordinates (npoints lines to be read)
                coords = np.genfromtxt(filename, skip_header=linenum, skip_footer=nlines - nskiplines)
                coords = coords.T
                lon[n] = coords[0]
                lat[n] = coords[1]

                # Update line number
                # (taking into account the number of points already read)
                linenum = nskiplines + 1

            self.x = np.array(lon)
            self.y = np.array(lat)

        else:
            raise FileNotFoundError('File does not exist')

    def add_to_plot(self, **kwargs):
        """Add the contours to the plot
        """
        for lon, lat in zip(self.x, self.y):
            # Append first element of the array to close the contour
            plt.plot(np.append(lon, lon[0]),
                     np.append(lat, lat[0]),
                     **kwargs)

    @property
    def get_points_number(self):
        """For each contour, return the number of points
        """
        ncontour = self.get_contours_number
        npoints = []
        for i in range(0, ncontour):
            npoints.append(len(self.x[i]))
        return npoints


class Diva2DParameters(object):
    """Class that stores the parameter properties
    """

    def __init__(self, cl=None, icoordchange=None, ispec=None, ireg=None,
                 xori=None, yori=None, dx=None, dy=None, nx=None, ny=None,
                 valex=None, snr=None, varbak=None):
        """
        :param cl: Correlation length
        :type cl: float
        """
        self.cl = cl
        self.icoordchange = icoordchange
        self.ispec = ispec
        self.ireg = ireg
        self.xori = xori
        self.yori = yori
        self.dx = dx
        self.dy = dy
        self.nx = nx
        self.ny = ny
        self.valex = valex
        self.snr = snr
        self.varbak = varbak
        self.xend = self.xori + (self.nx - 1) * self.dx
        self.yend = self.yori + (self.ny - 1) * self.dy

    def list_parameters(self):
        """Print the parameter values read from the parameter file
        """
        print("Correlation length: {0}".format(self.cl))
        print("icoordchange: {0}".format(self.icoordchange))
        print("ispec: {0}".format(self.ispec))
        print("ireg: {0}".format(self.ireg))
        print("xori: {0}, yori: {1}, dx: {2}, dy: {3}, nx: {4}, ny: {5}".format(self.xori, self.yori, self.dx,
                                                                                self.dy, self.nx, self.ny))
        print("Exclusion value: {0}".format(self.valex))
        print("Signal-to-noise ratio: {0}".format(self.snr))
        print("Variance of the background field: {0}".format(self.varbak))

    def write_to_file(self, filename):
        """Create a DIVA 2D parameter file given the main analysis parameters
        defined as floats or integers.
        """
        paramstring = ("# Correlation Length lc \n{0} \n"
                       "# icoordchange \n{1} \n"
                       "# ispec \n{2} \n"
                       "# ireg \n{3} \n"
                       "# xori \n{4} \n"
                       "# yori \n{5} \n"
                       "# dx \n{6} \n"
                       "# dy \n{7} \n"
                       "# nx \n{8} \n"
                       "# ny \n{9} \n"
                       "# valex \n{10} \n"
                       "# snr \n{11} \n"
                       "# varbak \n{12}").format(self.cl, self.icoordchange, self.ispec,
                                                 self.ireg, self.xori, self.yori, self.dx, self.dy,
                                                 self.nx, self.ny, self.valex, self.snr, self.varbak,
                                                 )

        with open(filename, 'w') as f:
            f.write(paramstring)

    def read_from_file(self, filename):
        """Read the information contained in a DIVA parameter file
        and extract the analysis parameters
        """
        cl, icoord, ispec, ireg, xori, yori, dx, dy, nx,\
            ny, valex, snr, varbak = np.loadtxt(filename, comments='#', unpack=True)

        self.cl = cl
        self.icoordchange = icoord
        self.ispec = ispec
        self.ireg = ireg
        self.xori = xori
        self.yori = yori
        self.dx = dx
        self.dy = dy
        self.nx = nx
        self.ny = ny
        self.valex = valex
        self.snr = snr
        self.varbak = varbak

    def plot_outputgrid(self, scalefactor=1, **kwargs):
        """Plot the specified output grid for the analyzed field.

        If the grid is too dense, use a scale factor larger than 1.
        The scale factor is rounded if not chosen as integer.
        """

        if not (type(scalefactor) == 'int'):
            scalefactor = round(scalefactor)

        xx = np.arange(self.xori, self.xend, scalefactor * self.dx)
        yy = np.arange(self.yori, self.yend, scalefactor * self.dy)
        plt.hlines(yy, self.xori, self.xend, linewidth=0.2, **kwargs)
        plt.vlines(xx, self.yori, self.yend, linewidth=0.2, **kwargs)


class Diva2DResults(object):
    """Class that stores the results of the analysis
    """

    def __init__(self, filename):
        """Read the analyzed field, the error field (if exists) and their coordinates
        from the netCDF file.
        If the error field doesn't exist, the function return a field full of NaN's.
        """
        self.filename = filename

        try:

            with netCDF4.Dataset(filename) as nc:
                self.x = nc.variables['x'][:]
                self.y = nc.variables['y'][:]
                self.field = nc.variables['analyzed_field'][:]
                try:
                    self.error = nc.variables['error_field'][:]
                except KeyError:
                    logger.warning('No error field in the netCDF file (will return)')
                    self.error = np.nan * self.field
        except OSError:
            logger.error("File {0} does not exist".format(filename))

    def add_to_plot(self, field, **kwargs):
        """Add the result to the plot
        :param field: 'result' or 'error'
        :type field: str
        """
        if field == 'result':
            plt.pcolormesh(self.x, self.y, self.field, **kwargs)
            plt.colorbar()
        elif field == 'error':
            plt.pcolormesh(self.x, self.y, self.error, **kwargs)
            plt.colorbar()
        else:
            logger.error("Field selected for plot does not exist")
            logger.error("Try 'result' or 'error'")


class Diva2DMesh(object):
    """This class stores the finite-element mesh generated by Diva.

    The mesh is stored in 2 files:
    * the first stores the coordinates of the nodes of the triangles,
    * the second contains the mesh topology: numbers of nodes, interfaces and elements.

    The mesh is never explicitely created by the user, but rather generated by a call to the
    script **divamesh**. It is based on the contour file (coast.cont) and the parameter list
    (param.par)
    """

    def __init__(self, filename1, filename2):
        """Initialise the mesh object by reading the coordinates and the topology
        from the specified files.
        """
        datamesh = np.loadtxt(filename2)
        self.nnodes = int(datamesh[0])
        self.ninterfaces = int(datamesh[1])
        self.nelements = int(datamesh[2])

        logger.info("Number of nodes: {0}".format(self.nnodes))
        logger.info("Number of interfaces: {0}".format(self.ninterfaces))
        logger.info("Number of elements: {0}".format(self.nelements))

        # Load mesh nodes
        meshnodes = np.genfromtxt(filename1, skip_footer=self.nelements + self.ninterfaces)
        meshnodes = np.fromstring(meshnodes)

        # Load mesh elements
        meshelements = np.genfromtxt(filename1, skip_header=self.nnodes + self.ninterfaces)
        meshelements = np.fromstring(meshelements)
        meshelements = np.int_(meshelements)

        # Extract node coordinates
        self.xnode = meshnodes[np.arange(1, self.nnodes * 3, 3)]
        self.ynode = meshnodes[np.arange(2, self.nnodes * 3, 3)]

        # Indices of the elements
        self.i1 = meshelements[np.arange(0, self.nelements * 6, 6)] - 1
        self.i2 = meshelements[np.arange(2, self.nelements * 6, 6)] - 1
        self.i3 = meshelements[np.arange(4, self.nelements * 6, 6)] - 1

    def add_to_plot(self, ax, **kwargs):
        """Plot the finite element mesh using the patch function of matplotlib.

        An ax object should exist in order to add the patches to the plot.
        It is also possible to make the plot using simple line. That method is slower.
        """
        for j in range(0, self.nelements):
            verts = [(self.xnode[self.i1[j]], self.ynode[self.i1[j]]),
                     (self.xnode[self.i2[j]], self.ynode[self.i2[j]]),
                     (self.xnode[self.i3[j]], self.ynode[self.i3[j]]),
                     (self.xnode[self.i1[j]], self.ynode[self.i1[j]])]
            meshpath = path.Path(verts)
            meshpatch = patches.PathPatch(meshpath, facecolor='none', **kwargs)
            ax.add_patch(meshpatch)

        ax.set_xlim(self.xnode.min(), self.xnode.max())
        ax.set_ylim(self.ynode.min(), self.ynode.max())

        '''
        xx = (self.xnode[self.i1[j]], self.xnode[self.i2[j]], self.xnode[self.i3[j]], self.xnode[self.i1[j]])
        yy = (self.ynode[self.i1[j]], self.ynode[self.i2[j]], self.ynode[self.i3[j]], self.ynode[self.i1[j]])
        plt.plot(xx, yy, **kwargs)
        '''


def main():
    parameters2d = Diva2DParameters(1.5, 0, 0, 1, -10., -10., 0.2, 0.2, 101, 101, -999, 3.0, 1.0)
    parameters2d.list_parameters()


if __name__ == "__main__":
    main()
