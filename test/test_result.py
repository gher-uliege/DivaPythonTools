import os
import numpy as np
import pydiva2d
import subprocess
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
        self.noresultfile = "./data/noresult.nc"
        self.outputfile = "./data/testresult.nc"
        self.nogeojsonfile = "./nodata/results.js"
        self.geojsonfile = "./data/results.js"
        
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
        """
        Instantiate object with arrays of different length
        """
        self.assertRaises(Exception,
                          lambda: pydiva2d.Diva2DResults(self.xx, self.yy, self.zz, self.eebad))

        self.assertRaises(Exception,
                          lambda: pydiva2d.Diva2DResults(self.xx, self.xx, self.zz, self.eebad))

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
        results = pydiva2d.Diva2DResults().read_from(self.resultfile)
        self.assertEqual(len(results.x), 101)
        self.assertEqual(len(results.y), 101)
        self.assertEqual(results.x[5], -9.)
        self.assertEqual(results.y[-1], 10.)
        self.assertEqual(results.analysis.mean(), 0.015413076363357843)
        self.assertEqual(results.error.mean(), 0.9919163602941177)
        self.assertEqual(results.error.min(), 0.7073806524276733)
        self.assertEqual(results.analysis.shape, (101, 101))

    def test_read_nonexisting_file(self):
        """
        Try instantiate Contour object reading an non-existing file
        """
        self.assertRaises(FileNotFoundError,
                          lambda: pydiva2d.Diva2DResults().read_from(self.noresultfile))

    def test_make(self):
        """
        Check the results of the divacalc execution with selected files
        """

        # Create mesh prior to analysis
        pydiva2d.Diva2DMesh().make(self.divadir, self.coastfile, self.paramfile)

        results = pydiva2d.Diva2DResults().make(self.divadir, datafile=self.datafile,
                                                paramfile=self.paramfile,
                                                contourfile=self.coastfile,
                                                outputfile=self.outputfile)

        self.assertTrue(os.path.exists(self.outputfile))
        self.assertEqual(results.x[10], 28.)
        self.assertEqual(results.y[20], 42.)
        self.assertAlmostEqual(results.analysis.data.mean(), -70.0825347900)
        self.assertAlmostEqual(results.analysis.data.max(), -3.5384511948)
        self.assertEqual(results.analysis.data.min(), -99.)

    def test_write_nonexisting_geojson(self):
        """
        Check if geoJSON is properly created from contours
        :param filename: path to the file to be created
        :type filename: str
        """
        results = pydiva2d.Diva2DResults().read_from(self.resultfile)
        self.assertRaises(FileNotFoundError,
                          lambda: results.to_geojson(filename=self.nogeojsonfile))

    def test_write_geojson(self):
        """
        Check if geoJSON is properly created from contours
        :param filename: path to the file to be created
        :type filename: str
        """
        results = pydiva2d.Diva2DResults().read_from(self.resultfile)
        results.to_geojson(filename=self.geojsonfile)

        self.assertTrue(os.path.exists(self.geojsonfile))

        with open(self.geojsonfile) as f:
            lines = f.readlines()
            line0 = lines[0].rstrip()

        self.assertEqual(line0, "var results = {")
        self.assertEqual(len(lines), 2058)

        results.to_geojson(filename=self.geojsonfile, varname="divaresults")
        self.assertTrue(os.path.exists(self.geojsonfile))

        with open(self.geojsonfile) as f:
            lines = f.readlines()
            line0 = lines[0].rstrip()

        self.assertEqual(line0, "var divaresults = {")
        self.assertEqual(len(lines), 2058)

        results.to_geojson(filename=self.geojsonfile, levels=np.linspace(0, 0.5, 10))
        self.assertTrue(os.path.exists(self.geojsonfile))

        with open(self.geojsonfile) as f:
            lines = f.readlines()
            line0 = lines[0].rstrip()

        self.assertEqual(line0, "var results = {")
        self.assertEqual(len(lines), 2048)

    def tearDown(self):
        if os.path.exists(self.outputfile):
            os.remove(self.outputfile)

        # Clean Diva intermediate directories
        subprocess.Popen("./divaclean", cwd=os.path.join(self.divadir, "DIVA3D/divastripped"),
                         stdout=subprocess.PIPE, shell=True)


if __name__ == '__main__':
    unittest.main()



