from collections import Counter

from .angle_method import angle  # noqa
from .c_method import c_method  # noqa
from .distance_method import distance, distance_adjacent  # noqa
from .kneedle import kneedle  # noqa
from .menger import menger_anchored, menger_successive  # noqa
from .ols import ols_swiping  # noqa
from .util import prepare

_METHODS = [
    "angle",
    "c_method",
    "distance",
    "distance_adjacent",
    "kneedle",
    "menger_anchored",
    "menger_successive",
    "ols_swiping",
]


@prepare
def find_knee(x, y, method="menger_successive", **kwargs):
    """
    Public method for finding the knee

    Args:
        x (``np.ndarray``): the x coordinates of the points
        y (``np.ndarray``): the y coordinates of the points
        method: `str`, denotes the method to be used (default: menger_successive)
        **kwargs: possible additional arguments for the knee-finding method

    Returns (``int``): the index of the knee
    """
    assert method in _METHODS + ["all"]
    if method == "all":
        return all(x, y, **kwargs)
    function = globals()[method]
    return function(x, y, **kwargs)


@prepare
def all(x, y, **kwargs):
    """
    Find the knee by running all available methods and returning the most-voted result.

    Each method casts a vote for a knee index; the index with the most votes wins.
    Ties are broken by the natural ordering of `collections.Counter.most_common`.

    Args:
        x (``np.ndarray``): the x coordinates of the points
        y (``np.ndarray``): the y coordinates of the points
        **kwargs: additional arguments forwarded to every individual method

    Returns (``int``): the index of the knee
    """
    votes = Counter(
        globals()[m](x, y, **kwargs)
        for m in _METHODS
    )
    return votes.most_common(1)[0][0]
