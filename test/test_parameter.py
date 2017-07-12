import numpy as np
import pydiva2d
import unittest


class TestParamMethods(unittest.TestCase):

    def setUp(self):
        self.cl = 1.244
        self.icoordchange = 0
        self.ispec = -11
        self.ireg = 2
        self.xori = -10.1
        self.yori = .0001
        self.dx = 0.25
        self.dy = 0.333
        self.nx = 401
        self.ny = 151
        self.valex = -999.
        self.snr = .5
        self.varbak = 1.0
        self.divadir = "/home/ctroupin/Software/DIVA/DIVA-diva-4.7.1/"
        self.paramfile = "../data/param.par"
        self.noparamfile = "./data/noparam.par"

    def test_init(self):
        """Instantiate Parameter object with pre-set values
        """
        parameters = pydiva2d.Diva2DParameters(self.cl, self.icoordchange, self.ispec,
                                               self.ireg, self.xori, self.yori, self.dx,
                                               self.dy, self.nx, self.ny, self.valex,
                                               self.snr, self.varbak)
        self.assertEqual(parameters.cl, self.cl)
        self.assertEqual(parameters.icoordchange, self.icoordchange)
        self.assertEqual(parameters.ispec, self.ispec)
        self.assertEqual(parameters.xend, 89.9)
        self.assertEqual(parameters.yend, 49.950100000000006)

    def test_read_file(self):
        """Instantiate Parameter object by reading existing file
        """
        parameters = pydiva2d.Diva2DParameters().read_from(self.paramfile)
        self.assertEqual(parameters.cl, 1)
        self.assertEqual(parameters.icoordchange, 2)
        self.assertEqual(parameters.ispec, 0)
        self.assertEqual(parameters.ireg, 2)
        self.assertEqual(parameters.xori, 27)
        self.assertEqual(parameters.yori, 40)
        self.assertEqual(parameters.dx, 0.1)
        self.assertEqual(parameters.dy, 0.1)
        self.assertEqual(parameters.nx, 151)
        self.assertEqual(parameters.ny, 76)
        self.assertEqual(parameters.valex, -99)
        self.assertEqual(parameters.snr, 1.0)
        self.assertEqual(parameters.varbak, 0)
        self.assertEqual(parameters.xend, 42.0)
        self.assertEqual(parameters.yend, 47.5)

    def test_read_nonexisting_file(self):
        """
        Try instantiate Parameter object reading an non-existing file
        """
        self.assertRaises(FileNotFoundError,
                          lambda: pydiva2d.Diva2DParameters().read_from(self.noparamfile))


if __name__ == '__main__':
    unittest.main()



