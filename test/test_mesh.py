import pydiva2d
import unittest
import subprocess
import os


print("Running tests on Diva mesh")
print(" ")


class TestMeshMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.EmptyMesh = pydiva2d.Diva2DMesh()
        cls.meshfile = "./dataread/mesh.dat"
        cls.meshtopofile = "./dataread/meshtopo.dat"
        cls.nomeshfile = "./dataread/nomesh.dat"
        cls.nomeshtopofile = "./dataread/nomeshtopo.dat"
        cls.coastfile = "./dataread/coast_mesh.cont"
        cls.paramfile = "./dataread/param_mesh.par"
        cls.noparamfile = "./dataread/noparam_mesh.par"
        cls.divadir = "/home/ctroupin/Software/DIVA/DIVA-diva-4.7.1/"
        cls.nogeojsonfile = "./nodata/mesh.js"
        cls.geojsonfile = "./datawrite/mesh.js"

    def test_init_empty(self):
        """
        Instantiate an empty Mesh object
        """
        self.assertTrue(not self.EmptyMesh.i1)
        self.assertTrue(not self.EmptyMesh.nelements)
        self.assertTrue(not self.EmptyMesh.ninterfaces)
        self.assertTrue(not self.EmptyMesh.nnodes)

    def test_read_file(self):
        """
        Instantiate Mesh object by reading existing file
        """
        squaremesh = pydiva2d.Diva2DMesh().read_from(self.meshfile, self.meshtopofile)
        self.assertEqual(squaremesh.nelements, 348)
        self.assertEqual(squaremesh.nnodes, 197)
        self.assertEqual(squaremesh.ninterfaces, 544)
        self.assertEqual(len(squaremesh.i1), squaremesh.nelements)
        self.assertEqual(len(squaremesh.i1), len(squaremesh.i2))
        self.assertEqual(len(squaremesh.i2), len(squaremesh.i3))
        self.assertEqual(squaremesh.i1[6], 43)

    def test_read_file_numpy(self):
        """
        Instantiate Mesh object by reading existing file
        using numpy module
        """
        squaremesh = pydiva2d.Diva2DMesh().read_from_np(self.meshfile, self.meshtopofile)
        self.assertEqual(squaremesh.nelements, 348)
        self.assertEqual(squaremesh.nnodes, 197)
        self.assertEqual(squaremesh.ninterfaces, 544)
        self.assertEqual(len(squaremesh.i1), squaremesh.nelements)
        self.assertEqual(len(squaremesh.i1), len(squaremesh.i2))
        self.assertEqual(len(squaremesh.i2), len(squaremesh.i3))
        self.assertEqual(squaremesh.i1[6], 43)

    def test_read_nonexisting_file(self):
        """
        Try instantiate Mesh object reading an non-existing file
        """

        self.assertRaises(FileNotFoundError,
                          lambda: pydiva2d.Diva2DMesh().read_from_np(self.nomeshfile, self.nomeshtopofile))
        self.assertRaises(FileNotFoundError,
                          lambda: pydiva2d.Diva2DMesh().read_from_np(self.meshfile, self.nomeshtopofile))
        self.assertRaises(FileNotFoundError,
                          lambda: pydiva2d.Diva2DMesh().read_from_np(self.nomeshfile, self.meshtopofile))

        self.assertRaises(FileNotFoundError,
                          lambda: pydiva2d.Diva2DMesh().read_from(self.nomeshfile, self.nomeshtopofile))
        self.assertRaises(FileNotFoundError,
                          lambda: pydiva2d.Diva2DMesh().read_from(self.meshfile, self.nomeshtopofile))
        self.assertRaises(FileNotFoundError,
                          lambda: pydiva2d.Diva2DMesh().read_from(self.nomeshfile, self.meshtopofile))

    def test_create_mesh(self):
        """
        Generate Mesh from existing, simple parameter and contour files
        """
        mesh = pydiva2d.Diva2DMesh().make(self.divadir, self.coastfile, self.paramfile)
        self.assertEqual(mesh.nnodes, 16)
        self.assertEqual(mesh.ninterfaces, 34)
        self.assertEqual(mesh.nelements, 19)

    def test_write_nonexisting_geojson(self):
        """
        Check if error is raised when the file cannot be written
        """
        squaremesh = pydiva2d.Diva2DMesh().read_from(self.meshfile, self.meshtopofile)
        self.assertRaises(FileNotFoundError,
                          lambda: squaremesh.to_geojson(filename=self.nogeojsonfile))

    def test_write_geojson(self):
        """
        Check if geoJSON is properly created from finite-element mesh
        """
        squaremesh = pydiva2d.Diva2DMesh().read_from(self.meshfile, self.meshtopofile)
        squaremesh.to_geojson(filename=self.geojsonfile)

        self.assertTrue(os.path.exists(self.geojsonfile))

        with open(self.geojsonfile) as f:
            lines = f.readlines()
            line0 = lines[0].rstrip()

        self.assertEqual(line0, "var mesh = {")
        self.assertEqual(len(lines), 6965)

        squaremesh.to_geojson(filename=self.geojsonfile, varname="divamesh")
        self.assertTrue(os.path.exists(self.geojsonfile))

        with open(self.geojsonfile) as f:
            lines = f.readlines()
            line0 = lines[0].rstrip()

        self.assertEqual(line0, "var divamesh = {")
        self.assertEqual(len(lines), 6965)

    @classmethod
    def tearDownClass(cls):

        cls.divadir = "/home/ctroupin/Software/DIVA/DIVA-diva-4.7.1/"
        cls.geojsonfile = "./datawrite/mesh.js"

        # Clean Diva intermediate directories and files
        subprocess.run("./divaclean", cwd=os.path.join(cls.divadir, "DIVA3D/divastripped"),
                       stdout=subprocess.PIPE, shell=True)

        os.remove(cls.geojsonfile)
