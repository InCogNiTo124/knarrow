import numpy as np


def angle(x, y, **kwargs):
    """
    Find a knee by looking at the maximum change of the angle of the line going through consecutive point pairs.

    Quite sensitive to noise, use with cubic spline smoothing.

    Args:
        x (``np.ndarray``): the :math:`x` coordinates of the points
        y (``np.ndarray``): the :math:`y` coordinates of the points
        **kwargs: possible additional arguments (none are used)

    Returns:
        ``int``: the index of the knee
    """
    assert len(kwargs) == 0
    assert x.shape == y.shape
    d_x = np.diff(x)
    d_y = np.diff(y)
    angles = np.arctan2(d_y, d_x)
    angle_differences = np.abs(np.diff(angles))
    max_diff = angle_differences.argmax().item()
    return max_diff + 1
