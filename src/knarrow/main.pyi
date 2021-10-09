from typing import Any

import numpy as np
from numpy import typing as npt

def double_triangle_area(vertices: npt.NDArray[np.float_]) -> npt.NDArray[np.float_]: ...
def get_squared_vector_lengths(vertices: npt.NDArray[np.float_]) -> npt.NDArray[np.float_]: ...
def get_curvature(vertices: npt.NDArray[np.float_]) -> npt.NDArray[np.float_]: ...
def menger_successive(x: npt.NDArray[np.float_], y: npt.NDArray[np.float_], kwargs: Any) -> int: ...
def angle(x: npt.NDArray[np.float_], y: npt.NDArray[np.float_], kwargs: Any) -> int: ...
def distance_vert(x: npt.NDArray[np.float_], y: npt.NDArray[np.float_], kwargs: Any) -> int: ...
def menger_anchored(x: npt.NDArray[np.float_], y: npt.NDArray[np.float_], kwargs: Any) -> int: ...
def find_knee(x: npt.NDArray[np.float_], y: npt.NDArray[np.float_], method: str, kwargs: Any) -> int: ...
