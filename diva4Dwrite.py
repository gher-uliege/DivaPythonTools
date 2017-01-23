#!/usr/bin/python3
"""In this module the functions help for the preparation the DIVA4D input files.

The user specify a set of parameters (years to be processed,
variables to interpolate, data input files, ...),
and the DIVA input files are generated.
"""
import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')


def write_datasource(diva4ddir, datafilelist):
    """Create the "datasource" file in the specified diva4ddir.
    :param diva4ddir: Diva4D main directory
    :type diva4ddir: str
    :param datafilelist: List of ODV spreadsheet files
    :type datafilelist: list
    :return:
    """
    with open(os.path.join(diva4ddir, 'datasource'), 'w') as f:
        for datafile in datafilelist:
            f.write(' '.join((datafile, '\n')))
    logger.info("File 'datasource' written in directory {0}".format(diva4ddir))


def write_constandrefe(diva4ddir, advection_flag, ref_flag,
                       var_year_code='00000000', var_month_code='0000'):
    """Create the "constandrefe" file in the specified diva4ddir.
    :param diva4ddir: Diva4D main directory
    :type diva4ddir: str
    :param advection_flag: Flag that indicates if advection is activated
    :type advection_flag: int
    :param ref_flag: Flag that indicates if there is a reference field
    :type ref_flag: int
    :param var_year_code: Variable year code
    :type var_year_code: str
    :param var_month_code:  Variable month code
    :type var_month_code: str
    """
    constandrefe_string = ("# advection flag\n{0}\n"
                           "# reference field flag\n{1}\n"
                           "# variable year code\n{2}\n"
                           "# variable month code\n{3}").format(
        advection_flag, ref_flag, var_year_code, var_month_code)
    with open(os.path.join(diva4ddir, 'constandrefe'), 'w') as f:
        f.write(constandrefe_string)
    logger.info("File 'constandrefe' written in directory {0}".format(diva4ddir))


