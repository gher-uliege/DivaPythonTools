import pydiva2d
import unittest
import os


class TestParamMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.cl = 1.244
        cls.icoordchange = 0
        cls.ispec = -11
        cls.ireg = 2
        cls.xori = -10.1
        cls.yori = .0001
        cls.dx = 0.25
        cls.dy = 0.333
        cls.nx = 401
        cls.ny = 151
        cls.valex = -999.
        cls.snr = .5
        cls.varbak = 1.0
        cls.divadir = "/home/ctroupin/Software/DIVA/DIVA-diva-4.7.1/"
        cls.paramfile = "../data/param.par"
        cls.noparamfile = "./data/noparam.par"
        cls.outputfile = "./datawrite/param.par"

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
        
    def test_write_file(self):

        parameters = pydiva2d.Diva2DParameters(self.cl, self.icoordchange, self.ispec,
                                               self.ireg, self.xori, self.yori, self.dx,
                                               self.dy, self.nx, self.ny, self.valex,
                                               self.snr, self.varbak)

        parameters.write_to(self.outputfile)

        self.assertTrue(os.path.exists(self.outputfile))

        with open(self.outputfile) as f:
            lines = f.readlines()
            line0 = lines[0].rstrip()
            line5 = lines[5].rstrip()
        self.assertEqual(len(lines), 26)
        self.assertEqual(line0, "# Correlation Length lc")
        self.assertEqual(int(line5), -11)

    @classmethod
    def tearDownClass(cls):
        print("Tearing down...")

        cls.outputfile = "./datawrite/param.par"
        os.remove(cls.outputfile)

if __name__ == '__main__':
    unittest.main()
