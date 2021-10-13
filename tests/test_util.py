from knarrow.util import normalize, np_windowed, projection_distance
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
        scaled_array = normalize(array)
        assert scaled_array.min().item() == 0
        assert scaled_array.max().item() == 1


@pytest.mark.parametrize(
    "x, target",
    [
        (np.array([[0.0, 1.0], [1.0, 1.0]]), np.sqrt(2) / 2),
        # for the test cases below I played with GeoGebra
        (np.array([[1.29988207, 2.92713209], [4.9468562479, 1.60558047]]), 2.38286757),
        # test simultaneous multi input
        # It may be a good idea to add more tests to thoroughly test the output shapes
        # I just can't be bothered now tho
        (
            np.array(
                [
                    [[-0.25039962, 1.453093749], [-1.254270565, 2.431550234]],
                    [[-1.3432211549916, -3.502724810702], [1.8335856141482, -1.4314467972228]],
                ]
            ),
            np.array([0.443610636, 3.5875659543561]),
        ),
    ],
)
def test_projection_distance(x, target):
    result = projection_distance(x)
    if isinstance(target, np.ndarray):
        assert isinstance(result, np.ndarray)
        assert result.ndim == target.ndim
        assert result.shape == target.shape
    assert np.allclose(result, target)
