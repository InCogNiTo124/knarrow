from typing import Any, Callable, Dict, Union

from mypy_extensions import KwArg, VarArg
import numpy as np
import numpy.linalg as la
import numpy.typing as npt

Number = Union[int, float]


def np_windowed(length: int, window_size: int, stride: int = 1, dilation: int = 1) -> npt.NDArray[np.int_]:
    """
    Return indices x such that every row in array[x] is a windowed slice of the array
    Helper function which uses numpy broadcasting to work
    Adapted from: https://stackoverflow.com/a/42258242

    Args:
        length: int, the total length of the array to be indexed
        window_size: int, the size of the window to be slided across the array
        stride: int, the size of the "jumps" between the consecutive windows (default: 1)
        dilation: int, the distance between the elements in the window (default: 1)

    Returns: npt.NDArray, indices for windowing an array
    """
    base_indices: npt.NDArray[np.int_] = stride * np.arange((length - window_size) // (stride * dilation) + 1).reshape(
        -1, 1
    )
    windows: npt.NDArray[np.int_] = dilation * np.arange(window_size).reshape(1, -1)
    return windows + base_indices  # broadcasting trick


def np_anchored(length: int) -> npt.NDArray[np.int_]:
    """
    Return indices x such that every row in array[x] is a slice of the array with a first, i-th and the last element
    Helper function which uses numpy broadcasting to work

    Args:
        length: int, the total length of the array to be indexed in the anchored way
    Returns: npt.NDArray, indices for windowing an array

    """
    indices = list(range(1, length - 1))
    first = [0] * len(indices)
    last = [length - 1] * len(indices)
    indices = np.stack((first, indices, last), axis=-1)
    return indices


def prepare(
    f: Callable[[npt.NDArray[np.float_], npt.NDArray[np.float_], str, KwArg(Dict[Any, Any])], int]
) -> Callable[[VarArg(), KwArg()], int]:
    def inner(*args: VarArg(), **kwargs: KwArg()) -> int:
        assert 1 <= len(args) <= 2
        if len(args) == 2:
            x = np.array(args[0])
            assert x.ndim == 1 and x.shape[0] > 3
            y = np.array(args[1])
            assert y.ndim == 1 and y.shape[0] > 3
        elif len(args) == 1:
            argument = np.array(args[0]).squeeze()  # squeeze ensures all dimensions are > 1
            assert 1 <= argument.ndim <= 2
            if argument.ndim == 1:
                assert argument.shape[0] >= 3, "The input must have at least 3 points"
                y = argument
                x = np.arange(len(y))
            elif argument.ndim == 2:
                n_rows, n_cols = argument.shape
                if n_rows > n_cols:
                    argument = argument.T
                assert argument.shape[1] >= 3, "The input must have at least 3 points"
                x, y = argument[0], argument[1]
        else:
            raise ValueError("There can only be 1 or 2 positional arguments passed to the function")

        # more or less all the algorithms depend on the inputs to be sorted, at least in the x dimension
        # therefore the x and y are sorted together
        if not np.all(np.diff(x) > 0):
            sorted_indices = np.argsort(x)  # sort in the ascending way
            x = x[sorted_indices]
            y = y[sorted_indices]
            assert np.all(np.diff(x))
        # all the methods should work no matter the scale of the data
        # therefore the input 2D space is transformed in [0, 1]x[0, 1] square
        x = normalize(x)
        y = normalize(y)

        # optionally smooth out the data using cubic splines (custom implementation, no external libs)
        smoothing = kwargs.get("smoothing", 0.0)
        assert smoothing >= 0.0
        if smoothing > 0:
            x, y = cubic_spline_smoothing(x, y, smoothing)
        return f(x, y, **kwargs)

    return inner


def normalize(x):
    """
    Helper function for normalizing the inputs.
    Normalization is an affine transformation such that the minimal element of x maps to 0, and maximal element of x
    maps to 1
    Args:
        x: npt.NDArray, the array to be normalized

    Returns: npt.NDArray, a normalized array such that the minimum is 0 and the maximum is 1

    """
    return (x - x.min()) / (x.max() - x.min())


def get_delta_matrix(h):
    """
    [h1, h2, h3, h4] ->
    [[1/h1   -1/h1-1/h2      1/h2           0         0]
    [  0       1/h2      -1/h2-1/h3        0         0]
    [  0      0             1/h3      -1/h3-1/h4   1/h4]]
    Args:
        h:

    Returns:

    """
    assert h.ndim == 1
    n = len(h)
    dest = np.zeros((n - 1, n + 1))
    np.fill_diagonal(dest, 1 / h[:-1])
    np.fill_diagonal(dest[:, 1:], -1 / h[1:])  # heh indexing trick
    dest -= np.roll(dest, 1, axis=1)
    return dest


def get_weight_matrix(h):
    """

    Args:
        h:

    Returns:

    """
    assert h.ndim == 1
    n = len(h)
    out = np.zeros((n - 1, n - 1))
    np.fill_diagonal(out, (h[:-1] + h[1:]) / 3.0)  # main diagonal
    np.fill_diagonal(out[:, 1:], h[1:] / 6.0)  # upper diagonal
    np.fill_diagonal(out[1:, :], h[1:] / 6.0)  # lower diagonal
    return out


def cubic_spline_smoothing(x, y, smoothing_factor=0):
    h = np.diff(x)
    delta = get_delta_matrix(h)
    weight = get_weight_matrix(h)
    # equivalent to 'delta.T @ np.inv(weight) @ delta', just both numerically more stable and faster
    matrix = delta.T @ la.solve(weight, delta)
    smoothed_y = la.solve(np.identity(len(y)) + smoothing_factor * matrix, y)
    return x, smoothed_y


def projection_distance(vertices):
    """
    Return the projection distance of the point P1 to the line through both P2 and the origin.
    Args:
        vertices: np.ndarray of dimensions (..., 2, 2), coordinates of the points such that vertices[0] are the
        coordinates of the point we wish to project on a line defined with the origin and vertices[1]

    Returns: distances, np.ndarray, one dimensional array denoting the distance the point vertices[0] must travel to be
    projected onto the line defined by vertices[1] and the origin
    """
    # vertices is of shape (..., 2, 2)
    assert vertices.ndim >= 2
    assert vertices.shape[-2:] == (2, 2)
    determinants = np.abs(la.det(vertices))  # this is of shape (...), the last two are not existent anymore
    vectors = vertices[..., 1, :]  # select the second row of all the matrices. this is of shape (..., 2)
    lengths = la.norm(vectors, ord=2, axis=-1)  # this is of shape (...)
    distances = determinants / lengths
    return distances
