import pydiva2d
import unittest

class TestMeshMethods(unittest.TestCase):


    def setUp(self):
        self.EmptyMesh = pydiva2d.Diva2DMesh()
        self.meshfile = "./data/mesh.dat"
        self.meshtopofile = "./data/meshtopo.dat"
        self.coastfile = "./data/coast_mesh.cont"
        self.paramfile = "./data/param_mesh.par"
        self.divadir = "/home/ctroupin/Software/DIVA/DIVA-diva-4.7.1/"

    def test_init_empty(self):
        self.assertTrue(not(self.EmptyMesh.i1))
        self.assertTrue(not(self.EmptyMesh.nelements))
        self.assertTrue(not(self.EmptyMesh.ninterfaces))
        self.assertTrue(not(self.EmptyMesh.nnodes))

    def test_read_file(self):
        SquareMesh = pydiva2d.Diva2DMesh()
        SquareMesh.read_from(self.meshfile, self.meshtopofile)
        self.assertEqual(SquareMesh.nelements, 348)
        self.assertEqual(SquareMesh.nnodes, 197)
        self.assertEqual(SquareMesh.ninterfaces, 544)
        self.assertEqual(len(SquareMesh.i1), SquareMesh.nelements)
        self.assertEqual(len(SquareMesh.i1), len(SquareMesh.i2))
        self.assertEqual(len(SquareMesh.i2), len(SquareMesh.i3))
        self.assertEqual(SquareMesh.i1[6], 43)

    def test_read_file_numpy(self):
        SquareMesh = pydiva2d.Diva2DMesh()
        SquareMesh.read_from_np(self.meshfile, self.meshtopofile)
        self.assertEqual(SquareMesh.nelements, 348)
        self.assertEqual(SquareMesh.nnodes, 197)
        self.assertEqual(SquareMesh.ninterfaces, 544)
        self.assertEqual(len(SquareMesh.i1), SquareMesh.nelements)
        self.assertEqual(len(SquareMesh.i1), len(SquareMesh.i2))
        self.assertEqual(len(SquareMesh.i2), len(SquareMesh.i3))
        self.assertEqual(SquareMesh.i1[6], 43)

    def test_create_mesh(self):
        Mesh2create = pydiva2d.Diva2DMesh()
        Mesh2create.make(self.divadir, self.coastfile, self.paramfile)
        self.assertEqual(Mesh2create.nnodes, 16)
        self.assertEqual(Mesh2create.ninterfaces, 34)
        self.assertEqual(Mesh2create.nelements, 19)





