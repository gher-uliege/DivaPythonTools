import pydiva2d
import numpy as np

x = np.array((0., 1., 2.))
y = np.array((1., 0., 1.))
field = np.array((2., 4., 0.))

Diva2DData = pydiva2d.Diva2DData(x, y, field)