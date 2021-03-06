import enum
from typing import Any, Callable, Tuple

import numpy as np
import numpy.typing as npt

class KneeType(enum.Enum):
    DECREASING_CONVEX = 0
    INCREASING_CONCAVE = 1
    DECREASING_CONCAVE = 2
    INCREASING_CONVEX = 3

def np_windowed(length: int, window_size: int, stride: int = 1, dilation: int = 1) -> npt.NDArray[np.int_]: ...
def np_anchored(length: int) -> npt.NDArray[np.int_]: ...
def prepare(f: Callable[[Any], int]) -> int: ...
def normalize(x: npt.NDArray[np.float_]) -> npt.NDArray[np.float_]: ...
def get_delta_matrix(x: npt.NDArray[np.float_]) -> npt.NDArray[np.float_]: ...
def get_weight_matrix(x: npt.NDArray[np.float_]) -> npt.NDArray[np.float_]: ...
def cubic_spline_smoothing(
    x: npt.NDArray[np.float_], y: npt.NDArray[np.float_], smoothing_factor: float
) -> Tuple[npt.NDArray[np.float_], npt.NDArray[np.float_]]: ...
def projection_distance(vertices: npt.NDArray[np.float_]) -> npt.NDArray[np.float_]: ...
def detect_knee_type(y1: float, y2: float, y3: float, y4: float) -> KneeType: ...
