import logging
import os
import linecache
import numpy as np
import datetime
import matplotlib.pyplot as plt
import netCDF4
import subprocess
import shutil
from matplotlib import path
from matplotlib import patches

__author__ = 'ctroupin (GHER, ULg)'
"""Module for running Diva2D, including:
- Input file preparation
- Figure generation
- Map generation
"""


def divalogger(logname, logfile):
    """Create logger object to handle messages
    :param logname: name of the logger
    :param logfile: path to the file storing the messages
    :type logfile: str
    """
    logger = logging.getLogger(logname)
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler(logfile)
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


logdir = "./logs/"
if not os.path.exists(logdir):
    os.makedirs(logdir)
logfile = ''.join((logdir, 'Diva_', datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S'), '.log'))
logger = divalogger(__name__, logfile)
logger.info("Logs written in file: {0}".format(logfile))


class DivaDirectories(object):
    """Object storing the paths to the main Diva 2D directories: binaries, sources,
    execution directory, ...
    """

    def __init__(self, divamain):
        """Creation of the 'Diva Directories' object using the user inputs.
        :param divamain: Main Diva directory (path ending by diva-x.y.z)
        :type divamain: str
        :return:
        """

        if os.path.isdir(divamain):
            self.divamain = divamain
            logger.debug("{0} exists".format(self.divamain))
            self.divabin = os.path.join(self.divamain, 'DIVA3D/bin')
            self.divasrc = os.path.join(self.divamain, 'DIVA3D/src/Fortran')
            self.diva2d = os.path.join(self.divamain, 'DIVA3D/divastripped')
            self.diva4d = os.path.join(self.divamain, 'JRA4/Climatology')
            self.divaexample = os.path.join(self.divamain, 'Example4D/')

            logger.info('Diva main directory: {0}'.format(self.divamain))
            logger.info('Creating Diva directory paths')
            logger.info("Binary directory:   {0}".format(self.divabin))
            logger.info("Source directory:   {0}".format(self.divasrc))
            logger.info("Main 2D directory:  {0}".format(self.diva2d))
            logger.info("Main 4D directory:  {0}".format(self.diva4d))
            logger.info("Example directory:  {0}".format(self.divaexample))
        else:
            logger.error("{0} is not a directory or doesn't exist".format(divamain))


class Diva2Dfiles(object):
    """Diva 2D input and output files names based on the current Diva directory
    """

    def __init__(self, diva2d):
        """Creation of the Diva 2D 'file' object based on the main Diva 2D directory
        :param diva2d: Main directory for Diva 2D (path ending by divastripped)
        :type diva2d: str
        :return:
        """
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
            logger.info("Contour file:   {0}".format(self.contour))
            logger.info("Parameter file: {0}".format(self.parameter))
            logger.info("Data file:      {0}".format(self.data))
            logger.info("Valatxy file:   {0}".format(self.valatxy))
            logger.info("Result file:    {0}".format(self.result))
            logger.info("Mesh file:      {0}".format(self.mesh))
            logger.info("Mesh topo file: {0}".format(self.meshtopo))
        else:
            logger.error("%{0} is not a directory or doesn't exist".format(self.diva2d))


class Diva2DData(object):
    """Class to store the properties of a 2D data file
    """

    def __init__(self, x=None, y=None, field=None, weight=None):
        """Creation of the Diva 2D 'data' object using the user inputs.
        :param x: Data point x-coordinates
        :type x: numpy array
        :param y: Data point y-coordinates
        :type y: numpy array
        :param field: Data point values
        :type field: numpy array
        :param weight: Data point weights
        :type weight: numpy array
        :return:
        """

        logger.info("Creating Diva 2D data object")
        if x is None:
            logger.info("X vector not defined")
            self.x = x
        elif isinstance(x, np.ndarray):
            pass
        elif isinstance(x, list):
            x = np.array(x)
        else:
            logger.error("Not a valid type for x coordinates")
            raise Exception("Not a valid type for x coordinates")

        if y is None:
            logger.info("Y vector not defined")
            self.y = y
        elif isinstance(y, np.ndarray):
            pass
        elif isinstance(y, list):
            y = np.array(y)
        else:
            logger.error("Not a valid type for x coordinates")
            raise Exception("Not a valid type for x coordinates")

        if field is None:
            logger.info("Data values not defined")
            self.field = field
            self.x = None
            self.y = None
        elif isinstance(field, np.ndarray):
            pass
        elif isinstance(field, list):
            field = np.array(field)
        else:
            logger.error("Not a valid type for data values")
            raise Exception("Not a valid type for x coordinates")

        if (field is None) & (weight is None):
            logger.info("Data weights not defined")
            self.weight = weight
            self.field = None
            self.x = None
            self.y = None
        elif (weight is None) & (field is not None):
            weight = np.array([1] * len(field))
            logger.info("Weight set to 1 for all data points")
        elif isinstance(weight, np.ndarray):
            pass
        elif isinstance(weight, list):
            weight = np.array(weight)
        else:
            logger.error("Not a valid type for weight")
            raise Exception("Not a valid type for weight")

        try:
            if (len(x) == len(y)) & (len(x) == len(field)) & (len(field) == len(weight)):
                self.x = x
                self.y = y
                self.field = field
                self.weight = weight
            else:
                logger.error("Input vectors have not the same length")
                raise Exception("Input vectors have not the same length")
        except TypeError:
            # If the values are all None
            logger.info("Coordinates, data and weights set to None")

    def write_to(self, filename):
        """Write the data positions and valies into the selected file .
        :param filename: name of the 'data' file
        :type filename: str
        :return:
        """
        with open(filename, 'w') as f:
            for xx, yy, zz, ww in zip(self.x, self.y, self.field, self.weight):
                f.write("%s %s %s %s\n" % (xx, yy, zz, ww))
        logger.info("Written data into file {0}".format(filename))

    def read_from_slow(self, filename):
        """Read the information contained in a DIVA data file
        lon, lat, field, (weight).

        This function uses 'numpy.loadtxt', which seems slower than the classic
        reading line by line.
        :param filename: Name of the 'data' file
        :type filename: str
        """
        self.x, self.y, self.field = np.loadtxt(filename, unpack=True, usecols=(0, 1, 2))
        # Not sure the function easily deals with data files with different number of columns.
        # Maybe not necessary to deal with that situation.

    def read_from(self, filename):
        """Read the information contained in a DIVA data file
        lon, lat, field, (weight).

        This function uses python lists and convert them to 'ndarrays' once the
        file is read.
        :param filename: name of the 'data' file
        :type filename: str
        """

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

    def add_to_plot(self, m=None, **kwargs):
        """Add the data points to the plot using a scatter plot.
        :param m: basemap projection
        :type m: mpl_toolkits.basemap.Basemap
        :param kwargs: options for the plot
        :return dataplot
        """
        if m is None:
            logger.debug("No projection defined")
            logger.debug("Adding data points to plot")
            dataplot = plt.scatter(self.x, self.y, c=self.field, **kwargs)
        else:
            logger.debug("Applying projection to coordinates")
            logger.debug("Adding data points to map")

            dataplot = m.scatter(self.x, self.y, c=self.field, latlon=True, **kwargs)

        return dataplot

    def add_positions_to_plot(self, **kwargs):
        """Add the data positions to the plot.
        :param kwargs: options for the plot
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
    """Class that stores the properties of a contour
    """

    def __init__(self, x=None, y=None):
        """Creation of the Diva 2D 'data' object using the user inputs.
        :param x: x-coordinates of the contours
        :type x: numpy ndarray
        :param y: y-coordinates of the contours
        :type y: numpy ndarray
        """
        logger.info("Creating Diva 2D contour object")
        if (x is None) | (y is None):
            logger.info("Contour coordinates not defined")
            self.x = x
            self.y = y
        else:
            if isinstance(x, list):
                x = np.array(x)
            elif isinstance(x, np.ndarray):
                pass
            else:
                logger.error("Not a valid type for x coordinates")
                raise Exception("Not a valid type for x coordinates")

            if isinstance(y, list):
                y = np.array(y)
            elif isinstance(y, np.ndarray):
                pass
            else:
                logger.error("Not a valid type for y coordinates")
                raise Exception("Not a valid type for y coordinates")

            if len(x) == len(y):
                self.x = x
                self.y = y
            else:
                logger.error("Input vectors have not the same length")
                Exception("Input vectors have not the same length")

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
        """Write the contour coordinates into the selected file
        :param filename: name of the 'datasource' file
        :type filename: str
        :return:
        """
        ncontour = self.get_contours_number
        npoints = self.get_points_number

        with open(filename, 'w') as f:
            f.write(str(ncontour) + '\n')
            for i in range(0, ncontour):

                logger.debug("Sub-contour no. {0} has {1} points".format(i + 1, npoints[i]))
                f.write(str(npoints[i]) + '\n')
                for xx, yy in zip(self.x[i], self.y[i]):
                    line = ' '.join((str(xx), str(yy)))
                    f.write(line + '\n')

        logger.info("Written contours into file {0}".format(filename))

    def read_from_np(self, filename):
        """Get the coordinates of the contour from an already existing contour file.

        The function use numpy method 'genfromtxt' several times and is not optimised at all.
        For large contour files, prefer 'read_from' function.
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
        :parameter filename: name of the 'contour' file
        :type filename: str
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

    def add_to_plot(self, m=None, **kwargs):
        """Add the contours to the plot
        :param m: basemap projection
        :type m: mpl_toolkits.basemap.Basemap
        """

        if m is None:
            logger.debug("No projection defined")
            logger.debug('Adding contours to plot')
            for lon, lat in zip(self.x, self.y):
                # Append first element of the array to close the contour
                plt.plot(np.append(lon, lon[0]),
                         np.append(lat, lat[0]),
                         **kwargs)
        else:
            logger.debug("Applying projection to coordinates")
            logger.debug('Adding contours to map')
            for lon, lat in zip(self.x, self.y):
                m.plot(np.append(lon, lon[0]),
                       np.append(lat, lat[0]),
                       latlon=True, **kwargs)


class Diva2DParameters(object):
    """Class that stores the parameter properties

    Example:
    ========

    Parameters = Diva2DParameters(CorrelationLength, iCoordChange, iSpec, iReg, xmin, ymin, dx, dy,
                                  nx, ny, ExclusionValue, SignalToNoiseRatio, VarianceBackgroundField)
    """

    def __init__(self, cl=None, icoordchange=0, ispec=0, ireg=0,
                 xori=None, yori=None, dx=None, dy=None, nx=None, ny=None,
                 valex=-999., snr=None, varbak=None):
        """Creation of the Diva 2D 'data' object using the user inputs.
        :param cl: correlation length
        :type cl: float
        :param icoordchange: flag for the specification of the coordinate change
        :type icoordchange: int
        :param ispec: flag for the specification of the output field
        :type ispec: int
        :param ireg: flag for the specification of the reference field
        :type ireg: int
        :param xori: westermost location of the computation domain
        :type xori: float
        :param yori: southernmost location of the computation domain
        :type yori: float
        :param dx: spatial step in the x-direction
        :type dx: float
        :param dy: spatial step in the x-direction
        :type dy: float
        :param nx: number of steps in the x-direction
        :type nx: int
        :param ny: number of steps in the y-direction
        :type ny: int
        :param valex: exclusion (also called fill) value in the analysis and error fields
        :type valex: float
        :param snr: signal-to-noise ratio of the dataset
        :type snr: float
        :param varbak: variance of the background field
        :type varbak: float
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

        # Compute domain limits for later use
        if self.nx and self.dx and self.xori:
            self.xend = self.xori + (self.nx - 1) * self.dx
        else:
            self.xend = None
        if self.ny and self.dy and self.yori:
            self.yend = self.yori + (self.ny - 1) * self.dy
        else:
            self.yend = None

        logger.info("Creating Diva 2D parameter object")

    '''
    class Icoord(object):

        def __init__(self, icoordchange=0):
            self.icoordchange = icoordchange
            print(icoordchange)

        def describe(self):
            if self.icoordchange == None:
                logger.warning("icoordchange not defined")
                self.description = ' '
            else:
                if self.icoordchange == 0:
                    self.description = 'no change is necessary ; same coordinates as data'
                elif self.icoordchange == 1:
                    self.description = 'convertion from degrees to kilometers'
                elif self.icoordchange == 2:
                    self.description = 'conversion from degrees to kilometers using a cosine projection'
                elif self.icoordchange < 0:
                    self.description = 'apply scale factor xscale before doing starting the calculation'
                else:
                    self.description = 'unknown value'
    '''

    def describe(self):
        """Provide a description of the parameter values stored in the parameter file

        If the parameters were not initialised, returns None for each value.
        """

        print("Correlation length: {0}".format(self.cl))
        print("icoordchange: {0}".format(self.icoordchange))
        print("ispec: {0}".format(self.ispec))
        print("ireg: {0}".format(self.ireg))
        print("Domain: x-axis: from {0} to {1} with {2} steps of {3}".format(self.xori, self.xend,
                                                                             self.nx, self.dx))
        print("Domain: y-axis: from {0} to {1} with {2} steps of {3}".format(self.yori, self.yend,
                                                                             self.ny, self.dy))
        print("Exclusion value: {0}".format(self.valex))
        print("Signal-to-noise ratio: {0}".format(self.snr))
        print("Variance of the background field: {0}".format(self.varbak))

    def write_to(self, filename):
        """Create a DIVA 2D parameter file given the main analysis parameters
        defined as floats or integers.
        :param filename: name of the 'parameter' file
        :type filename: str
        :return
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
        :param filename: name of the 'parameter' file
        :type filename: str
        """
        if os.path.exists(filename):
            logger.info("Reading parameters from file {0}".format(filename))
            cl, icoord, ispec, ireg, xori, yori, dx, dy, nx,\
                ny, valex, snr, varbak = np.loadtxt(filename, comments='#', unpack=True)

            self.cl = cl
            self.icoordchange = int(icoord)
            self.ispec = int(ispec)
            self.ireg = int(ireg)
            self.xori = xori
            self.yori = yori
            self.dx = dx
            self.dy = dy
            self.nx = int(nx)
            self.ny = int(ny)
            self.valex = valex
            self.snr = snr
            self.varbak = varbak

            # Compute domain limits for later use
            self.xend = self.xori + (self.nx - 1) * self.dx
            self.yend = self.yori + (self.ny - 1) * self.dy
        else:
            logger.error("File {0} does not exist".format(filename))
            raise FileNotFoundError('File does not exist')

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
        """Creation of the Diva 2D 'data' object using the user inputs.
        :param x: x-coordinates of the additional points
        :type x: numpy array
        :param y: x-coordinates of the additional points
        :type y: numpy array
        """
        if len(x) == len(y):
            self.x = x
            self.y = y
            logger.info("Creating Diva 2D valatxy object")
        else:
            logger.error("Input vectors have not the same length")
            raise Exception("Input vectors have not the same length")

    def write_to(self, filename):
        """Write the positions where the analysis has to be extracted into the selected file.
        :param filename: name of the 'valatxy' file
        :type filename: str
        :return:
        """
        with open(filename, 'w') as f:
            for xx, yy in zip(self.x, self.y):
                f.write("%s %s\n" % (xx, yy))
        logger.info("Written locations into file {0}".format(filename))

    def read_from(self, filename):
        """Read the information contained in a valatxy file
        :param filename: name of the 'valatxy' file
        :type filename: str
        """
        self.x, self.y = np.loadtxt(filename, unpack=True, usecols=(0, 1))

    def add_to_plot(self, m=None, **kwargs):
        """Add the positions of the extra analysis points to the plot using a scatter plot.
        :param m: basemap projection
        :type m: mpl_toolkits.basemap.Basemap
        """

        if m is None:
            logger.debug("No projection defined")
            logger.debug('Adding extra analysis points to plot')
            dataplot = plt.scatter(self.x, self.y, **kwargs)
        else:
            logger.debug("Applying projection to coordinates")
            logger.debug('Adding extra analysis points to plot')
            dataplot = m.scatter(self.x, self.y, latlon=True, **kwargs)

        return dataplot


class Diva2DResults(object):
    """Class that stores the results of the analysis
    """

    def __init__(self, x=None, y=None, analysis=None, error=None):
        """Creation of the Diva 2D 'Result' object using the user inputs.
        :param x: x-coordinates
        :type x: numpy array
        :param y: y-coordinates
        :type y: numpy array
        :param analysis: analysed field (2D)
        :type analysis: numpy ndarray
        :param error: error field (2D)
        :type error: numpy ndarray
        """
        logger.info("Creating Diva 2D Result object")
        if isinstance(x, np.ndarray):
            self.x = x
        elif isinstance(x, list):
            self.x = np.array(x)
        else:
            logger.debug("X vector not defined. Should be np.ndarray or list")

        if isinstance(y, np.ndarray):
            self.y = y
        elif isinstance(x, list):
            self.y = np.array(y)
        else:
            logger.debug("Y vector not defined. Should be np.ndarray or list")

        if isinstance(analysis, np.ndarray):
            if analysis.shape[0] == len(x) and analysis.shape[1] == len(y):
                logger.debug('Consistent dimensions for the analysed field')
                self.analysis = analysis
                if isinstance(error, np.ndarray):
                    if analysis.shape == error.shape:
                        logger.debug('Consistent dimensions for the error field')
                        self.error = error
                    else:
                        Exception("Dimension mismatch")
                        logger.error("Dimension mismatch")
                else:
                    logger.debug("Error field not defined")
            else:
                Exception("Dimension mismatch")
                logger.error("Dimension mismatch")
        else:
            logger.debug("Analysed field not defined")

    @classmethod
    def read_from(self, filename):
        """Read the analyzed field, the error field (if exists) and their coordinates
        from the netCDF file.
        If the error field doesn't exist, the function return a field full of NaN's.
        :param filename: name of the 'result' file
        :type filename: str
        """

        try:

            with netCDF4.Dataset(filename) as nc:
                self.x = nc.variables['x'][:]
                self.y = nc.variables['y'][:]
                self.analysis = nc.variables['analyzed_field'][:]
                try:
                    self.error = nc.variables['error_field'][:]
                except KeyError:
                    logger.warning("No error field in the netCDF file (will return NaN's)")
                    self.error = np.nan * self.analysis
        except OSError:
            logger.error("File {0} does not exist".format(filename))

    @staticmethod
    def make(divadir, datafile=None, paramfile=None, contourfile=None):
        """Perform the interpolation using script divacalc
        :param divadir: main Diva directory
        :type divadir: str
        :param datafile: path to the file containing the data
        :type datafile: str
        :param paramfile: path to the file containing the parameters
        :type paramfile: str
        :param contourfile: path to the file containing the contour(s)
        :type contourfile: str
        """

        divadirs = DivaDirectories(divamain=divadir)
        divafiles = Diva2Dfiles(divadirs.diva2d)

        if datafile is None:
            if not os.path.exists(divafiles.data):
                logger.error("No data.dat file in ./input")
                return
        else:
            try:
                shutil.copy2(datafile, divafiles.data)
            except FileNotFoundError:
                logger.error("File {0} doesn't exist".format(datafile))
                logger.error("Execution stopped")
                return

        if paramfile is None:
            if not os.path.exists(divafiles.parameter):
                logger.error("No param.par file in ./input")
                return
        else:
            try:
                shutil.copy2(paramfile, divafiles.parameter)
            except FileNotFoundError:
                logger.error("File {0} doesn't exist".format(paramfile))
                logger.error("Execution stopped")
                return

        if contourfile is None:
            if not os.path.exists(divafiles.contour):
                logger.error("No coast.cont file in ./input")
        else:
            try:
                shutil.copy2(contourfile, divafiles.contour)
            except FileNotFoundError:
                logger.error("File {0} doesn't exist".format(contourfile))
                logger.error("Execution stopped")
                return

        calcprocess = subprocess.Popen("./divacalc", cwd=divadirs.diva2d,
                                       stdout=subprocess.PIPE, shell=True)
        out = calcprocess.stdout.read()

        if logfile:
            with open(logfile, 'a') as f:
                f.write(str(out).replace('\\n', '\n'))

        # Check if analysis has been performed
        if os.path.exists(os.path.join(divadirs.diva2d, 'divawork/fort.84')):
            logger.info("Finished generation of analysis field")
            # Read the analysis from the netCDF
            Diva2DResults.read_from(divafiles.result)
        else:
            logger.error("Analysis not performed, check log for more details")



    def add_to_plot(self, field='analysis', m=None, **kwargs):
        """Add the result to the plot
        :param field: 'analysis' or 'error'
        :type field: str
        :param m: basemap projection
        :type m: mpl_toolkits.basemap.Basemap
        :return resultplot: matplotlib.collections.QuadMesh
        :type resultplot: QuadMesh
        """

        if m is None:
            logger.debug("No projection defined")
            if field == 'analysis':
                logger.debug('Adding analysed field to plot')
                resultplot = plt.pcolormesh(self.x, self.y, self.analysis, **kwargs)
                # plt.colorbar()
            elif field == 'error':
                logger.debug('Adding error field to plot')
                resultplot = plt.pcolormesh(self.x, self.y, self.error, **kwargs)
                # plt.colorbar()
            else:
                logger.error("Field selected for plot does not exist")
                logger.error("Try 'analysis' or 'error'")
                resultplot = None

        else:
            logger.debug("Applying projection to coordinates")
            xx, yy = np.meshgrid(self.x, self.y)
            if field == 'analysis':
                logger.debug('Adding analysed field to plot')
                resultplot = m.pcolormesh(xx, yy, self.analysis, ax=m.ax, latlon=True, **kwargs)
                # plt.colorbar(pcm)
                # m.ax.set_xlim(xx.min(), xx.max())
                # m.ax.set_ylim(yy.min(), yy.max())
            elif field == 'error':
                logger.debug('Adding error field to plot')
                resultplot = m.pcolormesh(xx, yy, self.error, ax=m.ax, latlon=True, **kwargs)
                # plt.colorbar(pcm)
                # m.ax.set_xlim(xx.min(), xx.max())
                # m.ax.set_ylim(yy.min(), yy.max())
            else:
                logger.error("Field selected for plot does not exist")
                logger.error("Try 'analysis' or 'error'")
                resultplot = None

        return resultplot


class Diva2DMesh(object):
    """This class stores the finite-element mesh generated by Diva.

    Example:
    =======

    Mesh = Diva2DMesh()

    The mesh is stored in 2 files:
    * the first stores the coordinates of the nodes of the triangles,
    * the second contains the mesh topology: numbers of nodes, interfaces and elements.

    The mesh is never explicitly created by the user, but rather generated by a call to the
    script **divamesh**. It is based on the contour file (coast.cont) and the parameter list
    (param.par).
    """

    def __init__(self, nnodes=None, ninterfaces=None, nelements=None,
                 xnode=None, ynode=None, i1=None, i2=None, i3=None):
        """
        :param nnodes: number of nodes in the finite-element mesh
        :type nnodes: int
        :param ninterfaces: number of interfaces in the finite-element mesh
        :type ninterfaces: int
        :param nelements: number of elements in the finite-element mesh
        :type nelements: int
        :param xnode: x-coordinates of the mesh nodes
        :type xnode: numpy.ndarray
        :param ynode: y-coordinates of the mesh nodes
        :type ynode: numpy.ndarray
        :param i1: indices of the elements
        :type i1: numpy.ndarray
        :param i2: indices of the elements
        :type i2: numpy.ndarray
        :param i3: indices of the elements
        :type i3: numpy.ndarray
        :return:
        """

        logger.info("Creating Diva 2D mesh object")
        self.nnodes = nnodes
        self.ninterfaces = ninterfaces
        self.nelements = nelements
        self.xnode = xnode
        self.ynode = ynode
        self.i1 = i1
        self.i2 = i2
        self.i3 = i3

    @staticmethod
    def make(divadir):
        """Perform the mesh generation using script divamesh

        :param divadir: main Diva directory
        :type divadir: str
        """

        divadirs = DivaDirectories(divadir)
        divafiles = Diva2Dfiles(divadirs.diva2d)

        meshprocess = subprocess.Popen("./divamesh", cwd=divadirs.diva2d,
                                       stdout=subprocess.PIPE, shell=True)
        out = meshprocess.stdout.read()

        # Check if mesh has been created
        if os.path.exists(divafiles.mesh):
            if os.path.exists(divafiles.meshtopo):
                logger.info("Finished generation of the finite-element mesh")
                # Read the mesh from the created files
                Diva2DMesh.read_from(divafiles.mesh, divafiles.meshtopo)
        else:
            logger.error("Mesh not generated, check log for more details")

        if logfile:
            with open(logfile, 'a') as f:
                f.write(str(out).replace('\\n', '\n'))

    @classmethod
    def read_from_np(cls, filename1, filename2):
        """Initialise the mesh object by reading the coordinates and the topology
        from the specified files.

        Example:
        =======

            Mesh.read_from_np(meshfile, meshtopofile)

        This function uses numpy 'loadtxt' and 'genfromtxt' methods.
        :param filename1: name of the 'mesh' file (coordinates)
        :type filename1: str
        :param filename2: name of the 'meshtopo' file (topology)
        :type filename2: str
        """
        logger.info("Creating Diva 2D mesh object")

        datamesh = np.loadtxt(filename2)
        cls.nnodes = int(datamesh[0])
        cls.ninterfaces = int(datamesh[1])
        cls.nelements = int(datamesh[2])

        # Load mesh nodes
        meshnodes = np.genfromtxt(filename1, skip_footer=cls.nelements + cls.ninterfaces)
        # meshnodes = np.fromstring(meshnodes)

        # Load mesh elements
        meshelements = np.genfromtxt(filename1, skip_header=cls.nnodes + cls.ninterfaces)
        meshelements = np.fromstring(meshelements)
        meshelements = np.int_(meshelements)

        # Extract node coordinates
        cls.xnode = meshnodes[np.arange(1, cls.nnodes * 3, 3)]
        cls.ynode = meshnodes[np.arange(2, cls.nnodes * 3, 3)]

        # Indices of the elements
        cls.i1 = meshelements[np.arange(0, cls.nelements * 6, 6)] - 1
        cls.i2 = meshelements[np.arange(2, cls.nelements * 6, 6)] - 1
        cls.i3 = meshelements[np.arange(4, cls.nelements * 6, 6)] - 1

    @classmethod
    def read_from(self, filename1, filename2):
        """Initialise the mesh object by reading the coordinates and the topology
        from the specified files.

        Example:
        =======

            Mesh.read_from(meshfile, meshtopofile)

        This function reads the files line by line using 'readline' methods
        and then convert the lists to numpy array.
        :param filename1: name of the 'mesh' file (coordinates)
        :type filename1: str
        :param filename2: name of the 'meshtopo' file (topology)
        :type filename2: str
        """
        # Read mesh topology
        with open(filename2) as f:
            self.nnodes = int(f.readline().rstrip())
            self.ninterfaces = int(f.readline().rstrip())
            self.nelements = int(f.readline().rstrip())

        # Initialise line index
        nlines = 0
        # and lists
        xnode = []
        ynode = []
        interfaces = []
        i1, i2, i3 = [], [], []

        with open(filename1, 'r') as f:
            # Read the node coordinates
            while nlines < self.nnodes:
                llines = f.readline().rsplit()
                xnode.append(float(llines[1]))
                ynode.append(float(llines[2]))
                nlines += 1
            # Read the interfaces
            while nlines < self.nnodes + self.ninterfaces:
                interfaces.append(int(f.readline().rsplit()[0]))
                nlines += 1
            # Read the elements
            while nlines < self.nnodes + self.ninterfaces + self.nelements:
                llines = f.readline().rsplit()
                i1.append(int(llines[0]) - 1)
                i2.append(int(llines[2]) - 1)
                i3.append(int(llines[4]) - 1)
                nlines += 1

        self.xnode = np.array(xnode)
        self.ynode = np.array(ynode)
        self.i1 = np.array(i1)
        self.i2 = np.array(i2)
        self.i3 = np.array(i3)

    def describe(self):
        """Summarise the mesh characteristics
        """
        print("Number of nodes: {0}".format(self.nnodes))
        print("Number of interfaces: {0}".format(self.ninterfaces))
        print("Number of elements: {0}".format(self.nelements))

    def add_to_plot(self, m=None, **kwargs):
        """Plot the finite element mesh using the line segments.

        Example:
        =======

            fig = plt.figure()
            ax =  ax = plt.subplot(111)
            Mesh.add_to_plot(edgecolor='b', facecolor='0.9', linewidth=0.5)

        The method 'add_to_plot_patch' uses matplotlib 'patch' and provide additional
        plotting options but is slower than 'add_to_plot'.

        :param m: basemap
        :type m: mpl_toolkits.basemap.Basemap
        :return meshplot: matplotlib.lines.Line2D object
        :type meshplot: list
        """

        # Create empty lists of coordinates
        xx = []
        yy = []
        # Read each element coordinates and add values that will lead to projected values
        # that will be discarded
        #
        # Previous solution: we add a NaN to avoid plotting lines joining 2 elements
        for j in range(0, self.nelements):
            xx.extend((self.xnode[self.i1[j]], self.xnode[self.i2[j]],
                       self.xnode[self.i3[j]], self.xnode[self.i1[j]], np.nan))
            yy.extend((self.ynode[self.i1[j]], self.ynode[self.i2[j]],
                       self.ynode[self.i3[j]], self.ynode[self.i1[j]], np.nan))

        if m is None:
            logger.debug("No projection defined")
            logger.debug('Adding finite-element mesh to plot')
            meshplot = plt.plot(xx, yy, **kwargs)

            logger.debug('Setting limits to axes')
            # ax.set_xlim(self.xnode.min(), self.xnode.max())
            # ax.set_ylim(self.ynode.min(), self.ynode.max())
        else:
            logger.debug("Applying projection to coordinates")
            logger.debug('Adding finite-element mesh to map')

            # Apply projection
            # (to avoid warnings if we did it through the plot
            xx, yy = m(xx, yy)
            # Mask large values
            np.ma.masked_greater(xx, 1e+20, copy=True)
            np.ma.masked_greater(yy, 1e+20, copy=True)

            meshplot = m.plot(xx, yy, latlon=False, **kwargs)

            """
            logger.debug('Setting limits to axes')
            m.ax.set_xlim(np.nanmin(xx), np.nanmax(xx))
            m.ax.set_ylim(np.nanmin(yy), np.nanmax(yy))
            """
        return meshplot

    def add_to_plot_patch(self, ax, m=None, **kwargs):
        """Plot the finite element mesh using the 'patch' function of matplotlib.

        Example:
        =======

            fig = plt.figure()
            ax =  ax = plt.subplot(111)
            Mesh.add_to_plot_patch(ax, edgecolor='b', facecolor='0.9', linewidth=0.5)

        Note that an 'ax' object should exist in order to add the patches to the plot.

        The method 'add_to_plot' uses simple lines and is recommended for meshes
        with a large number of elements.
        :param ax: axes
        :type ax: matplotlib.axes._subplots.AxesSubplot
        :param m: basemap
        :type m: mpl_toolkits.basemap.Basemap
        """

        if m is None:
            logger.debug("No projection defined")
            logger.debug('Adding finite-element mesh to plot')

            for j in range(0, self.nelements):
                verts = [(self.xnode[self.i1[j]], self.ynode[self.i1[j]]),
                         (self.xnode[self.i2[j]], self.ynode[self.i2[j]]),
                         (self.xnode[self.i3[j]], self.ynode[self.i3[j]]),
                         (self.xnode[self.i1[j]], self.ynode[self.i1[j]])]

                meshpath = path.Path(verts)
                meshpatch = patches.PathPatch(meshpath, **kwargs)
                ax.add_patch(meshpatch)

            logger.debug('Setting limits to axes')
            ax.set_xlim(self.xnode.min(), self.xnode.max())
            ax.set_ylim(self.ynode.min(), self.ynode.max())
        else:
            logger.debug("Applying projection to coordinates")
            logger.debug('Adding finite-element mesh to map')
            xnode, ynode = m(self.xnode, self.ynode)
            m.ax = ax
            for j in range(0, self.nelements):
                verts = [(xnode[self.i1[j]], ynode[self.i1[j]]),
                         (xnode[self.i2[j]], ynode[self.i2[j]]),
                         (xnode[self.i3[j]], ynode[self.i3[j]]),
                         (xnode[self.i1[j]], ynode[self.i1[j]])]
                meshpath = path.Path(verts)
                meshpatch = patches.PathPatch(meshpath, **kwargs)
                m.ax.add_patch(meshpatch)

            logger.debug('Setting limits to axes')
            m.ax.set_xlim(xnode.min(), xnode.max())
            m.ax.set_ylim(ynode.min(), ynode.max())

    def add_element_num(self, m=None, **kwargs):
        """Write the element number at the center of each triangle.
        :param m: basemap
        :type m: mpl_toolkits.basemap.Basemap

        Example:
        =======

            Mesh.add_element_num(color='r', fontsize=8)

        """

        if m is None:
            for j in range(0, self.nelements):
                xnodemean = (1. / 3.) * (self.xnode[self.i1[j]] + self.xnode[self.i2[j]] + self.xnode[self.i3[j]])
                ynodemean = (1. / 3.) * (self.ynode[self.i1[j]] + self.ynode[self.i2[j]] + self.ynode[self.i3[j]])
                plt.text(xnodemean, ynodemean, str(j + 1),
                         ha='center', va='center', **kwargs)
        else:
            xnode_proj, ynode_proj = m(self.xnode, self.ynode)
            # m.ax = ax
            for j in range(0, self.nelements):
                xnodemean = (1. / 3.) * (xnode_proj[self.i1[j]] + xnode_proj[self.i2[j]] + xnode_proj[self.i3[j]])
                ynodemean = (1. / 3.) * (ynode_proj[self.i1[j]] + ynode_proj[self.i2[j]] + ynode_proj[self.i3[j]])
                plt.text(xnodemean, ynodemean, str(j + 1),
                         ha='center', va='center', **kwargs)


def main():
    """Do something here"""


if __name__ == "__main__":
    main()
