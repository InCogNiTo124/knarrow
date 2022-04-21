from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from collections import Counter
from functools import partial
from pathlib import Path

from knarrow import find_knee


def gte_0(value):
    x = float(value)
    assert x >= 0.0
    return x


METHODS = [
    "angle",
    "c_method",
    "distance",
    "distance_adjacent",
    "kneedle",
    "menger_anchored",
    "menger_successive",
    "ols_swiping",
]


def get_parser():
    parser = ArgumentParser(prog="knarrow", formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "-m", "--method", choices=(["all"] + METHODS), default="all", help="select the knee searching method"
    )
    parser.add_argument(
        "--sort",
        action="store_true",
        help="sort the values before the knee search. By default is assumes the input is already sorted",
    )
    parser.add_argument("--smoothing", default=0.0, type=gte_0, help="cublic spline smoothing parameter")
    parser.add_argument(
        "-d", "--delimiter", default=None, help="split the values with DELIMITER. If None, split by space"
    )
    parser.add_argument(
        "-o",
        "--output",
        choices=["index", "value"],
        default="index",
        help=(
            "if output is `value`, this will return the row of the input file where the knee was detected. "
            "if output is `index`, the index of that row will be returned"
        ),
    )
    parser.add_argument("files", nargs="*", default=["-"], help="a list of files. STDIN is denoted with `-`.")
    return parser


def cli(method="all", files=None, sort=False, delimiter=None, output=None, smoothing=None):
    for filename in files:
        path = Path("/dev/stdin" if filename == "-" else filename)
        with path.open("r") as file:
            rows = list(map(str.strip, file))
            split = partial(str.split, sep=delimiter)
            values = map(split, rows)
            numbers = list(tuple(float(value) for value in row) for row in values)
            indices = list(range(len(numbers)))
            if sort:
                indices.sort(key=lambda i: numbers[i])
                key_function = (lambda x: x) if len(numbers[0]) == 1 else (lambda x: x[0])
                numbers.sort(key=key_function)

            if method == "all":
                counter = Counter([find_knee(numbers, method=m, sort=False, smoothing=smoothing) for m in METHODS])
                most_common = counter.most_common(1).pop(0)
                knee = most_common[0]
            else:
                knee = find_knee(numbers, method=method, sort=False, smoothing=smoothing)

            result = indices[knee] if output == "index" else rows[indices[knee]]
            print(path.name, result)
    return


def main():
    parser = get_parser()
    args = vars(parser.parse_args())
    exit(cli(**args))


if __name__ == "__main__":
    main()
