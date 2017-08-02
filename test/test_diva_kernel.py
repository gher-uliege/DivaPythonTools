import pydiva2d
import unittest
import os
import subprocess

print("Running tests on Diva Kernel")
print(" ")


class TestDivaKernel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.divadir = "/home/ctroupin/Software/DIVA/DIVA-diva-4.7.1/"
        cls.contourfile = "./datawrite/coast.cont"
        cls.datafile = "./datawrite/data.dat"
        cls.paramfile = "./datawrite/param.par"

        # Create contour
        cls.xc = [[-10, 10, 10, -10]]
        cls.yc = [[-10, -10, 10, 10]]
        contour = pydiva2d.Diva2DContours(cls.xc, cls.yc)
        contour.write_to(cls.contourfile)

        # Create parameter file
        parameters = pydiva2d.Diva2DParameters(3., 0, 11, 0, -10., -10., 0.1, 0.1,
                                               201, 201, -99, 1.0, 1.)
        parameters.write_to(cls.paramfile)

        # Create datafile
        data = pydiva2d.Diva2DData(x=[0], y=[0], field=[1.], weight=[1.])
        data.write_to(cls.datafile)

    def test_created_file(self):
        self.assertTrue(os.path.exists(self.contourfile))
        self.assertTrue(os.path.exists(self.datafile))
        self.assertTrue(os.path.exists(self.paramfile))

    def test_values(self):
        
        # Generate mesh
        pydiva2d.Diva2DMesh().make(divadir=self.divadir,
                                   contourfile=self.contourfile,
                                   paramfile=self.paramfile)
        # Perform analysis
        results = pydiva2d.Diva2DResults().make(divadir=self.divadir,
                                                datafile=self.datafile,
                                                paramfile=self.paramfile,
                                                contourfile=self.contourfile)

        self.assertAlmostEqual(results.analysis[100, 100], 0.50659037)
        self.assertAlmostEqual(results.analysis.mean(), 0.138724758537)
        self.assertAlmostEqual(results.analysis.min(), 0.035492767)
        self.assertAlmostEqual(results.analysis.max(), 0.50659037)
        self.assertAlmostEqual(results.analysis[12, 122], 0.0886603)

        self.assertAlmostEqual(results.error[100, 100], 0.7024312)
        self.assertAlmostEqual(results.error.mean(), 0.92658222707)
        self.assertAlmostEqual(results.error.min(), 0.7024312)
        self.assertAlmostEqual(results.error.max(), 0.98209327)
        self.assertAlmostEqual(results.error[44, -3], 0.97032255)

    @classmethod
    def tearDownClass(cls):
        print("Tearing down...")

        cls.divadir = "/home/ctroupin/Software/DIVA/DIVA-diva-4.7.1/"
        cls.contourfile = "./datawrite/coast.cont"
        cls.datafile = "./datawrite/data.dat"
        cls.paramfile = "./datawrite/param.par"

        # Clean Diva intermediate directories and files
        subprocess.run("./divaclean", cwd=os.path.join(cls.divadir, "DIVA3D/divastripped"),
                       stdout=subprocess.PIPE, shell=True)

        os.remove(cls.contourfile)
        os.remove(cls.paramfile)
        os.remove(cls.datafile)

if __name__ == '__main__':
    unittest.main()
