from typing import Any, Dict

import numpy as np
from numpy import linalg as la
import numpy.typing as npt

from .util import np_windowed, prepare


def double_triangle_area(vertices: npt.NDArray[np.float_]) -> npt.NDArray[np.float_]:
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


def get_squared_vector_lengths(vertices: npt.NDArray[np.float_]) -> npt.NDArray[np.float_]:
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


def get_curvature(vertices: npt.NDArray[np.float_]) -> npt.NDArray[np.float_]:
    area = double_triangle_area(vertices)
    value = 4 * area * area / np.prod(get_squared_vector_lengths(vertices))
    curvature: npt.NDArray[np.float_] = np.sqrt(value)
    return curvature


@prepare
def menger(x: npt.NDArray[np.float_], y: npt.NDArray[np.float_], **kwargs: Dict[Any, Any]) -> int:
    assert len(kwargs) == 0
    assert x.shape == y.shape
    indices = np_windowed(len(x), 3)
    data_points = np.stack((x[indices], y[indices]), axis=-1)
    curve_scores = np.array([get_curvature(row) for row in data_points])
    return curve_scores.argmax().item() + 1


@prepare
def find_knee(x: npt.NDArray[np.float_], y: npt.NDArray[np.float_], method="menger", **kwargs: Dict[Any, Any]) -> int:
    assert method == "menger"
    return menger(x, y, **kwargs)
