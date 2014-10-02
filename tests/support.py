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

    def test_3d_stretched_diamond(self):
        bset = BasicSet("{ [i, j, k] : 0 <= i,k,j and i + j < 4 and k < 4}")
        f = bset_get_faces(bset)
        assert f == [[[0.0, 0.0, 0.0], [0.0, 3.0, 0.0], [0.0, 3.0, 3.0], [0.0, 0.0, 3.0]],
                     [[0.0, 0.0, 0.0], [3.0, 0.0, 0.0], [0.0, 3.0, 0.0]],
                     [[0.0, 0.0, 0.0], [3.0, 0.0, 0.0], [3.0, 0.0, 3.0], [0.0, 0.0, 3.0]],
                     [[0.0, 0.0, 3.0], [3.0, 0.0, 3.0], [0.0, 3.0, 3.0]],
                     [[0.0, 3.0, 0.0], [3.0, 0.0, 0.0], [3.0, 0.0, 3.0], [0.0, 3.0, 3.0]]]

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

    def test_3d_rational_vertices(self):
        bset = BasicSet("{ [i, j, k] : 0 <= i , j, k and i,k+2j <= 3 }")
        v, f = get_vertices_and_faces(bset)
        assert v == [[0.0, 0.0, 0.0], [0.0, 0.0, 3.0], [0.0, 1.5, 0.0],
                     [3.0, 0.0, 0.0], [3.0, 0.0, 3.0], [3.0, 1.5, 0.0]]
        assert f == [[0, 2, 1], [0, 3, 4, 1], [0, 3, 5, 2], [1, 4, 5, 2],
                     [3, 5, 4]]
    def test_3d_rational_vertices2(self):
        bset = BasicSet("{ [i0, i1, i2] : i0 >= 0 and i2 >= -i1 and i2 <= 15 - i0 - 2i1 and 2i1 >= 3 + i0 and 2i1 <= 15 + i0 and i2 <= -3 and i2 >= -15 }")
        f1 = bset_get_faces(bset)
        v, f = get_vertices_and_faces(bset)
        assert v == [[0.0, 3.0, -3.0], [0.0, 7.5, -7.5], [0.0, 7.5, -3.0],
                     [1.5, 8.25, -3.0], [3.0, 3.0, -3.0], [5.0, 10.0, -10.0],
                     [7.5, 5.25, -3.0], [9.0, 6.0, -6.0]]
        assert f == [[0, 2, 1], [0, 4, 6, 3, 2], [0, 4, 7, 5, 1], [1, 5, 3, 2],
                     [3, 6, 7, 5], [4, 7, 6]]

class Test_bset_get_points(unittest.TestCase):
    def test_scale(self):
        bset = BasicSet("{[i]: 0 <= i  <= 1}")
        p = bset_get_points(bset, scale=10)
        assert p == [[0], [0.1]]

    def test_scale_2(self):
        bset = BasicSet("{[i]: 0 <= i  <= 1}")
        p = bset_get_points(bset, scale=20)
        assert p == [[0], [0.05]]

    def test_cube(self):
        bset = BasicSet("{[i,j,k]: 0 <= i,j,k <= 2}")
        p = bset_get_points(bset)
        assert p == [[0, 0, 0], [0, 0, 1], [0, 0, 2],
                     [0, 1, 0], [0, 1, 1], [0, 1, 2],
                     [0, 2, 0], [0, 2, 1], [0, 2, 2],

                     [1, 0, 0], [1, 0, 1], [1, 0, 2],
                     [1, 1, 0], [1, 1, 1], [1, 1, 2],
                     [1, 2, 0], [1, 2, 1], [1, 2, 2],

                     [2, 0, 0], [2, 0, 1], [2, 0, 2],
                     [2, 1, 0], [2, 1, 1], [2, 1, 2],
                     [2, 2, 0], [2, 2, 1], [2, 2, 2]]

    def test_cube_only_hull(self):
        bset = BasicSet("{[i,j,k]: 0 <= i,j,k <= 2}")
        p = bset_get_points(bset, only_hull=True)
        assert p == [[0, 0, 0], [0, 0, 1], [0, 0, 2],
                     [0, 1, 0], [0, 1, 1], [0, 1, 2],
                     [0, 2, 0], [0, 2, 1], [0, 2, 2],

                     [1, 0, 0], [1, 0, 1], [1, 0, 2],
                     [1, 1, 0],            [1, 1, 2],
                     [1, 2, 0], [1, 2, 1], [1, 2, 2],

                     [2, 0, 0], [2, 0, 1], [2, 0, 2],
                     [2, 1, 0], [2, 1, 1], [2, 1, 2],
                     [2, 2, 0], [2, 2, 1], [2, 2, 2]]

class Test_get_rectangular_hull(unittest.TestCase):
    def test_triangular(self):
        bset = BasicSet("{[i,j]: 0 <= i,j and i <= 2 and j + i <= 4}")
        p = get_rectangular_hull(bset, offset=0)
        assert p.is_equal(Set("{ [i, j] : 0 <= i <= 2 and 0 <= j <= 4 }"))

    def test_triangular_offset(self):
        bset = BasicSet("{[i,j]: 0 <= i,j and i <= 2 and j + i <= 4}")
        p = get_rectangular_hull(bset, offset=2)
        assert p.is_equal(Set("{ [i, j] : -2 <= i <= 4 and -2 <= j <= 6 }"))

class Test_sort_points(unittest.TestCase):
    def test_empty(self):
        res = sort_points([])
        assert res == []

    def test_single(self):
        bset = BasicSet("{[0,1,2]}")
        points = []
        bset.foreach_point(points.append)
        points = sort_points(points)
        points = list(map(get_point_coordinates, points))
        assert points == [[0,1,2]]

    def test_single(self):
        bset1 = BasicSet("{[x,y]: 0 <= x, y <= 1}")
        bset2 = BasicSet("{[x,y]: -1 <= x, y <= 0}")
        points = []
        bset1.foreach_point(points.append)
        bset2.foreach_point(points.append)
        points = sort_points(points)
        points = list(map(get_point_coordinates, points))
        assert points == [[-1, -1], [-1, 0],
                          [0, -1], [0, 0], [0, 0], [0, 1],
                          [1, 0], [1, 1]]


if __name__ == '__main__':
    unittest.main()
