from .angle_method import angle  # noqa
from .c_method import c_method  # noqa
from .distance_method import distance, distance_adjacent  # noqa
from .menger import menger_anchored, menger_successive  # noqa
from .ols import ols_swiping  # noqa
from .util import prepare


@prepare
def find_knee(x, y, method="menger_successive", **kwargs):
    """
    Public method for finding the knee

    Args:
        x: npt.NDArray, the x coordinates of the points
        y: npt.NDArray, the y coordinates of the points
        method: str, denotes the method to be used (default: menger_successive)
        **kwargs: possible additional arguments for the knee-finding method

    Returns: int, the index of the knee
    """
    assert method in [
        "angle",
        "c_method",
        "distance",
        "distance_adjacent",
        "menger_anchored",
        "menger_successive",
        "ols_swiping",
    ]
    function = globals()[method]
    return function(x, y, **kwargs)