def write_driver(diva4ddir, extraction_flag, coast_flag, clean_flag, min_datanum,
                 param_flag, min_l, max_l, min_snr, max_snr,
                 analysisref_flag, lower_level, upper_level, netcdf4d_flag,
                 gnuplot_flag, detrend_groupnum):
    """Create the "driver" file in the specified diva4ddir. Its content
    is derived from the parameters specified by the user.
    :param diva4ddir: Diva4D main directory
    :type diva4ddir: str
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
            extraction_flag, coast_flag, clean_flag, min_datanum,
            param_flag, min_l, max_l, min_snr, max_snr,
            analysisref_flag, lower_level, upper_level, netcdf4d_flag,
            gnuplot_flag, detrend_groupnum)
    with open(os.path.join(diva4ddir, 'driver'), 'w') as f:
        f.write(driver_string)
    logger.info("File 'driver' written in directory {0}".format(diva4ddir))


def write_monthlist(diva4ddir, monthlist):
    """Create the file "monthlist" in the specified diva4ddir.
    :param diva4ddir: Diva4D main directory
    :type diva4ddir: str
    :param monthlist: List of strings representing periods in months
    (ex: 0101, 0202)
    :type monthlist: list
    """
    with open(os.path.join(diva4ddir, 'monthlist'), 'w') as f:
        for mm in monthlist:
            f.write(' '.join((mm, '\n')))

    logger.info("File 'monthlist' written in directory {0}".format(diva4ddir))


def write_qflist(diva4ddir, qflist):
    """Create the "qfList" file in the specified diva4ddir.
    :param diva4ddir: Diva4D main directory
    :type diva4ddir: str
    :param qflist: List of accepted quality flags for the osbervations
    :type qflist: list
    """
    with open(os.path.join(diva4ddir, 'qflist'), 'w') as f:
        for qf in qflist:
            f.write(' '.join((str(qf), '\n')))

    logger.info("File 'qfList' written in directory {0}".format(diva4ddir))


def write_varlist(diva4ddir, varlist):
    """Create the "varlist" file in the specified diva4ddir.
    :param diva4ddir: Diva4D main directory
    :type diva4ddir: str
    :param varlist: List of variables to be processed
    :type varlist: list
    """
    with open(os.path.join(diva4ddir, 'varlist'), 'w') as f:
        for variables in varlist:
            f.write(' '.join((variables, '\n')))

    logger.info("File 'varlist' written in directory {0}".format(diva4ddir))


def write_yearlist(diva4ddir, yearlist):
    """
    Create the "yearlist" file in the specified diva4ddir
    :param diva4ddir: Diva4D main directory
    :type diva4ddir: str
    :param yearlist: List of years describing the periods to be processed
    :type yearlist: list
    """
    with open(os.path.join(diva4ddir, 'yearlist'), 'w') as f:
        for years in yearlist:
            f.write(' '.join((years, '\n')))

    logger.info("File 'yearlist' written in directory {0}".format(diva4ddir))


def write_contourdepth(diva4dinputdir, depthlist):
    """Create the "contour.depth" file in the specified diva4ddir
    :param diva4dinputdir: Diva4D main directory
    :type diva4dinputdir: str
    :param depthlist: List of depths (floats, >= 0)
    :type depthlist: list
    """
    with open(os.path.join(diva4dinputdir, 'contour.depth'), 'w') as f:
        for depths in depthlist:
            f.write(' '.join((str(depths), '\n')))

    logger.info("File 'contour.depth' written in directory {0}".format(diva4dinputdir))


def write_ncdfinfo(diva4dinputdir, ncdf_title, ncdf_reftime, ncdf_timeval, ncdf_cellmethod,
                   ncdf_institution, ncdf_groupemail, ncdf_source,
                   ncdf_comment, ncdf_authoremail, ncdf_acknowlegment):
    """Create the "NCDFinfo" file in the specified Diva4D input directory.
    :param diva4dinputdir: Diva4D main directory
    :type diva4dinputdir: str
    :param ncdf_title:
    :type ncdf_title: str
    :param ncdf_reftime: Reference time for data (if not climatological data)
    :type ncdf_reftime: str
    :param ncdf_timeval: Time value (if not climatological data)
    :type ncdf_timeval: float
    :param ncdf_cellmethod: Cell_method string
    :type ncdf_cellmethod: str
    :param ncdf_institution: Institution name: where the dataset was produced.
    :type ncdf_institution: str
    :param ncdf_groupemail: Production group and e-mail
    :type ncdf_groupemail: str
    :param ncdf_source: Source (observation, radiosonde, database, model-generated data,...)
    :type ncdf_source: str
    :param ncdf_comment: Comment
    :type ncdf_comment: str
    :param ncdf_authoremail: Author e-mail address (or contact person to report problems)
    :type ncdf_authoremail: str
    :param ncdf_acknowlegment: Acknowlegments
    :type ncdf_acknowlegment: str
    """
    ncdfinfo_string =\
    ("Title string for 3D NetCDF file:\n"
     "{0}\n"
     "Reference time for data (ie: days since since 1900-01-01), if not climatological data\n"
     "{1}\n"
     "Time value (that reprsents the data set), if not climatological data\n"
     "{2}\n"
     "Cell_methode string:\n"
     "{3}\n"
     "Institution name: where the dataset was produced.\n"
     "{4}\n"
     "Production group and e-mail\n"
     "{5}\n"
     "Source (observation, radiosonde, database, model-generated data,...)\n"
     "{6}\n"
     "Comment\n"
     "{7}\n"
     "Author e-mail address (or contact person to report problems)\n"
     "{8}\n"
     "Acknowledgements\n"
     "{9}").format(ncdf_title, ncdf_reftime, ncdf_timeval, ncdf_cellmethod,
                   ncdf_institution, ncdf_groupemail, ncdf_source,
                   ncdf_comment, ncdf_authoremail, ncdf_acknowlegment)

    with open(os.path.join(diva4dinputdir, 'NCDFinfo'), 'w') as f:
        f.write(ncdfinfo_string)

    logger.info("File 'NCDFinfo' written in directory {0}".format(diva4dinputdir))
