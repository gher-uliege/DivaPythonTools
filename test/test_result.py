import numpy as np
import pydiva2d
import unittest


class TestResultMethods(unittest.TestCase):
    
    def setUp(self):
        self.xx = np.array((1, 2, 3))
        self.yy = np.array((0, 1))
        self.zz = np.random.rand(3, 2)
        self.ee = np.random.rand(3, 2)
        self.eebad = np.random.rand(2, 3)
        self.divadir = "/home/ctroupin/Software/DIVA/DIVA-diva-4.7.1/"
        self.datafile = "../data/MLD1.dat"
        self.coastfile = "../data/coast.cont"
        self.paramfile = "../data/param.par"
        
    def test_init(self):
        ResultsSimple = pydiva2d.Diva2DResults(self.xx, self.yy, self.zz, self.ee)
        np.testing.assert_array_equal(ResultsSimple.x, self.xx)
        np.testing.assert_array_equal(ResultsSimple.y, self.yy)
        np.testing.assert_array_equal(ResultsSimple.analysis, self.zz)
        np.testing.assert_array_equal(ResultsSimple.error, self.ee)
        #self.assertIsNone(self.Results.error)

    def test_init_empty(self):
        ResultEmpty = pydiva2d.Diva2DResults()
        self.assertEqual(ResultEmpty.x, None)
        self.assertEqual(ResultEmpty.y, None)
        self.assertEqual(ResultEmpty.analysis, None)
        self.assertEqual(ResultEmpty.error, None)

    def test_init_dim_mismatch(self):
        ResultMismatch = pydiva2d.Diva2DResults(self.xx, self.yy, self.zz, self.eebad)
        # Check that exception is there

    def test_read_nonexisting_file(self):
        """Check that the object did not read from file
        """
        ResultsNoFile = pydiva2d.Diva2DResults()
        ResultsNoFile.read_from('./nofile.nc')
        self.assertTrue('ResultsNoFile' in locals())
        self.assertFalse('ResultsNoFile.x' in locals())
        self.assertFalse('ResultsNoFile.y' in locals())
        self.assertFalse('ResultsNoFile.analysis' in locals())

    def test_make(self):
        """
        Check the results of the divacalc execution with selected files
        """
        pydiva2d.Diva2DMesh().make(self.divadir, self.coastfile, self.paramfile)
        results = pydiva2d.Diva2DResults()
        results.make(self.divadir, datafile=self.datafile,
                     paramfile=self.paramfile,
                     contourfile=self.coastfile)

        self.assertEqual(results.x[10], 28.)
        self.assertEqual(results.y[20], 42.)
        print('{0:.16f}'.format(results.analysis.data.max()))
        print('__________')
        self.assertAlmostEqual(results.analysis.data.mean(), -70.0825347900)
        self.assertAlmostEqual(results.analysis.data.max(), -3.5384511948)
        self.assertAlmostEqual(results.analysis.data.min(), -99.)


if __name__ == '__main__':
    unittest.main()



