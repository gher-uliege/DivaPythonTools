#!/usr/bin/python3
'''
In this module the functions help for the preparation the DIVA4D input files.

The user specify a set of parameters (years to be processed,
variables to interpolate, data input files, ...),
and the DIVA input files are generated.
'''
import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')

def diva_directories(divadir):
    """Create directory names based on the Diva main directory.
    :param diva4Ddir: Diva4D main directory
    :type diva4Ddir: str
    :return divabindir: Diva binary directory
    """
    if os.path.isdir(divadir):
        logging.debug("{0} already exists".format(divadir))
        divabindir = os.path.join(divadir, 'DIVA3D/bin')
        divasrcdir = os.path.join(divadir, 'DIVA3D/src/Fortran')
        diva2Ddir = os.path.join(divadir, 'DIVA3D/divastripped')
        diva4Ddir = os.path.join(divadir, 'JRA4/Climatology')
        return divabindir, divasrcdir, diva2Ddir, diva4Ddir
    else:
        logger.error("%{0} is not a directory or doesn't exist".format(divadir))
        return '', '', '', ''


def write_datasource(diva4Ddir, datafilelist):
    '''Create the "datasource" file in the specified diva4Ddir.
    :param diva4Ddir: Diva4D main directory
    :type diva4Ddir: str
    :param datafilelist: List of ODV spreadsheet files
    :type datafilelist: list
    :return:
    '''
    with open(os.path.join(diva4Ddir, 'datasource'), 'w') as f:
        for datafile in datafilelist:
            f.write(' '.join((datafile, '\n')))
    logger.info("File 'datasource' written in directory {0}".format(diva4Ddir))


def write_constandrefe(diva4Ddir, advection_flag, ref_flag,
                       var_year_code='00000000', var_month_code='0000'):
    '''Create the "constandrefe" file in the specified diva4Ddir.
    :param diva4Ddir: Diva4D main directory
    :type diva4Ddir: str
    '''
    constandrefeString = ("# advection flag\n{0}\n"
                          "# reference field flag\n{1}\n"
                          "# variable year code\n{2}\n"
                          "# variable month code\n{3}").format(
                          advection_flag, ref_flag, var_year_code, var_month_code
                          )
    with open(os.path.join(diva4Ddir, 'constandrefe'), 'w') as f:
        f.write(constandrefeString)
    logger.info("File 'constandrefe' written in directory {0}".format(diva4Ddir))


def write_driver(diva4Ddir, extraction_flag, coast_flag, clean_flag, min_datanum,
                 param_flag, min_l, max_l, min_snr, max_snr,
                 analysisref_flag, lower_level, upper_level, netcdf4d_flag,
                 gnuplot_flag, detrend_groupnum):
    '''Create the "driver" file in the specified diva4Ddir. Its content
    is derived from the parameters specified by the user.
    :param diva4Ddir: Diva4D main directory
    :type diva4Ddir: str
    '''
    driverString = \
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
    with open(os.path.join(diva4Ddir, 'driver'), 'w') as f:
        f.write(driverString)
    logger.info("File 'driver' written in directory {0}".format(diva4Ddir))


def write_monthlist(diva4Ddir, monthList):
    '''Create the file "monthlist" in the specified diva4Ddir.
    :param diva4Ddir: Diva4D main directory
    :type diva4Ddir: str
    :param monthList: List of strings representing periods in months
    (ex: 0101, 0202)
    :type monthList: list
    '''
    with open(os.path.join(diva4Ddir, 'monthlist'), 'w') as f:
        for mm in monthList:
            f.write(' '.join((mm, '\n')))

    logger.info("File 'monthlist' written in directory {0}".format(diva4Ddir))


def write_qflist(diva4Ddir, qfList):
    '''Create the "qfList" file in the specified diva4Ddir.
    :param diva4Ddir: Diva4D main directory
    :type diva4Ddir: str
    qfList is a list of integers
    '''
    with open(os.path.join(diva4Ddir, 'qflist'), 'w') as f:
        for qf in qfList:
            f.write(' '.join((str(qf), '\n')))

    logger.info("File 'qfList' written in directory {0}".format(diva4Ddir))


def write_varlist(diva4Ddir, varList):
    '''Create the "varlist" file in the specified diva4Ddir.
    :param diva4Ddir: Diva4D main directory
    :type diva4Ddir: str
    varList is a list of strings
    '''
    with open(os.path.join(diva4Ddir, 'varlist')) as f:
        for vars in varList:
            f.write(' '.join(vars, '\n'))

    logger.info("File 'varlist' written in directory {0}".format(diva4Ddir))


def write_yearlist(diva4Ddir, yearList):
    '''
    Create the "yearlist" file in the specified diva4Ddir
    :param diva4Ddir: Diva4D main directory
    :type diva4Ddir: str
    varList is a list of strings
    '''
    with open(os.path.join(diva4Ddir, 'yearlist'), 'w') as f:
        for years in yearList:
            f.write(' '.join(years, '\n'))

    logger.info("File 'yearlist' written in directory {0}".format(diva4Ddir))


def write_contourdepth(diva4Ddir, depthList):
    '''Create the "contour.depth" file in the specified diva4Ddir
    :param diva4Ddir: Diva4D main directory
    :type diva4Ddir: str
    varList is a list of floats
    '''
    with open(os.path.join(diva4Ddir, 'contour.depth'), 'w') as f:
        for depths in depthList:
            f.write(' '.join(depths, '\n'))

    logger.info("File 'contour.depth' written in directory {0}".format(diva4Ddir))


def write_ncdfinfo(diva4Dinputdir, ncdf_title, ncdf_reftime, ncdf_timeval, ncdf_cellmethod,
                   ncdf_institution, ncdf_groupemail, ncdf_source,
                   ncdf_comment, ncdf_authoremail, ncdf_acknowlegment):
    '''Create the "NCDFinfo" file in the specified Diva4D input directory.
    :param diva4Ddir: Diva4D main directory
    :type diva4Ddir: str
    '''
    ncdfInfoString =\
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

    with open(os.path.join(diva4Dinputdir, 'NCDFinfo'), 'w') as f:
        f.write(ncdfInfoString)

    logger.info("File 'NCDFinfo' written in directory {0}".format(diva4Dinputdir))
