import numpy as np
import pydiva2d
import os
import unittest


class TestDivaData(unittest.TestCase):

    def setUp(self):
        # Create lists and arrays
        self.xlist = [1., 2., 10]
        self.ylist = [2., -1., 0.]
        self.datalist = [0., 10, 0]
        self.weightlist = [1., .2, 1.]
        self.xarray = np.array((6., 4., 2.1))
        self.yarray = np.array((1., 10., -1))
        self.yarray2 = np.array((1., 10., -1, 3.))
        self.datarray = np.array((7., 8., 9.))
        self.weightarray = np.array((1., 1., 1.))
        self.nogeojsonfile = "./nodata/data.js"
        self.geojsonfile = "./data/data.js"

    def test_init_data(self):
        Data0 = pydiva2d.Diva2DData()
        self.assertIsNone(Data0.x)
        self.assertIsNone(Data0.y)
        self.assertIsNone(Data0.field)
        self.assertIsNone(Data0.weight)

        Data1 = pydiva2d.Diva2DData(self.xlist, self.ylist, self.datalist)
        np.testing.assert_array_equal(Data1.x, self.xlist)
        np.testing.assert_array_equal(Data1.y, self.ylist)
        np.testing.assert_array_equal(Data1.field, self.datalist)
        np.testing.assert_array_equal(Data1.weight, np.ones_like(Data1.field))

        # Mix lists and arrays
        Data2 = pydiva2d.Diva2DData(self.xarray, self.yarray, self.datalist, self.weightlist)
        np.testing.assert_array_equal(Data2.x, self.xarray)
        np.testing.assert_array_equal(Data2.y, self.yarray)
        np.testing.assert_array_equal(Data2.field, self.datalist)
        np.testing.assert_array_equal(Data2.weight, self.weightlist)

        # Mix None's and lists
        Data3 = pydiva2d.Diva2DData(self.xarray, self.yarray)
        self.assertIsNone(Data3.x, self.xlist)
        self.assertIsNone(Data3.y)
        self.assertIsNone(Data3.field)
        self.assertIsNone(Data3.weight)

        # Dimension mismatch
        with self.assertRaises(Exception) as dim:
            Data4 = pydiva2d.Diva2DData(self.xarray, self.yarray2, self.datalist, self.weightlist)

    def test_write_nonexisting_geojson(self):
        """
        Check if geoJSON is properly created from data
        :param filename: path to the file to be created
        :type filename: str
        """
        data = pydiva2d.Diva2DData(self.xarray, self.yarray, self.datalist, self.weightlist)
        self.assertRaises(FileNotFoundError,
                          lambda: data.to_geojson(filename=self.nogeojsonfile))

    def test_write_geojson(self):
        """
        Check if geoJSON is properly created from data
        :param filename: path to the file to be created
        :type filename: str
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


if __name__ == '__main__':
    unittest.main()


