import unittest
import numpy as np
from pymatgen.core.structure import Structure
from pymatgen.core.lattice import Lattice
from topology.PyVMD import cmd_by_radius, cmd_by_bv, cmd_by_edge

class TestPyVMD(unittest.TestCase):
    def setUp(self):
        # Create a simple structure with properties for testing
        lattice = Lattice.cubic(3.0)
        coords = [[0.0, 0.0, 0.0], [0.5, 0.5, 0.5]]
        species = ["Li", "Li"]
        self.struct = Structure(lattice, species, coords, 
                                coords_are_cartesian=False,
                                site_properties={"voronoi_radius": [1.0, 0.5]})
        
        # Create nodes with BV properties for cmd_by_bv test
        self.bv_struct = Structure(lattice, species, coords, 
                                   coords_are_cartesian=False,
                                   site_properties={"valence_state": [1.0, 0.8]})
        
        # Add neighbor_nodes property for cmd_by_edge test
        neighbor_nodes = [[[1, 2.5, [0, 0, 0]]], [[0, 2.5, [0, 0, 0]]]]
        self.edge_struct = Structure(lattice, species, coords, 
                                    coords_are_cartesian=False,
                                    site_properties={
                                        "voronoi_radius": [1.0, 0.5],
                                        "neighbor_nodes": neighbor_nodes
                                    })
        
    def test_cmd_by_radius(self):
        # Test cmd_by_radius with r_cut=0.7 which should only include first site
        cmds = cmd_by_radius(self.struct, 0.7)
        self.assertEqual(len(cmds), 1)
        self.assertIn("draw sphere", cmds[0])
        
        # Test with molecular_id
        cmds = cmd_by_radius(self.struct, 0.7, molecular_id=1)
        self.assertEqual(len(cmds), 1)
        self.assertIn("graphics 1 sphere", cmds[0])
        
    def test_cmd_by_bv(self):
        # Test cmd_by_bv 
        cmds = cmd_by_bv(self.bv_struct)
        self.assertEqual(len(cmds), 2)
        for cmd in cmds:
            self.assertIn("draw text", cmd)
        
        # Test with molecular_id
        cmds = cmd_by_bv(self.bv_struct, molecular_id=1)
        self.assertEqual(len(cmds), 2)
        for cmd in cmds:
            self.assertIn("graphics 1 text", cmd)
            
    def test_cmd_by_edge(self):
        # Test cmd_by_edge
        cmds = cmd_by_edge(self.edge_struct, 1.0)
        self.assertEqual(len(cmds), 1)
        for cmd in cmds:
            self.assertIn("draw cylinder", cmd)
        
        # Test with molecular_id
        cmds = cmd_by_edge(self.edge_struct, 1.0, molecular_id=1)
        self.assertEqual(len(cmds), 1)
        for cmd in cmds:
            self.assertIn("graphics 1 cylinder", cmd)

if __name__ == '__main__':
    unittest.main()
