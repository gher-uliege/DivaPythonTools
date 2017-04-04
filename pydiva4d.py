__author__ = 'ctroupin'
"""User interface for diva in python
"""

import logging
import os
from pydiva2d import *
import numpy as np
import matplotlib.pyplot as plt
import netCDF4

# If we want to have a specific logger for the messages depending on Diva4D
# Probably not necessary
logger = divalogger(__name__, logfile)

class Diva4DDirectories(DivaDirectories):
    """Object storing the paths to the main Diva 4D directories: input, output,
    mesh, fields, execution directory, ...
    """
    def __init__(self, divamain):

        if os.path.isdir(divamain):
            self.divamain = divamain
            DivaDirectories.__init__(self, divamain)
            self.diva4dinput = os.path.join(self.diva4d, 'JRA4/Climatology/input')
            self.diva4doutput = os.path.join(self.diva4d, 'output/')
            self.diva4dmesh = os.path.join(self.diva4d, 'newinput/divamesh/')
            self.diva4dparam = os.path.join(self.diva4d, 'newinput/divaparam/')
            self.diva4dfields = os.path.join(self.diva4d, 'output/3Danalysis/Fields')

            logger.info('Diva 4D input directory: {0}'.format(self.diva4dinput))
            logger.info('Diva 4D output directory: {0}'.format(self.diva4doutput))
            logger.info('Diva 4D mesh directory: {0}'.format(self.diva4dmesh))
            logger.info('Diva 4D parameter directory: {0}'.format(self.diva4dparam))
            logger.info('Diva 4D field directory: {0}'.format(self.diva4dfields))
        else:
            logging.error("{0} is not a directory or doesn't exist".format(divamain))


class Diva4Dfiles(object):
    """Diva 4D input and output files names based on the main Diva directory
    """
    def __init__(self, diva4ddir):
        """If the directory 'diva4ddir' exists, create file names of the input files required by Diva 4D.
        :param diva4ddir: Diva 4D main directory (usually ending by 'Climatology/')
        :type diva4ddir: str
        :return:
        """
        self.diva4ddir = diva4ddir

        if os.path.isdir(self.diva4ddir):
            self.datasource = os.path.join(self.diva4ddir, 'datasource')
            self.constandrefe = os.path.join(self.diva4ddir, 'constandrefe')
            self.driver = os.path.join(self.diva4ddir, 'driver')
            self.monthlist = os.path.join(self.diva4ddir, 'monthlist')
            self.qflist = os.path.join(self.diva4ddir, 'qflist')
            self.varlist = os.path.join(self.diva4ddir, 'varlist')
            self.yearlist = os.path.join(self.diva4ddir, 'yearlist')
            self.contourdepth = os.path.join(self.diva4ddir, 'input/contour.depth')
            self.ncdfinfo = os.path.join(self.diva4ddir, 'ncdfinfo')
            self.param = os.path.join(self.diva4ddir, 'input/param.par')
            logger.info("Creating Diva 4D file names and paths")
            logger.info("datasource file:   {0}".format(self.datasource))
            logger.info("constandrefe file: {0}".format(self.constandrefe))
            logger.info("driver file:       {0}".format(self.driver))
            logger.info("monthlist file:    {0}".format(self.monthlist))
            logger.info("qflist file:       {0}".format(self.qflist))
            logger.info("varlist file:      {0}".format(self.varlist))
            logger.info("yearlist file:     {0}".format(self.yearlist))
            logger.info("contourdepth file: {0}".format(self.contourdepth))
            logger.info("ncdfinfo file:     {0}".format(self.ncdfinfo))
            logger.info("param.par file:    {0}".format(self.param))
        else:
            logging.error("%{0} is not a directory or doesn't exist".format(self.diva4ddir))


