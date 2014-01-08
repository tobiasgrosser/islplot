from islplot.support import *
from islpy import *

import unittest
from test import support

class TestGetVertexCoordinates(unittest.TestCase):
    def setUp(self):
        return

    def tearDown(self):
        return

    def test_2d_set_a(self):
        bset = BasicSet("{[i,j]: 0 <= i <= 10 and j = 0}")
        c = bset_get_vertex_coordinates(bset)
        assert c == [[0.0, 0.0], [10.0, 0.0]]

    def test_2d_set_b(self):
        bset = BasicSet("{[i,j]: 0 <= i,j <= 10}")
        c = bset_get_vertex_coordinates(bset)
        assert c == [[0.0, 0.0], [0.0, 10.0], [10.0, 10.0], [10.0, 0.0]]

    def test_2d_set_c(self):
        bset = BasicSet("{[i,j]: 0 <= i,j <= 10 and i + j < 2}")
        c = bset_get_vertex_coordinates(bset)
        assert c == [[0.0, 0.0], [0.0, 1.0], [1.0, 0.0]]

    def test_2d_set_d(self):
        bset = BasicSet("{[i,j]: 0 <= i,j <= 10 and i - j >= -4}")
        c = bset_get_vertex_coordinates(bset)
        assert c == [[0.0, 0.0], [0.0, 4.0], [6.0, 10.0], [10.0, 10.0], [10.0, 0.0]]

    def test_2d_set_with_non_integral_vertex(self):
        bset = BasicSet("{[i,j]: 0 <= i,j <= 9 and i - 2j >= -4}")
        c = bset_get_vertex_coordinates(bset)
        assert c == [[0.0, 0.0], [0.0, 2.0], [9.0, 6.5], [9.0, 0.0]]

    def test_2d_set_single_vertex(self):
        bset = BasicSet("{[2,2]}")
        c = bset_get_vertex_coordinates(bset)
        assert c == [[2.0, 2.0]]

if __name__ == '__main__':
    unittest.main()
