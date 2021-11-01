import numpy as np
from numpy import linalg as la

from .util import np_anchored, np_windowed


def double_triangle_area(vertices):
    """
    Return twice the area of a triangle with the given vertices.
    Args:
        vertices: np.ndarray, 3x2 matrix where every row is a new 2-D vertex (x, y)
    Returns:
        double_area: np.ndarray, 1x1 double of the area
    """
    assert vertices.shape == (3, 2)
    double_area = abs(la.det(np.hstack((vertices, np.ones((3, 1), dtype=vertices.dtype)))))
    return double_area


def get_squared_vector_lengths(vertices):
    """
    Return the square of the lengths between neighbouring vertices
    Args:
        vertices: np.ndarray, array of vertices

    Returns:
        lengths: np.ndarray, the entry at `lenghts[i]` is a squared distance between the vertex `i` and `i+1`
    """
    vector_differences = np.empty(vertices.shape)

    rolled = np.roll(vertices, -1, axis=0)
    np.subtract(rolled, vertices, out=vector_differences)
    lengths = np.einsum("ij,ij->i", vector_differences, vector_differences)
    return lengths


def get_curvature(vertices):
    """
    Calculate the Menger curvature defined by the three points
    Args:
        vertices: np.ndarray, 3x2 matrix where every row is a new 2-D vertex (x, y)

    Returns:
        curvature: np.ndarray, the reciprocal of the radius of the circumcircle around the vertices
    """
    area = double_triangle_area(vertices)
    value = 4 * area * area / np.prod(get_squared_vector_lengths(vertices))
    curvature = np.sqrt(value)
    return curvature


def menger_successive(x, y, **kwargs):
    """
    Find a knee using the Menger curvature on the three successive points
    Args:
        x: np.ndarray, the x coordinates of the points
        y: np.ndarray, the y coordinates of the points
        **kwargs: possible additional arguments (none are used)

    Returns: int, the index of the knee
    """
    assert len(kwargs) == 0
    assert x.shape == y.shape
    indices = np_windowed(len(x), 3)
    data_points = np.stack((x[indices], y[indices]), axis=-1)
    curve_scores = np.array([get_curvature(row) for row in data_points])
    return curve_scores.argmax().item() + 1


def menger_anchored(x, y, **kwargs):
    """
    Find a knee using the Menger curvature on the first point, last point, and varying the middle point.
    More resistant to the noise in the data than menger_successive

    Args:
        x: np.ndarray, the x coordinates of the points
        y: np.ndarray, the y coordinates of the points
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
