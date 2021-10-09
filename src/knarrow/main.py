from typing import Callable

from mypy_extensions import KwArg
import numpy as np
from numpy import linalg as la
import numpy.typing as npt

from .util import normalize, np_anchored, np_windowed, prepare


def double_triangle_area(vertices):
    """
    Return twice the area of a triangle with the given vertices.
    Args:
        vertices: npt.NDArray, 3x2 matrix where every row is a new 2-D vertex (x, y)
    Returns:
        double_area: npt.NDArray, 1x1 double of the area
    """
    assert vertices.shape == (3, 2)
    double_area: npt.NDArray[np.float_] = abs(la.det(np.hstack((vertices, np.ones((3, 1), dtype=vertices.dtype)))))
    return double_area


def get_squared_vector_lengths(vertices):
    """
    Return the square of the lengths between neighbouring vertices
    Args:
        vertices: npt.NDArray, array of vertices

    Returns:
        lengths: npt.NDArray, the entry at `lenghts[i]` is a squared distance between the vertex `i` and `i+1`
    """
    vector_differences = np.empty(vertices.shape)

    rolled = np.roll(vertices, -1, axis=0)
    np.subtract(rolled, vertices, out=vector_differences)
    lengths: npt.NDArray[np.float_] = np.einsum("ij,ij->i", vector_differences, vector_differences)
    return lengths


def get_curvature(vertices):
    """
    Calculate the Menger curvature defined by the three points
    Args:
        vertices: npt.NDArray, 3x2 matrix where every row is a new 2-D vertex (x, y)

    Returns:
        curvature: npt.NDArray, the reciprocal of the radius of the circumcircle around the vertices
    """
    area = double_triangle_area(vertices)
    value = 4 * area * area / np.prod(get_squared_vector_lengths(vertices))
    curvature: npt.NDArray[np.float_] = np.sqrt(value)
    return curvature


@prepare
def menger_successive(x, y, **kwargs):
    """
    Find a knee using the Menger curvature on the three successive points
    Args:
        x: npt.NDArray, the x coordinates of the points
        y: npt.NDArray, the y coordinates of the points
        **kwargs: possible additional arguments (none are used)

    Returns: int, the index of the knee
    """
    assert len(kwargs) == 0
    assert x.shape == y.shape
    indices = np_windowed(len(x), 3)
    data_points = np.stack((x[indices], y[indices]), axis=-1)
    curve_scores = np.array([get_curvature(row) for row in data_points])
    return curve_scores.argmax().item() + 1


@prepare
def menger_anchored(x, y, **kwargs):
    """
        Find a knee using the Menger curvature on the first point, last point, and varying the middle point.
        More resistant to the noise in the data than menger_successive

        Args:
            x: npt.NDArray, the x coordinates of the points
            y: npt.NDArray, the y coordinates of the points
            **kwargs: possible additional arguments (none are used)
    e
        Returns: int, the index of the knee
    """
    assert len(kwargs) == 0
    assert x.shape == y.shape
    # perhaps later `menger_anchored` and `menger_successive` can be united in the future
    # since the only difference is this line
    indices = np_anchored(len(x))
    data_points = np.stack((x[indices], y[indices]), axis=-1)
    curve_scores = np.array([get_curvature(row) for row in data_points])
    return curve_scores.argmax().item() + 1


@prepare
def angle(x, y, **kwargs):
    """
    Find a knee by looking at the maximum change of the angle between neighbouring points

    Args:
        x: npt.NDArray, the x coordinates of the points
        y: npt.NDArray, the y coordinates of the points
        **kwargs: possible additional arguments (none are used)

    Returns: int, the index of the knee
    """
    assert len(kwargs) == 0
    assert x.shape == y.shape
    d_x = np.diff(x)
    d_y = np.diff(y)
    angles = np.abs(np.arctan2(d_y, d_x))
    angle_differences = np.diff(angles)
    max_diff = angle_differences.argmax().item()
    return max_diff + 1


@prepare
def distance(x, y, **kwargs):
    """
    Find a knee by finding a point which is most distant from the line y=x (after normalizing the inputs)
    Fun fact: *vertical* distance of a point P from line y=x is just a scaled version of the *orthogonal* distance of
    the same point P from line x=y.

    Args:
        x: npt.NDArray, the x coordinates of the points
        y: npt.NDArray, the y coordinates of the points
        **kwargs: possible additional arguments (non are used)

    Returns: int, the index of the knee
    """
    assert len(kwargs) == 0
    assert x.shape == y.shape
    x_scaled = normalize(x)
    y_scaled = normalize(y)
    distances = abs(y_scaled - x_scaled)
    return np.argmax(distances).item()


@prepare
def find_knee(x, y, method="menger_successive", **kwargs):
    """
    Public method for finding the knee

    Args:
        x: npt.NDArray, the x coordinates of the points
        y: npt.NDArray, the y coordinates of the points
        method: str, denotes the method to be used (default: menger_successive)
        **kwargs: possible additional arguments for the knee-finding method

    Returns: int, the index of the knee
    """
    assert method in ["menger_successive", "menger_anchored", "angle", "distance_vert"]
    function: Callable[[npt.NDArray[np.float_], npt.NDArray[np.float_], KwArg()], int] = locals()[method]
    return function(x, y, **kwargs)
