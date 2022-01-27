import numpy as np

from .util import np_windowed, projection_distance


def distance(x, y, **kwargs):
    """
    Find a knee by finding a point which is most distant from the line :math:`y=x` (after normalizing the inputs)

    Fun fact: *vertical* distance of a point P from line :math:`y=x` is just a scaled version of the *orthogonal*
    distance of the same point P from line :math:`y=x`.

    Args:
        x (``np.ndarray``): the :math:`x` coordinates of the points
        y (``np.ndarray``): the :math:`y` coordinates of the points
        **kwargs: possible additional arguments (none are actually used)

    Returns:
        ``int``: the index of the knee
    """
    assert len(kwargs) == 0
    assert x.shape == y.shape
    distances = abs(y - x)
    return np.argmax(distances).item()


def distance_adjacent(x, y, **kwargs):
    """
    Find a knee by finding a point which is most distant from the line going through the neighbouring points.

    This method is quite sensitive to noise, so only use with cubic spline smoothing.

    Note: I developed a (somewhat) fancy linear algebra implementation so this should be quite fast.

    Args:
        x (``np.ndarray``): the :math:`x` coordinates of the points
        y (``np.ndarray``): the :math:`y` coordinates of the points
        **kwargs: possible additional arguments (none are actually used)

    Returns:
        ``int``: the index of the knee
    """
    assert len(kwargs) == 0
    indices = np_windowed(len(x), 3)
    x_windowed = x[indices]  # shape = (len(x), 3)
    y_windowed = y[indices]  # shape = (len(x), 3)
    points = np.stack((x_windowed, y_windowed), axis=-1)  # shape = (len(x), 3, 2)
    translated_points = points - points[:, [0], :]  # anchor all the triplets at the origin. The list is important!
    translated_points = translated_points[..., 1:, :]  # remove the origin po``int``, now shape = (len(x), 2, 2)
    distances = projection_distance(translated_points)
    return np.argmax(distances).item()
