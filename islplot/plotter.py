import matplotlib.pyplot as _plt
import islpy as _islpy

def _get_point_coordinates(point):
    return (int(point.get_coordinate_val(_islpy.dim_type.set, 0).get_num_si()),
            int(point.get_coordinate_val(_islpy.dim_type.set, 1).get_num_si()))

def plot_set_points(set_data, color="black", size=15):
    """
    Plot the individual points of a two dimensional isl set.

    :param set_data: The islpy.Set to plot.
    :param color: The color of the points.
    :param size: The diameter of the points.
    """
    points = []
    set_data.foreach_point(lambda x: points.append(_get_point_coordinates(x)))
    dimX = [x[0] for x in points]
    dimY = [x[1] for x in points]
    _plt.plot(dimX, dimY, ".", markersize=size, color=color, lw=0)

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

def _getValueOfDim(c):
    """
    Derive the value of a dimension from an appropriate constraint.

    This function expects an equality constraint without any existentially
    quantified dimensions for which at most one coefficient is non-zero.

    Example:
        [i,j]: 2i = 7

        => i = 7/2 = 3.5
    """
    assert c.is_equality(), "Equality constraint expected"
    assert not c.is_div_constraint(), "Div constraints not allowed"
    assert c.space.is_set(), "Only set spaces allowed"

    dimension = None
    coefficient = None

    for i in range(c.space.dim(_islpy.dim_type.set)):
        coef = c.get_coefficient_val(_islpy.dim_type.set, i).get_num_si()
        if coef == 0:
            continue

        assert dimension == None, "More than one dimension with coefficient"

        dimension = i
        coefficient = coef

    constant = c.get_constant_val().get_num_si()

    assert dimension != None, "Could not find a single dimension"

    value = float(-constant)/float(coefficient)

    return {'dim': dimension, 'val': value}

def _isl_vertex_get_coordinates(vertex):
    """
    Get the coordinates of the an isl vertex as a tuple of float values.

    To extract the coordinates we first get the expression defining the vertex.
    This expression is given as a rational set that specifies its (possibly
    rational) coordinates. We then convert this set into the tuple we will
    return.

    Example:

    For a vertex defined by the rational set
    { rat: S[i, j] : 2i = 7 and 2j = 9 } we produce the output (7/2, 9/2).

    :param vertex: The vertex from which we extract the coordinates.
    """
    rset = vertex.get_expr()
    coordinates = []
    rset.foreach_constraint(lambda x: coordinates.append(_getValueOfDim(x)))

    value = [None] * rset.dim(_islpy.dim_type.set)

    for c in coordinates:
        assert value[c['dim']] == None, "Value already set"
        value[c['dim']] = c['val']

    assert not None in value, "Not all dimensions specified"

    return value

def _isl_bset_get_vertex_coordinates(bset_data):
    """
    Given a basic set return the list of vertices at the corners.

    :param bset_data: The basic set to get the verteces from
    """

    # Get the vertices.
    vertices = []
    bset_data.compute_vertices().foreach_vertex(vertices.append)
    vertices = list(map(_isl_vertex_get_coordinates, vertices))

    # Sort the vertices in clockwise order.
    #
    # We select a 'center' point that lies within the convex hull of the
    # vertices. We then sort all points according to the direction (given as an
    # angle in radiens) they lie in respect to the center point.
    from math import atan2 as _atan2
    center = ((vertices[0][0] + vertices[1][0]) / 2.0,
              (vertices[0][1] + vertices[1][1]) / 2.0)
    f = lambda x: _atan2(x[0]-center[0], x[1]-center[1])
    vertices = sorted(vertices, key=f)
    return vertices

def plot_bset_shape(bset_data, show_vertices=True, *args, **kwargs):
    """
    Given an basic set, plot the shape formed by the constraints that define
    the basic set.

    :param bset_data: The basic set to plot.
    :param show_vertices: Show the vertices at the corners of the basic set's
                          shape.
    """

    vertices = _isl_bset_get_vertex_coordinates(bset_data)

    if show_vertices:
        dimX = [x[0] for x in vertices]
        dimY = [x[1] for x in vertices]
        _plt.plot(dimX, dimY, ".")

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
    patch = PathPatch(path, **kwargs)
    _plt.gca().add_patch(patch)

def plot_set_shapes(set_data, *args, **kwargs):
    """
    Plot a set of concex shapes for the individual basic sets this set consists
    of.

    :param set_data: The set to plot.
    """
    set_data.foreach_basic_set(lambda x: plot_bset_shape(x, **kwargs))

__all__ = ['plot_set_points', 'plot_bset_shape', 'plot_set_shapes',
           'plot_map']
