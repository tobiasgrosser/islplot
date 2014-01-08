import matplotlib.pyplot as _plt
import islpy as _islpy
from islplot.support import *

def _get_point_coordinates(point):
    return (int(point.get_coordinate_val(_islpy.dim_type.set, 0).get_num_si()),
            int(point.get_coordinate_val(_islpy.dim_type.set, 1).get_num_si()))

def plot_set_points(set_data, color="black", size=10, marker="o"):
    """
    Plot the individual points of a two dimensional isl set.

    :param set_data: The islpy.Set to plot.
    :param color: The color of the points.
    :param size: The diameter of the points.
    :param marker: The marker used to mark a point.
    """
    points = []
    set_data.foreach_point(lambda x: points.append(_get_point_coordinates(x)))
    dimX = [x[0] for x in points]
    dimY = [x[1] for x in points]
    _plt.plot(dimX, dimY, marker, markersize=size, color=color, lw=0)

def _plot_arrow(start, end, graph, *args, **kwargs):
    shrinkA = 10
    shrinkB = 10
    graph.annotate("", xy=start, xycoords='data',
                xytext=end, textcoords='data',
                arrowprops=dict(arrowstyle="<-",
                                connectionstyle="arc3",
                                shrinkA=shrinkA,
                                shrinkB=shrinkB)
               )

def plot_map(map_data, color="black"):
    """
    Given a map from a two dimensional set to another two dimensional set this
    functions prints the relations in this map as arrows going from the input
    to the output element.

    :param map_data: The islpy.Map to plot.
    :param color: The color of the arrows.
    """
    start_points = []

    map_data.range().foreach_point(start_points.append)

    for start in start_points:
        end_points = []
        limited = map_data.intersect_range(_islpy.BasicSet.from_point(start))
        limited.domain().foreach_point(end_points.append)
        for end in end_points:
                _plot_arrow(_get_point_coordinates(end),
                            _get_point_coordinates(start),
                            _plt, color=color)

def plot_bset_shape(bset_data, show_vertices=True, color="gray",
                    vertex_color=None,
                    vertex_marker="o", vertex_size=10):
    """
    Given an basic set, plot the shape formed by the constraints that define
    the basic set.

    :param bset_data: The basic set to plot.
    :param show_vertices: Show the vertices at the corners of the basic set's
                          shape.
    :param color: The backbround color of the shape.
    :param vertex_color: The color of the vertex markers.
    :param vertex_marker: The marker used to draw the vertices.
    :param vertex_size: The size of the vertices.
    """

    assert bset_data.is_bounded(), "Expected bounded set"

    if not vertex_color:
        vertex_color = color

    vertices = bset_get_vertex_coordinates(bset_data)

    if show_vertices:
        dimX = [x[0] for x in vertices]
        dimY = [x[1] for x in vertices]
        _plt.plot(dimX, dimY, vertex_marker, markersize=vertex_size,
                  color=vertex_color)

    if len(vertices) == 0:
        return

    import matplotlib.path as _matplotlib_path
    import matplotlib.patches as _matplotlib_patches
    Path = _matplotlib_path.Path
    PathPatch = _matplotlib_patches.PathPatch
    codes = [Path.LINETO] * len(vertices)
    codes[0] = Path.MOVETO
    pathdata = [(code, tuple(coord)) for code, coord in zip(codes, vertices)]
    pathdata.append((Path.CLOSEPOLY, (0, 0)))
    codes, verts = zip(*pathdata)
    path = Path(verts, codes)
    patch = PathPatch(path, facecolor=color)
    _plt.gca().add_patch(patch)

def plot_set_shapes(set_data, *args, **kwargs):
    """
    Plot a set of concex shapes for the individual basic sets this set consists
    of.

    :param set_data: The set to plot.
    """

    assert set_data.is_bounded(), "Expected bounded set"

    set_data.foreach_basic_set(lambda x: plot_bset_shape(x, **kwargs))


def plot_map_as_groups(bmap, color="gray", vertex_color=None, vertex_marker="o",
                       vertex_size=10):
    """
    Plot a map in groups of convex sets

    This function expects a map that assigns each domain element a single
    group id, such that each group forms a convex set of points. This function
    plots now each group as such a convex shape.

    This is e.g. useful to illustrate a tiling that is given as a between
    iteration vectors to tile ids.

    :param bmap: The map defining the groups of convex sets.
    :param vertex_color: The color the vertices are plotted.
    :param vertex_size: The size the vertices are plotted.
    :param vertex_marker: The marker the vertices are plotted as.
    :param color: The color the shapes are plotted.
    """

    if not vertex_color:
        vertex_color = color

    points = []
    range = bmap.range()
    range.foreach_point(points.append)

    for point in points:
        point_set = _islpy.BasicSet.from_point(point)
        part_set = bmap.intersect_range(point_set).domain()
        part_set_convex = part_set.convex_hull()

        # We currently expect that each group can be represented by a
        # single convex set.
        assert (part_set == part_set_convex)

        part_set = part_set_convex

        plot_set_points(part_set, color=vertex_color, size=vertex_size,
                        marker=vertex_marker)
        plot_bset_shape(part_set, color=color, vertex_color=vertex_color,
                        vertex_size=vertex_size, vertex_marker=vertex_marker)

__all__ = ['plot_set_points', 'plot_bset_shape', 'plot_set_shapes',
           'plot_map', 'plot_map_as_groups']
