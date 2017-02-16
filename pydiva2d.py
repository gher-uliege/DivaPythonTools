__author__ = 'ctroupin'
"""User interface for diva in python
"""

import logging
import os
import linecache
import numpy as np
import matplotlib.pyplot as plt
import netCDF4
from matplotlib import path
from matplotlib import patches


# create logger
logger = logging.getLogger('diva2D')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('diva2D.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)


class DivaDirectories(object):
    def __init__(self, divamain):
        """
        :param divamain: Main Diva directory (ending by diva-x.y.z)
        :return: str
        """
        self.divamain = divamain

        if os.path.isdir(self.divamain):
            logging.debug("{0} exists".format(self.divamain))
            self.divabin = os.path.join(self.divamain, 'DIVA3D/bin')
            self.divasrc = os.path.join(self.divamain, 'DIVA3D/src/Fortan')
            self.diva2d = os.path.join(self.divamain, 'DIVA3D/divastripped')
            self.diva4d = os.path.join(self.divamain, 'JRA4/Climatology')
            self.diva4dinput = os.path.join(self.divamain, 'JRA4/Climatology/input')
            logger.info('Diva main directory: {0}'.format(self.divamain))
            logger.info('Creating Diva directory paths')
            logger.info("Diva binary directory: {0}".format(self.divabin))
            logger.info("Diva source directory: {0}".format(self.divasrc))
            logger.info("Diva 2D directory: {0}".format(self.diva2d))
            logger.info("Diva 4D directory: {0}".format(self.diva4d))
            logger.info("Diva 4D input directory: {0}".format(self.diva4dinput))

        else:
            logging.error("{0} is not a directory or doesn't exist".format(self.divamain))


class Diva2Dfiles(object):
    """Diva 2D input and output files names based on the current Diva directory
    """
    def __init__(self, diva2d):

        self.diva2d = diva2d

        if os.path.isdir(self.diva2d):
            self.contour = os.path.join(self.diva2d, 'input/coast.cont')
            self.parameter = os.path.join(self.diva2d, 'input/param.par')
            self.data = os.path.join(self.diva2d, 'input/data.dat')
            self.valatxy = os.path.join(self.diva2d, 'input/valatxy.coord')
            self.result = os.path.join(self.diva2d, 'output/ghertonetcdf/results.nc')
            self.mesh = os.path.join(self.diva2d, 'meshgenwork/fort.22')
            self.meshtopo = os.path.join(self.diva2d, 'meshgenwork/fort.23')
            logger.info("Creating Diva 2D file names and paths")
            logger.info("Contour file: {0}".format(self.contour))
            logger.info("Parameter file: {0}".format(self.parameter))
            logger.info("Data file: {0}".format(self.data))
            logger.info("Valatxy file: {0}".format(self.valatxy))
            logger.info("Result file: {0}".format(self.result))
            logger.info("Mesh file: {0}".format(self.mesh))
            logger.info("Mesh topo file: {0}".format(self.meshtopo))
        else:
            logger.error("%{0} is not a directory or doesn't exist".format(self.diva2d))


class Diva2DData(object):
    """Class to store the properties of a 2D data file
    """

    def __init__(self, x=np.array(()), y=np.array(()), field=np.array(()), weight=None):

        if len(x):
            if (len(x) == len(y)) & (len(x) == len(field)):
                self.x = x
                self.y = y
                self.field = field
                logger.info("Creating Diva 2D data object")
            else:
                logger.error("Input vectors have not the same length")
                raise Exception("Input vectors have not the same length")

            if weight is None:
                self.weight = [1] * len(field)
                logger.info("Weight set to 1 for all data points")
            else:
                logger.info("Setting weights to data points")
                self.weight = weight

    def write_to(self, filename):
        """Write the data positions and valies into the selected file .
        :param filename: the name of the 'data' file
        :type filename: str
        :return:
        """
        with open(filename, 'w') as f:
            for xx, yy, zz, ww in zip(self.x, self.y, self.data, self.weight):
                f.write("%s %s %s %s\n" % (xx, yy, zz, ww))
        logger.info("Written data into file {0}".format(filename))

    def read_from_slow(self, filename):
        """Read the information contained in a DIVA data file
        lon, lat, field, (weight).

        This function uses 'numpy.loadtxt', which seems slower than the classic
        reading line by line.
        """
        self.x, self.y, self.field = np.loadtxt(filename, unpack=True, usecols=(0, 1, 2))
        # Not sure the function easily deals with data files with different number of columns.
        # Maybe not necessary to deal with that situation.

    def read_from(self, filename):
        lon, lat, field, weight = [], [], [], []

        if os.path.exists(filename):
            logger.info("Reading data from file {0}".format(filename))
            with open(filename, 'r') as f:
                line = f.readline()
                ncols = len(line.split())
                while ncols >= 3:
                    lon.append(float(line.split()[0]))
                    lat.append(float(line.split()[1]))
                    field.append(float(line.split()[2]))
                    if ncols >= 4:
                        weight.append(float(line.split()[3]))
                    else:
                        weight.append(1.)
                    line = f.readline()
                    ncols = len(line.split())

            self.x = np.array(lon)
            self.y = np.array(lat)
            self.field = np.array(field)
            self.weight = np.array(weight)
        else:
            logger.error("File {0} does not exist".format(filename))
            raise FileNotFoundError('File does not exist')

    def add_to_plot(self, **kwargs):
        """Add the data points to the plot using a scatter plot.
        :param kwargs:
        """
        logger.debug('Adding data points to plot')
        plt.scatter(self.x, self.y, c=self.field, **kwargs)

    def add_positions_to_plot(self, **kwargs):
        """Add the data positions to the plot.
        :param kwargs:
        """
        logger.debug('Adding data positions to plot')
        plt.scatter(self.x, self.y, **kwargs)

    @property
    def count_data(self):
        """Count the number of data points in the data file
        :return: ndata: int
        """
        try:
            ndata = len(self.x)
            logger.info("Number of data points: {0}".format(ndata))
        except AttributeError:
            logger.error("Data object has not been defined")
            ndata = 0
        return ndata


class Diva2DContours(object):
    """Class the stores the properties of a contour
    """

    def __init__(self, x=np.array(()), y=np.array(())):

        if len(x):
            if len(x) == len(y):
                self.x = x
                self.y = y
                logger.info("Creating Diva 2D contour object")
            else:
                Exception("Input vectors have not the same length")
                logger.error("Input vectors have not the same length")

    @property
    def get_contours_number(self):
        """ Return the number of sub-contours
        :return: ncontour: int
        """
        ncontour = len(self.x)
        logger.info("Number of contours: {0}".format(ncontour))
        return ncontour

    @property
    def get_points_number(self):
        """For each contour, return the number of points
        """
        ncontour = self.get_contours_number
        npoints = []
        for i in range(0, ncontour):
            npoints.append(len(self.x[i]))
        return npoints

    def write_to(self, filename):
        """Write the contour coordinates into the selected file.
        :param filename: the name of the 'datasource' file
        :type filename: str
        :return:
        """
        ncontour = self.get_contours_number
        npoints = self.get_points_number

        with open(filename, 'w') as f:
            f.write(str(ncontour) + '\n')
            for i in range(0, ncontour):

                logger.debug("Sub-contour no. {0} has {1} points".format(i+1, npoints[i]))
                f.write(str(npoints[i]) + '\n')
                for xx, yy in zip(self.x[i], self.y[i]):
                    line = ' '.join((str(xx), str(yy)))
                    f.write(line + '\n')

        logger.info("Written contours into file {0}".format(filename))

    def read_from_slow(self, filename):
        """Get the coordinates of the contour from an already existing contour file.

        The function use genfromtxt severall times and is not optimised at all.
        For large contour files, use 'read_from' function.
        :parameter: filename: str
        :return: lon: numpy ndarray
        :return: lat: numpy ndarray
        """

        # Check if the file exist
        if os.path.exists(filename):

            # Count number of contour and lines in the files
            # %timeit shows that "linecache" is way faster than "readline" on the first line
            logger.info("Reading contours from file {0}".format(filename))
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
            logger.error("File {0} does not exist".format(filename))
            raise FileNotFoundError('File does not exist')

    def read_from(self, filename):
        """Get the coordinates of the contour from an already existing contour file.

        The function reads the file only once and performs the conversion from lists
        to ndarrays at the end of the loop.
        :parameter: filename: str
        :return: lon: numpy ndarray
        :return: lat: numpy ndarray
        """

        if os.path.exists(filename):
            logger.info("Reading contours from file {0}".format(filename))
            with open(filename, 'r') as f:
                ncontour = int(f.readline().split()[0])
                logger.debug("Number of contours: {0}".format(ncontour))
                numpoints = []
                lon, lat = [], []
                for nc in range(0, ncontour):
                    npoints = int(f.readline().split()[0])
                    numpoints.append(npoints)
                    xx, yy = [], []
                    for pp in range(0, npoints):
                        # Read the coordinates of the sub-contour
                        coords = f.readline()
                        xx.append(float(coords.split()[0]))
                        yy.append(float(coords.split()[1]))
                    lon.append(xx)
                    lat.append(yy)
            self.x = np.array(lon)
            self.y = np.array(lat)
        else:
            logger.error("File {0} does not exist".format(filename))
            raise FileNotFoundError('File does not exist')

    def add_to_plot(self, **kwargs):
        """Add the contours to the plot
        """
        for lon, lat in zip(self.x, self.y):
            # Append first element of the array to close the contour
            plt.plot(np.append(lon, lon[0]),
                     np.append(lat, lat[0]),
                     **kwargs)


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
        if not(cl is None):
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
            # Compute domain limits for later use
            self.get_domain()

        logger.info("Creating Diva 2D parameter object")

    def describe(self):
        """Print the parameter values read from the parameter file
        """
        logger.info("Correlation length: {0}".format(self.cl))
        logger.info("icoordchange: {0}".format(self.icoordchange))
        logger.info("ispec: {0}".format(self.ispec))
        logger.info("ireg: {0}".format(self.ireg))
        logger.info("Domain: x-axis: from {0} to {1} with {2} steps of {3}".format(self.xori, self.xend,
                                                                                   self.nx, self.dx))
        logger.info("Domain: y-axis: from {0} to {1} with {2} steps of {3}".format(self.yori, self.yend,
                                                                                   self.ny, self.dy))
        logger.info("Exclusion value: {0}".format(self.valex))
        logger.info("Signal-to-noise ratio: {0}".format(self.snr))
        logger.info("Variance of the background field: {0}".format(self.varbak))

    def write_to(self, filename):
        """Create a DIVA 2D parameter file given the main analysis parameters
        defined as floats or integers.
        :param filename: the name of the 'parameter' file
        :type filename: str
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
            logger.info("Written parameters into file {0}".format(filename))

    def read_from(self, filename):
        """Read the information contained in a DIVA parameter file
        and extract the analysis parameters
        :param filename:
        """
        if os.path.exists(filename):
            logger.info("Reading parameters from file {0}".format(filename))
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

            self.get_domain()
        else:
            logger.error("File {0} does not exist".format(filename))
            raise FileNotFoundError('File does not exist')

    def get_domain(self):
        self.xend = self.xori + (self.nx - 1) * self.dx
        self.yend = self.yori + (self.ny - 1) * self.dy

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

        logger.debug('Adding output grid to plot')


class Diva2DValatxy(object):
    """Class to store the positions of the additional locations where the interpolation
    has to be performed.
    """

    def __init__(self, x, y):

        if len(x) == len(y):
            self.x = x
            self.y = y
            logger.info("Creating Diva 2D valatxy object")
        else:
            logger.error("Input vectors have not the same length")
            raise Exception("Input vectors have not the same length")

    def write_to(self, filename):
        """Write the positions where the analysis has to be extracted into the selected file.
        :param filename: the name of the 'valatxy' file
        :type filename: str
        :return:
        """
        with open(filename, 'w') as f:
            for xx, yy in zip(self.x, self.y):
                f.write("%s %s\n" % (xx, yy))
        logger.info("Written locations into file {0}".format(filename))

    def read_from(self, filename):
        """Read the information contained in a DIVA data file
        lon, lat, value, (field)
        """
        self.x, self.y = np.loadtxt(filename, unpack=True, usecols=(0, 1))

    def add_to_plot(self, **kwargs):
        """Add the positions of the extra analysis points to the plot using a scatter plot.
        :param kwargs:
        """
        logger.debug('Adding extra analysis points to plot')
        plt.scatter(self.x, self.y, **kwargs)


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
            logger.debug('Adding analysed field to plot')
            plt.pcolormesh(self.x, self.y, self.field, **kwargs)
            plt.colorbar()
        elif field == 'error':
            logger.debug('Adding error field to plot')
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
    (param.par).
    """

    def __init__(self, filename1, filename2):
        """Initialise the mesh object by reading the coordinates and the topology
        from the specified files.
        """
        logger.info("Creating Diva 2D mesh object")

        datamesh = np.loadtxt(filename2)
        self.nnodes = int(datamesh[0])
        self.ninterfaces = int(datamesh[1])
        self.nelements = int(datamesh[2])

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

    def describe(self):
        """Summarise the mesh characteristics
        """

        logger.info("Number of nodes: {0}".format(self.nnodes))
        logger.info("Number of interfaces: {0}".format(self.ninterfaces))
        logger.info("Number of elements: {0}".format(self.nelements))

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

        logger.debug('Adding finite-element mesh to plot')
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
