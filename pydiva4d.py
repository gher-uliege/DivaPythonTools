__author__ = 'ctroupin'
"""User interface for diva in python
"""

import logging
import os
import numpy as np
import matplotlib.pyplot as plt
import netCDF4

# create logger with 'spam_application'
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('diva4D.log')
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
            self.contourdepth = os.path.join(self.diva4ddir, 'contourdepth')
            self.ncdfinfo = os.path.join(self.diva4ddir, 'ncdfinfo')
            self.param = os.path.join(self.diva4ddir, 'input/param.par')

            logger.info("datasource file: {0}".format(self.datasource))
            logger.info("constandrefe file: {0}".format(self.constandrefe))
            logger.info("driver file: {0}".format(self.driver))
            logger.info("monthlist file: {0}".format(self.monthlist))
            logger.info("qflist file: {0}".format(self.qflist))
            logger.info("varlist file: {0}".format(self.varlist))
            logger.info("yearlist file: {0}".format(self.yearlist))
            logger.info("contourdepth file: {0}".format(self.contourdepth))
            logger.info("ncdfinfo file: {0}".format(self.ncdfinfo))
            logger.info("param.par file: {0}".format(self.param))
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

    def __init__(self, advection_flag, ref_flag, var_year_code='00000000', var_month_code='0000'):
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
        self.advection_flag = advection_flag
        self.ref_flag = ref_flag
        self.var_year_code = var_year_code
        self.var_month_code = var_month_code

    def write_to(self, filename):
        """Write the 'constandrefe' parameter in the specified file.
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


class Driver(object):
    """Diva 4D input file that specified how the analysis will be performed: domain,
    resolution, parameters, ...
    """
    def __init__(self, extraction_flag, coast_flag, clean_flag, min_datanum,
                 param_flag, min_l, max_l, min_snr, max_snr,
                 analysisref_flag, lower_level, upper_level, netcdf4d_flag,
                 gnuplot_flag, detrend_groupnum):
        """
        :param extraction_flag: extract flag: 1 do it, 0 do nothing, -1 press coord, -10 pressure+Saunders
        :type extraction_flag: int
        :param coast_flag: Boundary lines and coastlines generation: 0 nothing, 1: contours, 2: UV, 3: 1+2
        :type coast_flag: int
        :param clean_flag: cleaning data on mesh: 1, 2: RL, 3: both, 4: 1 + outliers elimination, 5: =4+2
        :type
        :param min_datanum:
        :type min_datanum:
        :param param_flag:
        :type param_flag:
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


class Monthlist(object):
    """Diva 4D input file listing the months to be processed.
    """
    def __init__(self, monthlist):
        """
        :param monthlist: List of strings representing periods in months
        (ex: 0101, 0202)
        :type monthlist: list
        :return:
        """
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


class Qflist(object):
    """Diva 4D input file listing the Quality Flags to be considered for the data selection.
    """
    def __init__(self, qflist):
        """
        :param qflist: List of accepted quality flags for the osbervations
        :type qflist: list
        :return:
        """
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


class Varlist(object):
    """Diva 4D input file listing the variables to be selected from the ODV file(s).
    """
    def __init__(self, varlist):
        """
        :param varlist: List of variables to be processed
        :type varlist: list
        :return:
        """
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


class Yearlist(object):
    """Diva 4D input file listing the years to be processed.
    """
    def __init__(self, yearlist):
        """
        :param yearlist: List of years describing the periods to be processed
        :type yearlist: list
        """
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


class Contourdepth(object):
    """Diva 4D input file listing the depth levels on which the data have to be extracted
    and the interpolation performed.
    """
    def __init__(self, depthlist):
        """
        :param depthlist: List of depths (floats, >= 0)
        :type depthlist: list
        """
        self.depthlist = depthlist

    def write_to(self, filename):
        """Write the contour depth list in the specified file.
        :param filename: name of the file where the contour depths will be written.
        :type filename: str

        """
        with open(filename, 'w') as f:
            for depths in self.depthlist:
                f.write(''.join((str(depths), '\n')))

        logger.info("Written into file {0}".format(filename))


class Ncdfinfo(object):
    """Diva 4D input file listing metadata that will be written to the result netCDF file.
    """
    def __init__(self, title, reftime, timeval, cellmethod, institution,
                 groupemail, source, comment, authoremail, acknowlegment):
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
        :param acknowlegment: Acknowlegments
        :type acknowlegment: str
        :return:
        """
        self.title = title
        self.reftime = reftime
        self.timeval = timeval
        self.cellmethod = cellmethod
        self.institution = institution
        self.groupemail = groupemail
        self.source = source
        self.comment = comment
        self.authoremail = authoremail
        self.acknowlegment = acknowlegment

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
                             self.comment, self.authoremail, self.acknowlegment)

        with open(filename, 'w') as f:
            f.write(ncdfinfo_string)

        logger.info("Written into file {0}".format(filename))