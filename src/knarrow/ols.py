import numpy as np
from numpy import linalg as la


def r_squared(x, y):
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
    r2_2 = corr ** 2
    assert np.allclose(r2_1, r2_2)
    return ((r2_1 + r2_2) / 2).item()


def ols_swiping(x, y, **kwargs):
    assert len(kwargs) == 0
    n = len(x)
    # some python magic
    # generator of all the splits, linear regressions and the sums of particular r2 coefficients
    results = ((i, r_squared(x[: i + 1], y[: i + 1]) + r_squared(x[i:], y[i:])) for i in range(1, n - 1))
    # the values are only calculated as the generator is consumed :))
    return min(results, key=lambda t: t[1])[0]
