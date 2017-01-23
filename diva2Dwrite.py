
import os
import logging


def make_diva_directorynames(divadir):
    """Create directory names based on the Diva main directory.
    :param diva4Ddir: Diva4D main directory
    :type diva4Ddir: str
    :return divabindir: Diva binary directory
    :return divasrcdir: Diva source directory
    :return diva2Ddir: Main 2D directory (divastripped)
    :return diva4Ddir: Main 4D directory (Climatology)
    :return diva4Dinputdir: input directory for the 4D
    """
    if os.path.isdir(divadir):
        logging.debug("{0} exists".format(divadir))
        divabindir = os.path.join(divadir, 'DIVA3D/bin') 
        divasrcdir = os.path.join(divadir, 'DIVA3D/src/Fortan')
        diva2Ddir = os.path.join(divadir, 'DIVA3D/divastripped')
        diva4Ddir = os.path.join(divadir, 'JRA4/Climatology')
        diva4Dinputdir = os.path.join(divadir, 'JRA4/Climatology/input')
        return divabindir, divasrcdir, diva2Ddir, diva4Ddir, diva4Dinputdir
    else:
        logging.error("%{0} is not a directory or doesn't exist".format(divadir))
        return '', '', '', ''


def make_diva2D_filenames(diva2Ddir):
    """Generate the input file names and location based on the diva2D main directory."""
    ContourFile = os.path.join(diva2Ddir, 'input/coast.cont')
    ParameterFile = os.path.join(diva2Ddir, 'input/param.par')
    DataFile = os.path.join(diva2Ddir, 'input/data.dat')
    ValatxyFile = os.path.join(diva2Ddir, 'input/valatxy.coord')
    return ContourFile, DataFile, ParameterFile, ValatxyFile


def write_contour(contours, ContourFile):
    """Write the contours (list of list of tuples)
    into the specified contour file.
    """
    ncontours = len(contours)
    with open(ContourFile, 'w') as f:
        f.write(str(ncontours) + '\n')
        for n, contour in enumerate(contours):
            npoints = len(contour)
            logging.debug("Sub-contour no. {0} has {1} points".format(n, npoints))
            f.write(str(npoints) + '\n')
            for points in contour:
                line = ' '.join(str(x) for x in points)
                f.write(line + '\n')
    logging.info("Writen contour file {0} \ncontaining {1} contours".format(ContourFile, ncontours))
        

def write_data(data, DataFile):
    """Write the data points (list of tuples, each tuple with 3 or 4 values)
    into the specified data file.
    """
    ndata = len(data)
    with open(DataFile, 'w') as f:
        for datapoints in data:
            line = ' '.join(str(x) for x in datapoints)
            f.write(line + '\n')
    logging.info("Written data file {0} \ncontaining {1} data points".format(DataFile, ndata))


def write_parameter(CorrelationLength, iCoordChange, iSpec, iReg,
                    xmin, ymin, dx, dy, nx, ny,
                    ExclusionValue, SignalToNoiseRatio, VarianceBackgroundField, ParameterFile):
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
            "# varbak \n{12}".format(CorrelationLength, iCoordChange, iSpec, iReg,
                                     xmin, ymin, dx, dy, nx, ny,
                                     ExclusionValue, SignalToNoiseRatio, VarianceBackgroundField)
           )
    with open(ParameterFile, 'w') as f:
        f.write(ParamString)
    logging.info("Written parameter file {0}".format(ParameterFile))

