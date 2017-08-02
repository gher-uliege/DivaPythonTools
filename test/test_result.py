import os
import numpy as np
import pydiva2d
import subprocess
import unittest

print("Running tests on Diva results")
print(" ")


class TestResultMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.xx = np.array((1, 2, 3))
        cls.yy = np.array((0, 1))
        cls.zz = np.random.rand(3, 2)
        cls.ee = np.random.rand(3, 2)
        cls.eebad = np.random.rand(2, 3)
        cls.divadir = "/home/ctroupin/Software/DIVA/DIVA-diva-4.7.1/"
        cls.datafile = "../data/MLD1.dat"
        cls.coastfile = "../data/coast.cont"
        cls.paramfile = "../data/param.par"
        cls.resultfile = "./dataread/resultsquare.nc"
        cls.noresultfile = "./dataread/noresult.nc"
        cls.outputfile = "./datawrite/testresult.nc"
        cls.nogeojsonfile = "./nodata/results.js"
        cls.geojsonfile = "./datawrite/results.js"

        if not os.path.exists("./datawrite/"):
            os.makedirs("./datawrite/")

    def test_init(self):
        """
        Instantiate Result object with pre-set values
        """
        results_simple = pydiva2d.Diva2DResults(self.xx, self.yy, self.zz, self.ee)
        np.testing.assert_array_equal(results_simple.x, self.xx)
        np.testing.assert_array_equal(results_simple.y, self.yy)
        np.testing.assert_array_equal(results_simple.analysis, self.zz)
        np.testing.assert_array_equal(results_simple.error, self.ee)
        # self.assertIsNone(self.Results.error)

    def test_init_empty(self):
        """
        Instantiate empty Result object
        """
        result_empty = pydiva2d.Diva2DResults()
        self.assertEqual(result_empty.x, None)
        self.assertEqual(result_empty.y, None)
        self.assertEqual(result_empty.analysis, None)
        self.assertEqual(result_empty.error, None)

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
        self.assertRaises(FileNotFoundError,
                          lambda: pydiva2d.Diva2DResults().read_from(self.noresultfile))

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
        Check if error is raised when trying to write in a non-existing directory
        """
        results = pydiva2d.Diva2DResults().read_from(self.resultfile)
        self.assertRaises(FileNotFoundError,
                          lambda: results.to_geojson(filename=self.nogeojsonfile))

    def test_write_geojson(self):
        """
        Check if geoJSON is properly created from results
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

    @classmethod
    def tearDownClass(cls):
        print("Tearing down...")

        cls.divadir = "/home/ctroupin/Software/DIVA/DIVA-diva-4.7.1/"
        cls.outputfile = "./datawrite/testresult.nc"
        cls.geojsonfile = "./datawrite/results.js"

        # Clean Diva intermediate directories and files
        subprocess.run("./divaclean", cwd=os.path.join(cls.divadir, "DIVA3D/divastripped"),
                         stdout=subprocess.PIPE, shell=True)

        os.remove(cls.outputfile)
        os.remove(cls.geojsonfile)


if __name__ == '__main__':
    unittest.main()