class Datasource(object):
    """Diva 4D input file listing the ODV spreasheet file(s) containing the observations.
    """

    def __init__(self, datafilelist=None):
        """
        :param datafilelist: List of ODV spreadsheet files
        :type datafilelist: list
        """
        logger.info("Creating Diva 4D Datasource object")

        if datafilelist is None:
            datafilelist = []
        elif isinstance(datafilelist, str):
            datafilelist = datafilelist.split()
            logger.warning('Argument converted from string to list')
        self.datafilelist = datafilelist

    def write_to(self, filename):
        """Write the names of the files containing the data
         in the 'datasource' file .
        :param filename: the name of the 'datasource' file
        :type filename: str
        :return:
        """

        with open(filename, 'w') as f:
            for datafile in self.datafilelist:
                f.write(''.join((datafile, '\n')))
        logger.info("Written into file {0}".format(filename))

    def read_from(self, filename):
        """Read the data sources from an existing file containing
        a list of ODV files and add it to the existing list.
        """
        try:
            with open(filename, 'r') as f:
                for lines in f:
                    self.datafilelist.append(lines.rstrip('\n'))
        except FileNotFoundError:
            logging.error("File {0} not found".format(filename))

        logger.info("Read from file {0}".format(filename))


class Constandrefe(object):
    """Diva 4D input file listing parameters for the generation of reference fields
    and advection.
    """

    def __init__(self, advection_flag=0, ref_flag=0, var_year_code='00000000', var_month_code='0000'):
        """
        :param advection_flag: Flag that indicates if advection is activated
        :type advection_flag: int
        :param ref_flag: Flag that indicates if there is a reference field
        :type ref_flag: int
        :param var_year_code: Variable year code
        :type var_year_code: str
        :param var_month_code: Variable month code
        :type var_month_code: str
        :return:
        """
        logger.info("Creating Diva 4D Constandrefe object")
        self.advection_flag = advection_flag
        self.ref_flag = ref_flag
        self.var_year_code = var_year_code
        self.var_month_code = var_month_code

    def write_to(self, filename):
        """Write the 'constandrefe' parameters in the specified file.
        :param filename: name of the file where the parameters will be written.
        :param filename: str
        """
        constandrefe_string = ("# advection flag\n{0}\n"
                               "# reference field flag\n{1}\n"
                               "# variable year code\n{2}\n"
                               "# variable month code\n{3}").format(
            self.advection_flag, self.ref_flag, self.var_year_code, self.var_month_code)

        with open(os.path.join(filename), 'w') as f:
            f.write(constandrefe_string)

        logger.info("Written into file {0}".format(filename))

    def read_from(self, filename):
        """Get the 'constandrefe' parameters from an existing file.

        :type self: object
        :param filename: name of the file where the contour depths are written.
        :type filename: str
        """
        if os.path.exists(filename):
            logger.info("Reading 'constandrefe' parameters from file {0}".format(filename))
            # Start with empty list
            constandrefe_param = []
            with open(filename, 'r') as f:
                line = f.readline()
                # Continue until line is empty
                while line:
                    constandrefe_param.append(line.rstrip())
                    line = f.readline()

            # Keep only the odd lines
            advection_flag, ref_flag, var_year_code, var_month_code = constandrefe_param[1::2]
            # Change to integer type if necessary
            self.advection_flag = int(advection_flag)
            self.ref_flag = int(ref_flag)
            self.var_year_code = var_year_code
            self.var_month_code = var_month_code
        else:
            logger.error("File {0} does not exist".format(filename))
            raise FileNotFoundError('File does not exist')


