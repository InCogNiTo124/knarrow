from typing import Callable

from mypy_extensions import KwArg
import numpy as np
from numpy import linalg as la
import numpy.typing as npt

from .util import np_anchored, np_windowed, prepare


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
    area = double_triangle_area(vertices)
    value = 4 * area * area / np.prod(get_squared_vector_lengths(vertices))
    curvature: npt.NDArray[np.float_] = np.sqrt(value)
    return curvature


@prepare
def menger_successive(x, y, **kwargs):
    assert len(kwargs) == 0
    assert x.shape == y.shape
    indices = np_windowed(len(x), 3)
    data_points = np.stack((x[indices], y[indices]), axis=-1)
    curve_scores = np.array([get_curvature(row) for row in data_points])
    return curve_scores.argmax().item() + 1


@prepare
def menger_anchored(x, y, **kwargs):
    assert len(kwargs) == 0
    assert x.shape == y.shape
    # perhaps later `menger_anchored` and `menger_successive` can be united in the future
    # since the only difference is this line
    indices = np_anchored(len(x))
    data_points = np.stack((x[indices], y[indices]), axis=-1)
    curve_scores = np.array([get_curvature(row) for row in data_points])
    return curve_scores.argmax().item() + 1


@prepare
def find_knee(x, y, method="menger_successive", **kwargs):
    assert method in ["menger_successive", "menger_anchored"]
    function: Callable[[npt.NDArray[np.float_], npt.NDArray[np.float_], KwArg()], int] = locals()[method]
    return function(x, y, **kwargs)
