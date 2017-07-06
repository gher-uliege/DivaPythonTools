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
        self.resultfile = "./data/resultsquare.nc"
        
    def test_init(self):
        """
        Instantiate Result object with pre-set values
        """
        ResultsSimple = pydiva2d.Diva2DResults(self.xx, self.yy, self.zz, self.ee)
        np.testing.assert_array_equal(ResultsSimple.x, self.xx)
        np.testing.assert_array_equal(ResultsSimple.y, self.yy)
        np.testing.assert_array_equal(ResultsSimple.analysis, self.zz)
        np.testing.assert_array_equal(ResultsSimple.error, self.ee)
        #self.assertIsNone(self.Results.error)

    def test_init_empty(self):
        """
        Instantiate empty Result object
        """
        ResultEmpty = pydiva2d.Diva2DResults()
        self.assertEqual(ResultEmpty.x, None)
        self.assertEqual(ResultEmpty.y, None)
        self.assertEqual(ResultEmpty.analysis, None)
        self.assertEqual(ResultEmpty.error, None)

    def test_init_dim_mismatch(self):
        ResultMismatch = pydiva2d.Diva2DResults(self.xx, self.yy, self.zz, self.eebad)
        # Check that exception is properly handled

    def test_read_nonexisting_file(self):
        """
        Check that the object did not read from file
        """
        results_noFile = pydiva2d.Diva2DResults()
        results_noFile.read_from('./nofile.nc')
        self.assertTrue('results_noFile' in locals())
        self.assertFalse('results_noFile.x' in locals())
        self.assertFalse('results_noFile.y' in locals())
        self.assertFalse('results_noFile.analysis' in locals())

    def test_read_existing_file(self):
        """
        Check if properly reads values from existing file
        """
        results_file = pydiva2d.Diva2DResults()
        results_file.read_from(self.resultfile)
        self.assertEqual(len(results_file.x), 101)
        self.assertEqual(len(results_file.y), 101)
        self.assertEqual(results_file.analysis.shape, (101, 101))
        self.assertEqual(results_file.x[5], -9.)
        self.assertEqual(results_file.y[-1], 10.)
        self.assertEqual(results_file.analysis.mean(), 0.015413076363357843)
        self.assertEqual(results_file.error.mean(), 0.9919163602941177)
        self.assertEqual(results_file.error.min(), 0.7073806524276733)

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
        self.assertAlmostEqual(results.analysis.data.mean(), -70.0825347900)
        self.assertAlmostEqual(results.analysis.data.max(), -3.5384511948)
        self.assertEqual(results.analysis.data.min(), -99.)

if __name__ == '__main__':
    unittest.main()



