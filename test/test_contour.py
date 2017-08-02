import numpy as np
import pydiva2d
import unittest
import os

print("Running tests on Diva contours")
print(" ")


class TestContourMethods(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.xlist = [[0.7173, 10.9596, 0.71213338], [3.424071, 23.9648, 23.8063, 3.4999]]
        cls.ylist = [[-1.7529, -1.257, 5.00245219], [1.6594, 1.945, 3.7673, 4.36759776]]
        cls.xx = np.array(((0.1, 4., 4, 1), (6.3, 9.3, 8.8, 7.4)))
        cls.yy = np.array(((0.3, 1., 3.4, 1.8), (-1., -1.4, 2.2, 3.3)))
        cls.coastfile = "../data/coast.cont"
        cls.outputfile = "./datawrite/coast.cont"
        cls.nocoastfile = "../data/nocoast.cont"
        cls.nogeojsonfile = "./nodata/contours.js"
        cls.geojsonfile = "./datawrite/contours.js"

    def test_init(self):
        """
        Instantiate Contour object with pre-set values
        """
        contour = pydiva2d.Diva2DContours(self.xx, self.yy)
        np.testing.assert_array_equal(contour.x, self.xx)
        np.testing.assert_array_equal(contour.y, self.yy)
        self.assertEqual(contour.get_contours_number, 2)

    def test_init_list(self):
        """
        Instantiate Contour object with a list of lists
        """
        contour = pydiva2d.Diva2DContours(self.xlist, self.ylist)
        np.testing.assert_array_equal(contour.x, self.xlist)
        np.testing.assert_array_equal(contour.y, self.ylist)
        self.assertEqual(contour.get_contours_number, 2)

    def test_read_file(self):
        """
        Instantiate Contour object reading an existing file
        """
        contour = pydiva2d.Diva2DContours().read_from(self.coastfile)
        self.assertEqual(contour.get_contours_number, 28)
        self.assertEqual(len(contour.x), 28)
        self.assertEqual(len(contour.y), 28)
        self.assertEqual(len(contour.x[0]), 576)
        self.assertEqual(len(contour.y[1]), 16)
        self.assertEqual(len(contour.x[-1]), 6)

    def test_read_file_numpy(self):
        """
        Instantiate Contour object reading an existing file
        using numpy module
        """
        contour = pydiva2d.Diva2DContours().read_from_np(self.coastfile)
        self.assertEqual(contour.get_contours_number, 28)
        self.assertEqual(len(contour.x), 28)
        self.assertEqual(len(contour.y), 28)
        self.assertEqual(len(contour.x[0]), 576)
        self.assertEqual(len(contour.y[1]), 16)
        self.assertEqual(len(contour.x[-1]), 6)

    def test_read_nonexisting_file(self):
        """
        Try instantiate Contour object reading an non-existing file
        """
        self.assertRaises(FileNotFoundError,
                          lambda: pydiva2d.Diva2DContours().read_from(self.nocoastfile))

    def test_write_file(self):
        """
        Write a contour to a file
        """
        contour = pydiva2d.Diva2DContours(self.xx, self.yy)
        contour.write_to(self.outputfile)

        self.assertTrue(os.path.exists(self.outputfile))
        with open(self.outputfile) as f:
            lines = f.readlines()
            lastline = lines[-1].rstrip()
            self.assertEqual(int(lines[0].rstrip()), 2)
            self.assertEqual(int(lines[1].rstrip()), 4)
            self.assertEqual(float(lastline.split()[0]), 7.4)
            self.assertEqual(len(lines), 11)

    def test_write_nonexisting_geojson(self):
        """
        Check if geoJSON is properly created from contours
        """
        contour = pydiva2d.Diva2DContours(self.xlist, self.ylist)
        self.assertRaises(FileNotFoundError,
                          lambda: contour.to_geojson(filename=self.nogeojsonfile))

    def test_write_geojson(self):
        """
        Check if geoJSON is properly created from contours
        """
        contour = pydiva2d.Diva2DContours(self.xlist, self.ylist)
        contour.to_geojson(filename=self.geojsonfile)

        self.assertTrue(os.path.exists(self.geojsonfile))

        with open(self.geojsonfile) as f:
            lines = f.readlines()
            line0 = lines[0].rstrip()

        self.assertEqual(line0, "var contours = {")
        self.assertEqual(len(lines), 41)

        contour.to_geojson(filename=self.geojsonfile, varname="divacont")
        self.assertTrue(os.path.exists(self.geojsonfile))

        with open(self.geojsonfile) as f:
            lines = f.readlines()
            line0 = lines[0].rstrip()

        self.assertEqual(line0, "var divacont = {")
        self.assertEqual(len(lines), 41)

    @classmethod
    def tearDownClass(cls):
        print("Tearing down...")

        cls.geojsonfile = "./datawrite/contours.js"
        cls.outputfile = "./datawrite/coast.cont"

        os.remove(cls.outputfile)
        os.remove(cls.geojsonfile)

if __name__ == '__main__':
    unittest.main()
