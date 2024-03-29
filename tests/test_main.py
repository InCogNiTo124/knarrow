import numpy as np
import pytest

from knarrow.main import find_knee

ALL_METHODS = [
    "angle",
    "c_method",
    "distance",
    "distance_adjacent",
    "kneedle",
    "menger_anchored",
    "menger_successive",
    "ols_swiping",
]


@pytest.mark.parametrize("method", ALL_METHODS)
@pytest.mark.parametrize(
    "x,target",
    [
        ([1.0, 1.05, 1.15, 1.28, 1.30, 2.5, 3.6, 4.9], 4),
        ((1, 2, 3, 4, 6), 3),
        (np.array([[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 7]]), 4),
        (np.array([[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 7]]), 4),  # same as above just transposed
        (np.array([1, 2, 3, 4, 6]).reshape(-1, 1), 3),
        (np.array([1, 2, 3, 4, 6]).reshape(1, -1), 3),
    ],
)
def test_onevar(method, x, target):
    result = find_knee(x, method=method)
    assert isinstance(result, int)
    assert abs(result - target) <= 1


# im lazy so I copied the inputs from above
# I think I'll need to add more tests soon...
@pytest.mark.parametrize("smoothing", [0.0, 0.001])
@pytest.mark.parametrize("method", ALL_METHODS)
@pytest.mark.parametrize(
    "y,target",
    [
        (np.array([1.0, 1.05, 1.15, 1.28, 1.30, 2.5, 3.6, 4.9]), 4),
        (np.array((1, 2, 3, 4, 6)), 3),
        (np.array([1, 2, 3, 4, 5, 7]), 4),
    ],
)
def test_twovar(smoothing, method, y, target):
    # test normally
    x = np.arange(len(y))
    result = find_knee(x, y, method=method, smoothing=smoothing)
    assert isinstance(result, int)
    assert abs(result - target) <= 1

    # test shuffled
    rng = np.random.default_rng()
    random_indices = rng.choice(x, len(x), replace=False)
    result = find_knee(x[random_indices], y[random_indices], method=method)
    assert isinstance(result, int)
    assert abs(target - result) <= 1


@pytest.mark.xfail(raises=AssertionError)
@pytest.mark.parametrize("method", ALL_METHODS)
@pytest.mark.parametrize(
    "inputs",
    [
        ([[0.0, 1.0]]),
        ([[0.0, 1.0], [0.0, 1.0]]),
        ([[0.0, 1.0, 2.0], [0.0, 1.0, 2.0], [3.0, 4.0, 5.5]]),
        (np.array([[1, 2, 3, 4]]), np.array([[1, 2, 3, 5]])),
        ([0.1, 0.2, 0.3, 0.4, 0.5], [0.2, 0.3, 0.45, 0.60, 1.0, 2.0]),
    ],
)
def test_fails(method, inputs):
    find_knee(*inputs, method=method)
