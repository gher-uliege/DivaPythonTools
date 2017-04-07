# Diva Python Tools

A set of modules to prepare the Diva input files and plot the data, contours, finite-element mesh and analysis field.

## Plots

The figures can be generated with and without the [Basemap](https://github.com/matplotlib/basemap) module (Plot on map projections). Some examples obtained with mixed-layer depth (MLD) data are shown below.

The complete example to generate these plots is inside the Notebooks directory.

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



