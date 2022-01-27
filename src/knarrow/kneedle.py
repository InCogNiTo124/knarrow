import numpy as np


def kneedle(x, y, **kwargs):
    """
    Kneedle method from https://doi.org/10.1109/ICDCSW.2011.20

    Args:
        x (``np.ndarray``): the :math:`x` coordinates of the points
        y (``np.ndarray``):  the :math:`y` coordinates of the points
        **kwargs:

    Returns:
        ``int``: the index of the knee
    """
    n = len(x)
    s = kwargs.get("S", 1.0)
    # Steps 1 and 2 from the paper are already performed
    # Step 3
    y_d = y - x

    # Step 4
    local_maxima_indices = ((y_d[1:-1] > y_d[:-2]) & (y_d[1:-1] > y_d[2:])).nonzero()[0] + 1  # len() >= 2
    if len(local_maxima_indices) == 1:
        return local_maxima_indices[0].item()
    x_lmx = x[local_maxima_indices]
    y_lmx = y_d[local_maxima_indices]
    # print(local_maxima_indices)

    # Step 5
    # The original paper states the following equation:
    # $\sum_{i=1}^{n-1}{\left(x_{sn_{i+1}}-x_{sn_i}\right)}$
    # where $x_sn$ is a vector of numbers scaled so that $min(x_sn) = 0$ and $max(x_sn) = 1$
    # If you **really** think about that, that sum will _always_ equal to 1
    t = y_lmx - s / (n - 1)
    # print(t)

    # Step 6
    # Fancy numpy tricks:
    # 1. broadcasting to build (threshold x values) bool matrix denoting when the y_d value drops below the threshold
    # 2. clever use of np.argpartition to get the indices of the earliest True per row
    below_threshold_mask = x_lmx[:, np.newaxis] < x  # shape == (len(x_lmx), n)
    below_threshold_mask &= t[:, np.newaxis] > y_d
    # print(below_threshold_mask)
    under_threshold_ix = np.argpartition(~below_threshold_mask, 0)[:, 0]

    # filter the local maxima
    local_maxima_indices_augmented = np.append(local_maxima_indices, n)
    maxima_mask = (local_maxima_indices_augmented[:-1] < under_threshold_ix) & (
        under_threshold_ix < local_maxima_indices_augmented[1:]
    )
    final_maxima = local_maxima_indices[maxima_mask]
    print("lmi", local_maxima_indices, ", fm", final_maxima)
    print(type(final_maxima), final_maxima.dtype)
    return final_maxima[0].item() + 1
