# Diva_python_tools

The Python tools for the [DIVA](http://modb.oce.ulg.ac.be/mediawiki/index.php/DIVA) interpolation sofware aim at providing modules to make easier the reading and plotting of input/output files. The jupyter notebook [example_2Dplot.ipynb](./example_2Dplot.ipynb) explains how to use the functions.

## Loading

The loading functions are available in the [diva2Dread](./diva2Dread.py) module. These functions allow the user to load the main input files:
* contours,
* parameters,
* data.

## Plotting

The plotting functions are available in the [diva2Dplot](./diva2Dplot.py) module. They allow the user to represent:
* the finite-element mesh,
* the analysed and error fields.

The example below show the Mixed-Layer Depth in the Black Sea for the month of January.

![blackseamld](https://cloud.githubusercontent.com/assets/11868914/22156085/0442b0f0-df32-11e6-8ab8-09cc8b207db8.png)

# References

## DIVA sofware

Troupin, C.; Sirjacobs, D.; Rixen, M.; Brasseur, P.; Brankart, J.-M.; Barth, A.; Alvera-Azcárate, A.; Capet, A.; Ouberdous, M.; Lenartz, F.; Toussaint, M.-E. & Beckers, J.-M. Generation of analysis and consistent error fields using the Data Interpolating Variational Analysis (Diva) Ocean Modelling, 2012, 52-53, 90-101. doi:[10.1016/j.ocemod.2012.05.002](https://doi.org/10.1016/j.ocemod.2012.05.002)

## Black Sea data

Capet, A.; Troupin, C.; Carstensen, J.; Grégoire, M. & Beckers, J.-M. Untangling spatial and temporal trends in the variability of the Black Sea Cold Intermediate Layer and mixed Layer Depth using the DIVA detrending procedure Ocean Dynamics, 2014, 64, 315-324. doi:[10.1007/s10236-013-0683-4](https://doi.org/10.1007/s10236-013-0683-4)
