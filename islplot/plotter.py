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
