import numpy as np
import pydiva2d
import importlib
import unittest

importlib.reload(pydiva2d)


class TestDivaContour(unittest.TestCase):

    def setUp(self):
        # Create lists and arrays
        self.xc = [0, 2., 2., 1.]
        self.yc = [-1., -1., 2., 2.]
        self.xcarray = np.array((0., 5., 5., 0.))
        self.ycarray = np.array((0., 5., 5., 0.))

    def test_init(self):
        Contour0 = pydiva2d.Diva2DContours()
        self.assertIsNone(Contour0.x)
        self.assertIsNone(Contour0.y)

        Contour1 = pydiva2d.Diva2DContours(self.xc, self.yc)
        np.testing.assert_array_equal(Contour1.x, self.xc)
        np.testing.assert_array_equal(Contour1.y, self.yc)

        Contour2 = pydiva2d.Diva2DContours(self.xcarray, self.ycarray)
        np.testing.assert_array_equal(Contour2.x, self.xcarray)
        np.testing.assert_array_equal(Contour2.y, self.ycarray)


if __name__ == '__main__':
    unittest.main()