class Driver(object):
    """Diva 4D input file that specified how the analysis will be performed: domain,
    resolution, parameters, data extraction...
    """
    def __init__(self, extraction_flag=0, coast_flag=0, clean_flag=0, min_datanum=0,
                 param_flag=0, min_l=0.0, max_l=1000., min_snr=0.0, max_snr=1000.,
                 analysisref_flag=0, lower_level=None, upper_level=None, netcdf4d_flag=0,
                 gnuplot_flag=0, detrend_groupnum=0):
        """
        :param extraction_flag: extract flag: 1 do it, 0 do nothing, -1 press coord, -10 pressure+Saunders
        :type extraction_flag: int
        :param coast_flag: Boundary lines and coastlines generation: 0 nothing, 1: contours, 2: UV, 3: 1+2
        :type coast_flag: int
        :param clean_flag: cleaning data on mesh: 1, 2: RL, 3: both, 4: 1 + outliers elimination, 5: =4+2
        :type clean_flag: int
        :param min_datanum: Minimal number of data in a layer
        :type min_datanum: int
        :param param_flag: Parameters estimation and vertical filtering
        :type param_flag: int
        :param min_l: Minimal correlation length during optimization
        :type min_l: float
        :param max_l: Maximal correlation length during optimization
        :type max_l: float
        :param min_snr: Minimal signal-to-noise ratio during optimization
        :type min_snr: float
        :param max_snr: Maximal signal-to-noise ratio during optimization
        :type max_snr: float
        :param analysisref_flag: Flag for the creation of reference field.
        2 do reference, 1 do analysis and 0 do nothing
        :type analysisref_flag: int
        :param lower_level: Depth lower level number
        :type lower_level: int
        :param upper_level: Depth upper level number
        :type upper_level: int
        :param netcdf4d_flag: 4D netcdf climatology file
        :type netcdf4d_flag: int
        :param gnuplot_flag: Gnutplot flag 0 or 1
        :type gnuplot_flag: int
        :param detrend_groupnum: Number of groups for data detrending, 0 if no detrending.
        :type detrend_groupnum: int
        :return:
        """
        logger.info("Creating Diva 4D Driver object")
        self.extraction_flag = extraction_flag
        self.coast_flag = coast_flag
        self.clean_flag = clean_flag
        self.min_datanum = min_datanum
        self.param_flag = param_flag
        self.min_l = min_l
        self.max_l = max_l
        self.min_snr = min_snr
        self.max_snr = max_snr
        self.analysisref_flag = analysisref_flag
        self.lower_level = lower_level
        self.upper_level = upper_level
        self.netcdf4d_flag = netcdf4d_flag
        self.gnuplot_flag = gnuplot_flag
        self.detrend_groupnum = detrend_groupnum

    def write_to(self, filename):
        """Write the 'driver' parameter in the specicfied filefile in the specified diva4ddir.
        :param filename: name of the file where the driver parameters will be written.
        :param filename: str
        """
        driver_string = \
            ("Data extraction: 1 do it, 0 do nothing, -1 press coord, -10 pressure+Saunders\n{0}\n"
             "boundary lines and coastlines generation: 0 nothing, 1: contours, 2: UV, 3: 1+2\n{1}\n"
             "cleaning data on mesh: 1, 2: RL, 3: both, 4: 1 + outliers elimination, 5: =4+2\n{2}\n"
             "minimal number of data in a layer. If less, uses data from any month.\n{3}\n"
             "Parameters estimation and vertical filtering:\n{4}\n"
             "Minimal L\n{5}\n"
             "Maximal L\n{6}\n"
             "Minimal SN\n{7}\n"
             "Maximal SN\n{8}\n"
             "Analysis and reference field:\n{9}\n"
             "lowerlevel number\n{10}\n"
             "upperlevel number\n{11}\n"
             "4D netcdf files generation:\n{12}\n"
             "gnuplot plots: 0 or 1\n{13}\n"
             "Data detrending: number of groups, 0 if no detrending.\n{14}\n").format(
                self.extraction_flag, self.coast_flag, self.clean_flag, self.min_datanum,
                self.param_flag, self.min_l, self.max_l, self.min_snr, self.max_snr,
                self.analysisref_flag, self.lower_level, self.upper_level, self.netcdf4d_flag,
                self.gnuplot_flag, self.detrend_groupnum)

        with open(filename, 'w') as f:
            f.write(driver_string)
        logger.info("Written into file {0}".format(filename))

    def read_from(self, filename):
        """Get the 'driver' parameters from an existing file.

        :type self: object
        :param filename: name of the file where the driver parameters are written.
        :type filename: str
        """
        if os.path.exists(filename):
            logger.info("Reading 'driver' parameters from file {0}".format(filename))
            # Start with empty list
            driver_param = []
            with open(filename, 'r') as f:
                line = f.readline()
                # Continue until line is empty
                while line:
                    driver_param.append(line.rstrip())
                    line = f.readline()

            # Keep only the odd lines
            extraction_flag, coast_flag, clean_flag, min_datanum,\
                param_flag, min_l, max_l, min_snr, max_snr, analysisref_flag,\
                lower_level, upper_level, netcdf4d_flag, gnuplot_flag, detrend_groupnum = driver_param[1::2]

            # Change to integer type if necessary
            self.extraction_flag = int(extraction_flag)
            self.coast_flag = int(coast_flag)
            self.clean_flag = int(clean_flag)
            self.min_datanum = int(min_datanum)
            self.param_flag = int(param_flag)
            self.min_l = float(min_l)
            self.max_l = float(max_l)
            self.min_snr = float(min_snr)
            self.max_snr = float(max_snr)
            self.analysisref_flag = int(analysisref_flag)
            self.lower_level = int(lower_level)
            self.upper_level = int(upper_level)
            self.netcdf4d_flag = int(netcdf4d_flag)
            self.gnuplot_flag = int(gnuplot_flag)
            self.detrend_groupnum = int(detrend_groupnum)
        else:
            logger.error("File {0} does not exist".format(filename))
            raise FileNotFoundError('File does not exist')


