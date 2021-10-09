from knarrow.util import np_windowed, scale
import numpy as np
import numpy.typing as npt
import pytest


@pytest.mark.parametrize(
    "length,w,s,d,target",
    [
        (7, 3, 1, 1, np.array([[0, 1, 2], [1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6]])),
        (7, 4, 1, 1, np.array([[0, 1, 2, 3], [1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6]])),
        (7, 3, 2, 1, np.array([[0, 1, 2], [2, 3, 4], [4, 5, 6]])),
        (7, 4, 2, 1, np.array([[0, 1, 2, 3], [2, 3, 4, 5]])),
        (7, 3, 1, 2, np.array([[0, 2, 4], [1, 3, 5], [2, 4, 6]])),
        (7, 3, 2, 2, np.array([[0, 2, 4], [2, 4, 6]])),
    ],
)
def test_np_widowed(length: int, w: int, s: int, d: int, target: npt.NDArray[np.int_]) -> None:
    output = np_windowed(length, w, s, d)
    assert output.shape == target.shape, output
    assert (output == target).all()


def test_scale():
    rng = np.random.default_rng()
    for _ in range(100):
        mean = rng.uniform(-10, 10)
        std = rng.uniform(1, 100)
        length = rng.integers(3, 100_000, 1)
        array = rng.normal(mean, std, length)
        scaled_array = scale(array)
        assert scaled_array.min().item() == 0
        assert scaled_array.max().item() == 1
