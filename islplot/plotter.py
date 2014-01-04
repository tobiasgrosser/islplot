import matplotlib.pyplot as _plt
import islpy as _islpy

def _get_point_coordinates(point):
    return (int(point.get_coordinate_val(_islpy.dim_type.set, 0).get_num_si()),
            int(point.get_coordinate_val(_islpy.dim_type.set, 1).get_num_si()))

def plot_points(set_data, color="black", size=15):
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
