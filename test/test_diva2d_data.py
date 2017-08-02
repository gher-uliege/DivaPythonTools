import numpy as np
import pydiva2d
import os
import unittest


class TestDivaData(unittest.TestCase):

    @classmethod
    def setUp(cls):
        # Create lists and arrays
        cls.xlist = [1., 2., 10]
        cls.ylist = [2., -1., 0.]
        cls.datalist = [0., 10, 0]
        cls.weightlist = [1., .2, 1.]
        cls.xarray = np.array((6., 4., 2.1))
        cls.yarray = np.array((1., 10., -1))
        cls.yarray2 = np.array((1., 10., -1, 3.))
        cls.datarray = np.array((7., 8., 9.))
        cls.weightarray = np.array((1., 1., 1.))
        cls.nogeojsonfile = "./nodata/data.js"
        cls.outputfile = "./datawrite/data.dat"
        cls.geojsonfile = "./datawrite/data.js"

    def test_init_data(self):
        data0 = pydiva2d.Diva2DData()
        self.assertIsNone(data0.x)
        self.assertIsNone(data0.y)
        self.assertIsNone(data0.field)
        self.assertIsNone(data0.weight)

        data1 = pydiva2d.Diva2DData(self.xlist, self.ylist, self.datalist)
        np.testing.assert_array_equal(data1.x, self.xlist)
        np.testing.assert_array_equal(data1.y, self.ylist)
        np.testing.assert_array_equal(data1.field, self.datalist)
        np.testing.assert_array_equal(data1.weight, np.ones_like(data1.field))

        # Mix lists and arrays
        data2 = pydiva2d.Diva2DData(self.xarray, self.yarray, self.datalist, self.weightlist)
        np.testing.assert_array_equal(data2.x, self.xarray)
        np.testing.assert_array_equal(data2.y, self.yarray)
        np.testing.assert_array_equal(data2.field, self.datalist)
        np.testing.assert_array_equal(data2.weight, self.weightlist)

        # Mix None's and lists
        data3 = pydiva2d.Diva2DData(self.xarray, self.yarray)
        self.assertIsNone(data3.x, self.xlist)
        self.assertIsNone(data3.y)
        self.assertIsNone(data3.field)
        self.assertIsNone(data3.weight)

        # Dimension mismatch
        with self.assertRaises(Exception) as dim:
            pydiva2d.Diva2DData(self.xarray, self.yarray2, self.datalist, self.weightlist)

    def test_write_file(self):
        """
        Write data points to a file
        """
        data = pydiva2d.Diva2DData(self.xarray, self.yarray, self.datalist, self.weightlist)
        data.write_to(self.outputfile)

        self.assertTrue(os.path.exists(self.outputfile))
        with open(self.outputfile) as f:
            lines = f.readlines()
            lastline = lines[-1].rstrip()
            secondline = lines[1].rstrip()

            self.assertEqual(float(secondline.split()[2]), 10.0)
            self.assertEqual(float(lastline.split()[0]), 2.1)
            self.assertEqual(len(lines), 3)

    def test_write_nonexisting_geojson(self):
        """
        Check if geoJSON is properly created from data
        """
        data = pydiva2d.Diva2DData(self.xarray, self.yarray, self.datalist, self.weightlist)
        self.assertRaises(FileNotFoundError,
                          lambda: data.to_geojson(filename=self.nogeojsonfile))

    def test_write_geojson(self):
        """
        Check if geoJSON is properly created from data
        """
        data = pydiva2d.Diva2DData(self.xarray, self.yarray, self.datalist, self.weightlist)
        data.to_geojson(filename=self.geojsonfile)

        self.assertTrue(os.path.exists(self.geojsonfile))

        with open(self.geojsonfile) as f:
            lines = f.readlines()
            line0 = lines[0].rstrip()

        self.assertEqual(line0, "var data = {")
        self.assertEqual(len(lines), 47)

        data.to_geojson(filename=self.geojsonfile, varname='divadata')

        with open(self.geojsonfile) as f:
            lines = f.readlines()
            line0 = lines[0].rstrip()

        self.assertEqual(line0, "var divadata = {")
        self.assertEqual(len(lines), 47)

    @classmethod
    def tearDownClass(cls):
        print("Tearing down...")

        cls.geojsonfile = "./datawrite/data.js"
        cls.outputfile = "./datawrite/data.dat"

        # os.remove(cls.outputfile)
        os.remove(cls.geojsonfile)


if __name__ == '__main__':
    unittest.main()
