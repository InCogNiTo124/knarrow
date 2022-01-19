import numpy as np

TOLERANCE = 1e-5


def f(x, c):
    """
    The knee curve.

    This function is being fitted to the input data by tweaking the `c` parameter.

    Args:
        x: `np.ndarray`, the `x` coordinates
        c: `float`, the shape parameter

    Returns: `np.ndarray`, the values of the function evaluated at the `x` w.r.t. `c`

    """
    return x * (np.exp(c) + 1) / (x * np.exp(c) + 1)


def df_dc(x, c):
    """
    The first derivative of the knee curve `f(x)` w.r.t x, conditioned on `c`.

    Args:
        x: `np.ndarray`, the `x` coordinates
        c: `float`, the shape parameter

    Returns: `np.ndarray`, values of the slopes of tangents on `f(x)` at `x`

    """
    t = x * np.exp(c)
    return (x - 1) * t / (t + 1) ** 2


def d2f_dc2(x, c):
    """
    The second derivative of the knee curve `f(x)` w.r.t x, conditioned on `c`.

    Args:
        x: `np.ndarray`, the `x` coordinates
        c: `float`, the shape parameter

    Returns: `np.ndarray`, values of the second derivative of `f(x)` at `x`

    """
    t = x * np.exp(c)
    return (x - 1) * x * np.exp(c) * (t - 1) / (t + 1) ** 3


def de_dc(y, x, c):
    """
    The first derivative of the energy function `E(x)` w.r.t `c`.

    Used in Newton-Raphson method for the optimization of the shape parameter `c`.

    Args:
        y: `np.ndarray`, the ground truth function values we wish to fit the knee curve `f(x)` on
        x: `np.ndarray`, the `x` coordinates
        c: `float`, the shape parameter

    Returns: `np.ndarray`, values of the first derivative of `E(x)` at `x`
    """
    return np.mean((f(x, c) - y) * df_dc(x, c))


def d2e_dc2(y, x, c):
    """
    The second derivative of the energy function `E(x)` w.r.t `c`.

    Used in Newton-Raphson method for the optimization of the shape parameter `c`.

    Args:
        y: `np.ndarray`, the ground truth function values we wish to fit the knee curve `f(x)` on
        x: `np.ndarray`, the `x` coordinates
        c: `float`, the shape parameter

    Returns: `np.ndarray`, values of the second derivative of `E(x)` at `x`
    """
    return np.mean(df_dc(x, c) + (f(x, c) - y) * d2f_dc2(x, c))


def newton_raphson(x, y):
    """
    The implementation of the [Newton-Raphson](https://en.wikipedia.org/wiki/Newton%27s_method) optimization procedure.
    It fits the knee curve `f(x)` to the `y` s of the corresponding `x` s by tweaking the shape parameter `c` from an
    initial guess.

    Args:
        x: `np.ndarray`, the ground truth `x` coordinates
        y: `np.ndarray`, the ground truth `y` coordinates

    Returns: `float`, the optimal shape parameter `c` which minimizes the squared error, up to a predefined tolerance level
    """
    c = 0
    new_c = 3
    while abs(new_c - c) > TOLERANCE:
        c = new_c
        new_c = c - de_dc(y, x, c) / d2e_dc2(y, x, c)
    return new_c


def get_knee(c):
    """
    Calculates the position of the point of maximal curvature.

    The position depends solely on the shape parameter `c`.

    Args:
        c: `float`, the shape parameter

    Returns: `float`, the `x` position where the knee curve `f(x)` is most curved

    """
    return (np.sqrt(1 + np.exp(c)) - 1) / np.exp(c)


def c_method(x, y, **kwargs):
    """
    Implements the C-method as described in https://blog.msmetko.xyz/posts/2

    Args:
        x: `np.ndarray`, the ground truth `x` coordinates
        y: `np.ndarray`, the ground truth `y` coordinates
        **kwargs: `dict`, optional arguments (should be empty)

    Returns:

    """
    assert len(kwargs) == 0
    best_c = newton_raphson(x, y)
    knee = get_knee(best_c)

    # the knee is a real number between 0 and 1 which is the best theoretical knee
    # however, that number most likely does not exist in the x array, so the closest is found
    best_knee = np.argmin(np.abs(x - knee))
    return best_knee.item()
