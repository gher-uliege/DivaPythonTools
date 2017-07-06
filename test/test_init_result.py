import numpy as np
import pydiva2d
import importlib
import unittest
importlib.reload(pydiva2d)


class TestResultMethods(unittest.TestCase):
    
    def setUp(self):
        self.xx = np.array((1, 2, 3))
        self.yy = np.array((0, 1))
        self.zz = np.random.rand(3, 2)
        self.Results = pydiva2d.Diva2DResults(self.xx, self.yy, self.zz)
        self.divadir = "/home/ctroupin/Software/DIVA/DIVA-diva-4.7.1"
        self.datafile = "../data/MLD1.dat"
        self.coastfile = "../data/coast.cont"
        self.paramfile = "../data/param.par"
        
    def test_init(self):
        np.testing.assert_array_equal(self.Results.x, self.xx)
        np.testing.assert_array_equal(self.Results.y, self.yy)
        np.testing.assert_array_equal(self.Results.analysis, self.zz)
        #self.assertIsNone(self.Results.error)

    def test_make(self):
        results = pydiva2d.Diva2DResults()\
        make(self.divadir, datafile=self.datafile,
                     paramfile=self.paramfile,
                     contourfile=self.coastfile)

        self.assertEqual(results.x[10], 28.)
        self.assertEqual(results.y[20], 42.)
        self.assertEqual(results.analysis.data.mean() == -70.082535)
        self.assertEqual(results.analysis.data.max() == -3.5384512)
        self.assertEqual(results.analysis.data.min() == -99.)


if __name__ == '__main__':
    unittest.main()



