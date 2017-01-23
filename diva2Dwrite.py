
import os
import logging


def make_diva_directorynames(divadir):
    """Create directory names based on the Diva main directory.
    :param divadir: Diva 4D main directory
    :type divadir: str
    :return divabindir: Diva binary directory
    :return divasrcdir: Diva source directory
    :return diva2ddir: Main 2D directory (divastripped)
    :return diva4ddir: Main 4D directory (Climatology)
    :return diva4Dinputdir: input directory for the 4D
    """
    if os.path.isdir(divadir):
        logging.debug("{0} exists".format(divadir))
        divabindir = os.path.join(divadir, 'DIVA3D/bin')
        divasrcdir = os.path.join(divadir, 'DIVA3D/src/Fortan')
        diva2ddir = os.path.join(divadir, 'DIVA3D/divastripped')
        diva4ddir = os.path.join(divadir, 'JRA4/Climatology')
        diva4Dinputdir = os.path.join(divadir, 'JRA4/Climatology/input')
        return divabindir, divasrcdir, diva2ddir, diva4ddir, diva4Dinputdir
    else:
        logging.error("%{0} is not a directory or doesn't exist".format(divadir))
        return '', '', '', ''


def make_diva2D_filenames(diva2ddir):
    """Generate the input file names and location based on the diva2D main directory.
    :param diva2ddir: Diva 2D main directory
    :type diva2ddir; str
    :return contourfile: Name of the contour file
    :return parameterfile:Name of the parameter file
    :return datafile: Name of the data file
    :return valatxyfile: Name of the valatxy file (list of positions
    where the field has to be interpolated
    """
    
    contourfile = os.path.join(diva2ddir, 'input/coast.cont')
    parameterfile = os.path.join(diva2ddir, 'input/param.par')
    datafile = os.path.join(diva2ddir, 'input/data.dat')
    valatxyfile = os.path.join(diva2ddir, 'input/valatxy.coord')
    return contourfile, datafile, parameterfile, valatxyfile


def write_contour(contours, contourfile):
    """Write the contours (list of list of tuples)
    into the specified contour file.
    """
    ncontours = len(contours)
    with open(contourfile, 'w') as f:
        f.write(str(ncontours) + '\n')
        for n, contour in enumerate(contours):
            npoints = len(contour)
            logging.debug("Sub-contour no. {0} has {1} points".format(n, npoints))
            f.write(str(npoints) + '\n')
            for points in contour:
                line = ' '.join(str(x) for x in points)
                f.write(line + '\n')
    logging.info("Writen contour file {0} \ncontaining {1} contours".format(contourfile, ncontours))
        

def write_data(data, datafile):
    """Write the data points (list of tuples, each tuple with 3 or 4 values)
    into the specified data file.
    """
    ndata = len(data)
    with open(datafile, 'w') as f:
        for datapoints in data:
            line = ' '.join(str(x) for x in datapoints)
            f.write(line + '\n')
    logging.info("Written data file {0} \ncontaining {1} data points".format(datafile, ndata))


def write_parameter(correlationlength, icoordchange, ispec, irtg,
                    xmin, ymin, dx, dy, nx, ny,
                    exclusionvalue, signaltonoiseratio, variancebackgroundfield, parameterfile):
    """Create a DIVA 2D parameter file given the main analysis parameters
    defined as floats or integers.
    """
    ParamString = ("# Correlation Length lc \n{0} \n"
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
                   "# varbak \n{12}").format(correlationlength, icoordchange, ispec, irtg,
                                             xmin, ymin, dx, dy, nx, ny,
                                             exclusionvalue, signaltonoiseratio, variancebackgroundfield, parameterfile)

    with open(parameterfile, 'w') as f:
        f.write(ParamString)
    logging.info("Written parameter file {0}".format(parameterfile))
