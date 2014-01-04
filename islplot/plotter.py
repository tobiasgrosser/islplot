import matplotlib.pyplot as _plt
import islpy as _islpy

def _get_point_coordinates(point):
    return (int(point.get_coordinate_val(_islpy.dim_type.set, 0).get_num_si()),
            int(point.get_coordinate_val(_islpy.dim_type.set, 1).get_num_si()))

def plot_points(islset, color="black", size=15):
    points = []
    islset.foreach_point(lambda x: points.append(_get_point_coordinates(x)))
    dimX = [x[0] for x in points]
    dimY = [x[1] for x in points]
    _plt.plot(dimX, dimY, ".", markersize=size, color=color, lw=0)