class Monthlist(object):
    """Diva 4D input file listing the month periods to be processed.

    Example:
    =======

        MonthList = MonthList(['0101', '0202']

    """
    def __init__(self, monthlist=None):
        """
        :param monthlist: List of strings representing periods in months
        (ex: 0101, 0202)
        :type monthlist: list
        :return:
        """
        logger.info("Creating Diva 4D Monthlist object")
        if monthlist is None:
            self.monthlist = []
        else:
            if isinstance(monthlist, str):
                logger.debug("Converting string to list")
                monthlist = [monthlist]
            self.monthlist = monthlist

    def write_to(self, filename):
        """Write the month list in the specified file.
        :param filename: name of the file where the parameters will be written.
        :param filename: str
        """
        with open(filename, 'w') as f:
            for mm in self.monthlist:
                f.write(''.join((mm, '\n')))
        logger.info("Written in file {0}".format(filename))

    def read_from(self, filename):
        """Get the 'monthlist' values from an existing file.

        Example:
        =======

            Monthlist.read_from(monthlistfile)

        If the 'monthlist' is already defined, the use of 'read_from' will discard
        the previous values.

        :type self: object
        :param filename: name of the file where the month periods are written.
        :type filename: str
        """
        if os.path.exists(filename):
            logger.info("Reading 'monthlist' values from file {0}".format(filename))
            # Start with empty list
            self.monthlist = []
            with open(filename, 'r') as f:
                line = f.readline()
                # Continue until line is empty
                while line:
                    self.monthlist.append(line.rstrip())
                    line = f.readline()
        else:
            logger.error("File {0} does not exist".format(filename))
            raise FileNotFoundError('File does not exist')


class Qflist(object):
    """Diva 4D input file listing the Quality Flags to be considered for the data selection.

    Example:
    =======

    Qflist = Qflist([0, 1, 2])

    """
    def __init__(self, qflist=None):
        """
        :param qflist: List of accepted quality flags (integers) for the observations
        :type qflist: list
        :return:
        """
        logger.info("Creating Diva 4D Qflist object")
        if qflist is None:
            self.qflist = []
        else:
            if isinstance(qflist, int):
                logger.debug("Converting integer to list")
                qflist = [qflist]
            self.qflist = qflist

    def write_to(self, filename):
        """Write the QF list in the specified file.
        :param filename: name of the file where the QF values will be written.
        :param filename: str
        """
        with open(filename, 'w') as f:
            for qf in self.qflist:
                f.write(''.join((str(qf), '\n')))
        logger.info("Written in file {0}".format(filename))

    def read_from(self, filename):
        """Get the 'qflist' values from an existing file.

        Example:
        =======

            Qflist.read_from(qflistfile)

        If the 'qflist' is already defined, the use of 'read_from' will discard
        the previous values.

        :type self: object
        :param filename: name of the file where the QF values are written.
        :type filename: str
        """
        if os.path.exists(filename):
            logger.info("Reading 'qflist' values from file {0}".format(filename))
            # Start with empty list
            self.qflist = []
            with open(filename, 'r') as f:
                line = f.readline()
                # Continue until line is empty
                while line:
                    self.qflist.append(int(line.rstrip()))
                    line = f.readline()
        else:
            logger.error("File {0} does not exist".format(filename))
            raise FileNotFoundError('File does not exist')


