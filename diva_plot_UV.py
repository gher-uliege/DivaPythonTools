# diva_plot_UV.py
# 
# plot advection velocity field
#
from GHERFormat import GHERFile

datafile = 'fieldgher.anl'
data2 = GHERFile(datafile).load()
