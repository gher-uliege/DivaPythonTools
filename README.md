# Diva Python Tools

A set of modules to 
1. prepare the Diva input files
2. run the Diva interpolation tool
3. read the output files (analysis, finite-element mesh)
4. plot input and output.

## Modules

The main modules are [pydiva2d](./pydiva2d.py) and [pydiva4d](./pydiva4D.py), which defines the classes for the 2D and 4D version of Diva, respectively.

### Pydiva2d

The module defines classes corresponding to the main Diva input (data, parameters, contours) and output files (analysed and error fields, finite-element mesh).

## Plots

The figures can be generated with and without the [Basemap](https://github.com/matplotlib/basemap) module (Plot on map projections). 

Some examples obtained with mixed-layer depth (MLD) data are shown below. The complete example to generate these plots is inside the Notebooks directory [(run_diva2D_MLD)](./Notebooks/run_diva2D_MLD.ipynb).

The [Notebooks](./Notebooks) directory contains additional examples showing how to run 2D and 4D cases.

### Data values
Scatter plot showing the data positions and values.
![Data](./figures/datapoints.png)

### Contours
By default, each sub-contour is displayed in a different color.
![Contour](./figures/contours.png)

### Finite-element mesh
Triangular mesh covering the region of interest.
![Mesh](./figures/mesh.png)

### Analysed fields
Pseudo-color plot of the gridded field obtained by the interpolation.
![Analysis](./figures/analysis.png)

### Combined information
Data, contours, mesh and analysis on the same figure.
![Combined](./figures/AnalysisMeshData.png)



