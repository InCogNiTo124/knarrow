import numpy as np
from numpy import linalg as la


def r_squared(x, y):
    """
    Fit a linear regression to :math:`y` and return the :math:`R^2` statistical measure of a fit of a linear regression

    Args:
        x (``np.ndarray``): The :math:`x` coordinates of the points
        y (``np.ndarray``): The :math:`y` coordinates of the points

    Returns:
         ``float``: The :math:`R^2` measure of a fit. Bounded by :math:`\\left[0, 1\\right]`. The closer :math:`R^2` is
         to :math:`1`, the better the fit.

    """
    x = x.ravel()
    y = y.ravel()
    assert x.ndim == y.ndim
    assert len(x) == len(y)
    n = len(x)
    xx = np.stack((np.ones(n), x))
    w, ssr, _, _ = la.lstsq(xx.T, y, rcond=None)
    if ssr.size == 0:
        ssr = 0
    sst = np.var(y, ddof=n - 1)
    r2_1 = (1 - ssr / sst).item()
    corr = np.corrcoef(w @ xx, y)[0, 1]
    r2_2 = corr**2
    assert np.allclose(r2_1, r2_2)
    return ((r2_1 + r2_2) / 2).item()


def ols_swiping(x, y, **kwargs):
    """
    Performs OLS swiping method.

    By first selecting a pivot point, all the data points are implicitly split into two parts: the left one and the
    right one. Then, the algorithm regresses a line onto :math:`y` with respect to :math:`x` for both parts using
    ordinary least squares. If both lines fit quite well, meaning the :math:`R^2` for both left and the right fit is
    particularly high, the pivot point is declared as a knee.

    Args:
        x (``np.ndarray``): the :math:`x` coordinates of the points
        y (``np.ndarray``): the :math:`y` coordinates of the points
        **kwargs: possible additional arguments (none are used)

    Returns:
        ``int``: the index of the knee
    """
    assert len(kwargs) == 0
    n = len(x)
    # some python magic
    # generator of all the splits, linear regressions and the sums of particular r2 coefficients
    results = ((i, r_squared(x[: i + 1], y[: i + 1]) + r_squared(x[i:], y[i:])) for i in range(1, n - 1))
    # the values are only calculated as the generator is consumed :))
    return min(results, key=lambda t: t[1])[0]