class Varlist(object):
    """Diva 4D input file listing the variables ('strings') to be selected from the ODV file(s).

    The variable names should be those found in the ODV files.

    Example:
    =======

        Varlist = Varlist(['Temperature', 'Salinity'])

    """
    def __init__(self, varlist=None):
        """
        :param varlist: List of variables to be processed
        :type varlist: list
        :return:
        """
        logger.info("Creating Diva 4D Varlist object")
        if varlist is None:
            self.varlist = []
        else:
            if isinstance(varlist, str):
                logger.debug("Converting string to list")
                varlist = [varlist]
            self.varlist = varlist

    def write_to(self, filename):
        """Write the variable list in the specified file.
        :param filename: name of the file where the variables will be written.
        :type filename: str
        """
        with open(filename, 'w') as f:
            for variables in self.varlist:
                f.write(''.join((variables, '\n')))

        logger.info("Written in file {0}".format(filename))

    def read_from(self, filename):
        """Get the list of variables from an existing file.

        Example:
        =======

            Varlist.read_from(varlistfile)

        If the 'varlist' is already defined, the use of 'read_from' will discard
        the previous values.

        :type self: object
        :param filename: name of the file where the variable names are written.
        :type filename: str
        """
        if os.path.exists(filename):
            logger.info("Reading list of variables from file {0}".format(filename))
            # Start with empty list
            self.varlist = []
            with open(filename, 'r') as f:
                line = f.readline()
                # Continue until line is empty
                while line:
                    self.varlist.append(line.rstrip())
                    line = f.readline()
        else:
            logger.error("File {0} does not exist".format(filename))
            raise FileNotFoundError('File does not exist')


class Yearlist(object):
    """Diva 4D input file listing the years to be processed.

    Example:
    =======

        Yearlist = Yearlist(['19502000'])

    """
    def __init__(self, yearlist=None):
        """
        :param yearlist: List of years describing the periods to be processed
        :type yearlist: list
        """
        logger.info("Creating Diva 4D Yearlist object")
        if yearlist is None:
            self.yearlist = []
        else:
            if isinstance(yearlist, str):
                logger.debug("Converting string to list")
                yearlist = [yearlist]
            self.yearlist = yearlist

    def write_to(self, filename):
        """Write the year list in the specified file.
        :param filename: name of the file where the selected year will be written.
        :type filename: str
        """
        with open(filename, 'w') as f:
            for years in self.yearlist:
                f.write(''.join((years, '\n')))

        logger.info("Written into file {0}".format(filename))

    def read_from(self, filename):
        """Get the list of year periods from an existing file.

        Example:
        =======

            Yearlist.read_from(yearlistfile)

        If the 'yearlist' is already defined, the use of 'read_from' will discard
        the previous values.

        :type self: object
        :param filename: name of the file where the variable names are written.
        :type filename: str
        """
        if os.path.exists(filename):
            logger.info("Reading list of variables from file {0}".format(filename))
            # Start with empty list
            self.yearlist = []
            with open(filename, 'r') as f:
                line = f.readline()
                # Continue until line is empty
                while line:
                    self.yearlist.append(line.rstrip())
                    line = f.readline()
        else:
            logger.error("File {0} does not exist".format(filename))
            raise FileNotFoundError('File does not exist')


class Contourdepth(object):
    """Diva 4D input file listing the depth levels on which the data have to be extracted
    and the interpolation performed.

    Example:
    =======

        Contourdepth = Contourdepth([200, 100., 50., 0.])

    """
    def __init__(self, depthlist=None):
        """
        :param depthlist: List of depths (floats, >= 0)
        :type depthlist: list
        """
        logger.info("Creating Diva 4D Contourdepth object")
        if depthlist is None:
            self.depthlist = []
        else:
            if isinstance(depthlist, (int, float)):
                logger.debug("Converting integer or float to list")
                depthlist = [depthlist]
            logger.debug("Ordering list of depths in decreasing order")
            depthlist.sort(reverse=True)
            self.depthlist = depthlist

            if any(x < 0 for x in depthlist):
                logger.warning("Depth levels should be defined as positive values")

    def write_to(self, filename):
        """Write the contour depth list in the specified file.
        :param filename: name of the file where the contour depths will be written.
        :type filename: str

        """
        with open(filename, 'w') as f:
            for depths in self.depthlist:
                f.write(''.join((str(depths), '\n')))

        logger.info("Written into file {0}".format(filename))

    def read_from(self, filename):
        """Get the depth contour from an already existing 'contour.depth' file.
        :param filename: name of the file where the contour depths are written.
        :type filename: str
        """
        depthlist = []
        if os.path.exists(filename):
            logger.info("Reading depth levels from file {0}".format(filename))
            with open(filename, 'r') as f:
                line = f.readline()
                while len(line) > 0:
                    depthlist.append(float(line.split()[0]))
                    line = f.readline()
            self.depthlist = depthlist
        else:
            logger.error("File {0} does not exist".format(filename))
            raise FileNotFoundError('File does not exist')


