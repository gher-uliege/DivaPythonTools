## Configuration

Make sure the directory containing pydiva2d.py and pydiva4d.py is present in the environment variable PYTHONPATH.

```bash
export PYTHONPATH=Path_to_pydiva2d:$PYTHONPATH
```
where *Path_to_pydiva2d* depends on the location of the package on your machine.

You can also add the previous line to your `.bashrc` file if working with unix system.

## Content

* [run_diva2D_rectangles](./run_diva2D_rectangles.ipynb): synthetic example with rectangular sub-domains.
* [run_diva2D_MLD](./run_diva2D_MLD.ipynb): realistic example using mixed-layer depth data in the Black Sea. 

* [plot_diva4D_results](./plot_diva4D_results.ipynb): plot the results of a Diva4D execution.
* [plot_diva4D_results_basemap](./plot_diva4D_results_basemap.ipynb): same as previous but using [Basemap](http://matplotlib.org/basemap/) module.

* [run_diva2D_bash](./run_diva2D_bash.ipynb): a example of Notebook in bash.
