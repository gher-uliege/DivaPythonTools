import numpy as np
import pydiva2d
import unittest


class TestContourMethods(unittest.TestCase):

    def setUp(self):
        self.xlist = [[0.7173, 10.9596, 0.71213338], [3.424071, 23.9648, 23.8063, 3.4999]]
        self.ylist = [[-1.7529, -1.257, 5.00245219], [1.6594, 1.945, 3.7673, 4.36759776]]
        self.xx = np.array(((0.1, 4., 4, 1), (6.3, 9.3, 8.8, 7.4)))
        self.yy = np.array(((0.3, 1., 3.4, 1.8), (-1., -1.4, 2.2, 3.3)))
        self.coastfile = "../data/coast.cont"
        self.nocoastfile = "../data/nocoast.cont"

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

    def test_create_geojson(self, filename):
        """
        Check if geoJSON is properly created from contours
        :param filename: path to the file to be created
        :type filename: str
        """

    def

if __name__ == '__main__':
    unittest.main()
