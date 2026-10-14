from typing import Any

import numpy.typing as npt

_METHODS: list[str]

def find_knee(
    x: npt.ArrayLike,
    y: npt.ArrayLike | None = ...,
    method: str = ...,
    **kwargs: Any,
) -> int: ...

def all(
    x: npt.ArrayLike,
    y: npt.ArrayLike | None = ...,
    **kwargs: Any,
) -> int: ...
