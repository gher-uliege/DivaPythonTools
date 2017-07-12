import pydiva2d
import unittest

class TestMeshMethods(unittest.TestCase):


    def setUp(self):
        self.EmptyMesh = pydiva2d.Diva2DMesh()
        self.meshfile = "./data/mesh.dat"
        self.meshtopofile = "./data/meshtopo.dat"
        self.nomeshfile = "./data/nomesh.dat"
        self.nomeshtopofile = "./data/nomeshtopo.dat"
        self.coastfile = "./data/coast_mesh.cont"
        self.paramfile = "./data/param_mesh.par"
        self.noparamfile = "./data/noparam_mesh.par"
        self.divadir = "/home/ctroupin/Software/DIVA/DIVA-diva-4.7.1/"

    def test_init_empty(self):
        """
        Instantiate an empty Mesh object
        """
        self.assertTrue(not(self.EmptyMesh.i1))
        self.assertTrue(not(self.EmptyMesh.nelements))
        self.assertTrue(not(self.EmptyMesh.ninterfaces))
        self.assertTrue(not(self.EmptyMesh.nnodes))

    def test_read_file(self):
        """
        Instantiate Mesh object by reading existing file
        """
        SquareMesh = pydiva2d.Diva2DMesh().read_from(self.meshfile, self.meshtopofile)
        self.assertEqual(SquareMesh.nelements, 348)
        self.assertEqual(SquareMesh.nnodes, 197)
        self.assertEqual(SquareMesh.ninterfaces, 544)
        self.assertEqual(len(SquareMesh.i1), SquareMesh.nelements)
        self.assertEqual(len(SquareMesh.i1), len(SquareMesh.i2))
        self.assertEqual(len(SquareMesh.i2), len(SquareMesh.i3))
        self.assertEqual(SquareMesh.i1[6], 43)

    def test_read_file_numpy(self):
        """
        Instantiate Mesh object by reading existing file
        using numpy module
        """
        SquareMesh = pydiva2d.Diva2DMesh().read_from_np(self.meshfile, self.meshtopofile)
        self.assertEqual(SquareMesh.nelements, 348)
        self.assertEqual(SquareMesh.nnodes, 197)
        self.assertEqual(SquareMesh.ninterfaces, 544)
        self.assertEqual(len(SquareMesh.i1), SquareMesh.nelements)
        self.assertEqual(len(SquareMesh.i1), len(SquareMesh.i2))
        self.assertEqual(len(SquareMesh.i2), len(SquareMesh.i3))
        self.assertEqual(SquareMesh.i1[6], 43)

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





