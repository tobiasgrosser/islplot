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

class Test_bset_get_faces(unittest.TestCase):
    def test_3d_empty(self):
        bset = BasicSet("{[i,j,k]: 1=0}")
        f = bset_get_faces(bset)
        assert f == []

    def test_3d_point(self):
        bset = BasicSet("{[i,j,k]: i = j = k = 0}")
        f = bset_get_faces(bset)
        assert f == [[[0.0, 0.0, 0.0]]]

    def test_3d_line(self):
        bset = BasicSet("{[i,j,k]: i = j = 0 and 0 <= k <= 10}")
        f = bset_get_faces(bset)
        assert f == [[[0.0, 0.0, 0.0], [0.0, 0.0, 10.0]]]

    def test_3d_triangle(self):
        bset = BasicSet("{[i,j,k]: 0 <= i,j <= 10 and i + j < 2 and k = 0}")
        f = bset_get_faces(bset)
        assert f == [[[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]]

    def test_3d_square(self):
        bset = BasicSet("{[i,j,k]: 0 <= i,k <= 10 and j = 2}")
        f = bset_get_faces(bset)
        assert f == [[[0.0, 2.0, 0.0], [10.0, 2.0, 0.0], [10.0, 2.0, 10.0], [0.0, 2.0, 10.0]]]

    def test_3d_pyramid(self):
        bset = BasicSet("{ [i, j, k] : 0 <= i,k,j and i + j + k <= 10}")
        f = bset_get_faces(bset)
        assert f == [[[0.0, 0.0, 0.0], [0.0, 10.0, 0.0], [0.0, 0.0, 10.0]],
                     [[0.0, 0.0, 0.0], [10.0, 0.0, 0.0], [0.0, 0.0, 10.0]],
                     [[0.0, 0.0, 0.0], [10.0, 0.0, 0.0], [0.0, 10.0, 0.0]],
                     [[0.0, 0.0, 10.0], [10.0, 0.0, 0.0], [0.0, 10.0, 0.0]]]

class Test_get_vertices_and_faces(unittest.TestCase):
    def test_3d_empty(self):
        bset = BasicSet("{[i,j,k]: 1=0}")
        v, f = get_vertices_and_faces(bset)
        assert v == []
        assert f == []

    def test_3d_point(self):
        bset = BasicSet("{[i,j,k]: i = j = k = 0}")
        v, f = get_vertices_and_faces(bset)
        assert v == [[0.0, 0.0, 0.0]]
        assert f == [[0]]

    def test_3d_line(self):
        bset = BasicSet("{[i,j,k]: i = j = 0 and 0 <= k <= 10}")
        v, f = get_vertices_and_faces(bset)
        assert v == [[0.0, 0.0, 0.0], [0.0, 0.0, 10.0]]
        assert f == [[0, 1]]

    def test_3d_triangle(self):
        bset = BasicSet("{[i,j,k]: 0 <= i,j <= 10 and i + j < 2 and k = 0}")
        v, f = get_vertices_and_faces(bset)
        assert v == [[0.0, 0.0, 0.0], [0.0, 1.0, 0.0], [1.0, 0.0, 0.0]]
        assert f == [[0, 2, 1]]

    def test_3d_square(self):
        bset = BasicSet("{[i,j,k]: 0 <= i,k <= 10 and j = 2}")
        v, f = get_vertices_and_faces(bset)
        assert v == [[0.0, 2.0, 0.0], [0.0, 2.0, 10.0], [10.0, 2.0, 0.0], [10.0, 2.0, 10.0]]
        assert f == [[0, 2, 3, 1]]

    def test_3d_pyramid(self):
        bset = BasicSet("{ [i, j, k] : 0 <= i,k,j and i + j + k <= 10}")
        v, f = get_vertices_and_faces(bset)
        assert v == [[0.0, 0.0, 0.0], [0.0, 0.0, 10.0], [0.0, 10.0, 0.0], [10.0, 0.0, 0.0]]
        assert f == [[0, 2, 1], [0, 3, 1], [0, 3, 2], [1, 3, 2]]

if __name__ == '__main__':
    unittest.main()