class Ncdfinfo(object):
    """Diva 4D input file listing metadata that will be written to the result netCDF file.
    """
    def __init__(self, title=None, reftime=None, timeval=None, cellmethod=None, institution=None,
                 groupemail=None, source=None, comment=None, authoremail=None, acknowledgment=None):
        """
        :param title: title of the netCDF file
        :type title: str
        :param reftime: Reference time for data (if not climatological data)
        :type reftime: str
        :param timeval: Time value (if not climatological data)
        :type timeval: float
        :param cellmethod: Cell_method string
        :type cellmethod: str
        :param institution: Institution name: where the dataset was produced.
        :type institution: str
        :param groupemail: Production group and e-mail
        :type groupemail: str
        :param source: Source (observation, radiosonde, database, model-generated data,...)
        :type source: str
        :param comment: Comment
        :type comment: str
        :param authoremail: Author e-mail address (or contact person to report problems)
        :type authoremail: str
        :param acknowledgment: acknowledgment
        :type acknowledgment: str
        :return:
        """
        logger.info("Creating Diva 4D Ncdfinfo object")
        self.title = title
        self.reftime = reftime
        self.timeval = timeval
        self.cellmethod = cellmethod
        self.institution = institution
        self.groupemail = groupemail
        self.source = source
        self.comment = comment
        self.authoremail = authoremail
        self.acknowledgment = acknowledgment

    def write_to(self, filename):
        """Write the netCDF metadata information in the specified file.
        :param filename: name of the file where the netCDF metadata information will be written.
        :type filename: str

        """
        ncdfinfo_string =\
            ('Title string for 3D NetCDF file:\n'
             "'{0}'\n"
             'Reference time for data (ie: days since since 1900-01-01), if not climatological data\n'
             "'{1}'\n"
             'Time value (that represents the data set), if not climatological data\n'
             "{2}\n"
             'Cell_methode string:\n'
             "'{3}'\n"
             'Institution name: where the dataset was produced.\n'
             "'{4}'\n"
             'Production group and e-mail\n'
             "'{5}'\n"
             'Source (observation, radiosonde, database, model-generated data,...)\n'
             "'{6}'\n"
             'Comment\n'
             "'{7}'\n"
             'Author e-mail address (or contact person to report problems)\n'
             "'{8}'\n"
             'Acknowledgements\n'
             "'{9}'").format(self.title, self.reftime, self.timeval, self.cellmethod,
                             self.institution, self.groupemail, self.source,
                             self.comment, self.authoremail, self.acknowledgment)

        with open(filename, 'w') as f:
            f.write(ncdfinfo_string)

        logger.info("Written into file {0}".format(filename))

    def read_from(self, filename):
        """Get the netCDF metadata information from an existing 'Ncdfinfo' file.

        :type self: object
        :param filename: name of the file where the contour depths are written.
        :type filename: str
        """
        if os.path.exists(filename):
            logger.info("Reading netCDF metadata from file {0}".format(filename))
            # Start with empty list
            ncdfinfo = []
            with open(filename, 'r') as f:
                line = f.readline()
                # Continue until line is empty
                while line:
                    ncdfinfo.append(line.rstrip())
                    line = f.readline()
            self.title, self.reftime, self.timeval, self.cellmethod,\
                self.institution, self.groupemail, self.source, self.comment,\
                self.authoremail, self.acknowledgment = ncdfinfo[1::2]
        else:
            logger.error("File {0} does not exist".format(filename))
            raise FileNotFoundError('File does not exist')
