import numpy as np

TOLERANCE = 1e-5


def f(x, c):
    return x * (np.exp(c) + 1) / (x * np.exp(c) + 1)


def df_dc(x, c):
    t = x * np.exp(c)
    return (x - 1) * t / (t + 1) ** 2


def d2f_dc2(x, c):
    t = x * np.exp(c)
    return (x - 1) * x * np.exp(c) * (t - 1) / (t + 1) ** 3


def de_dc(y, x, c):
    return np.mean((f(x, c) - y) * df_dc(x, c))


def d2e_dc2(y, x, c):
    return np.mean(df_dc(x, c) + (f(x, c) - y) * d2f_dc2(x, c))


def newton_raphson(x, y):
    c = 0
    new_c = 3
    while abs(new_c - c) > TOLERANCE:
        c = new_c
        new_c = c - de_dc(y, x, c) / d2e_dc2(y, x, c)
    return new_c


def get_knee(c):
    return (np.sqrt(1 + np.exp(c)) - 1) / np.exp(c)


def c_method(x, y, **kwargs):
    assert len(kwargs) == 0
    best_c = newton_raphson(x, y)
    knee = get_knee(best_c)

    # the knee is a real number between 0 and 1 which is the best theoretical knee
    # however, that number most likely does not exist in the x array, so the closest is found
    best_knee = np.argmin(np.abs(x - knee))
    return best_knee.item()
