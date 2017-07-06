import numpy as np
import pydiva2d
import unittest

class TestDivaKernel(unittest.TestCase):

    def setUp(self):
        # Create contour
        xc = [0, 10, 10, 0]
        yc = [0, 0, 10, 10]
        contour = pydiva2d(xc, yc)
        # Create parameter file

        # Create datafile

        # Generate mesh

        # Perform analysis

    def test_init(self):
        np.testing.assert_array_equal(self.Results.x, self.xx)
        np.testing.assert_array_equal(self.Results.y, self.yy)
        np.testing.assert_array_equal(self.Results.analysis, self.zz)
        # self.assertIsNone(self.Results.error)


if __name__ == '__main__':
    unittest.main()


