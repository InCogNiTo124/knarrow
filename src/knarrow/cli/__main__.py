from argparse import ArgumentParser
from collections import Counter
from functools import partial
from pathlib import Path

from knarrow import find_knee

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
    parser = ArgumentParser()
    parser.add_argument("-m", "--method", choices=METHODS + ["all"], default="all")
    parser.add_argument("-s", "--sort", action="store_true")
    parser.add_argument("-d", "--delimiter", default=None)
    parser.add_argument("files", nargs="*", default=["-"])
    return parser


def main(method="all", files=None, sort=False, delimiter=None):
    for filename in files:
        path = Path("/dev/stdin" if filename == "-" else filename)
        with path.open("r") as file:
            split = partial(str.split, sep=delimiter)
            rows = map(split, file)
            numbers = list(tuple(float(value) for value in row) for row in rows)
            if sort:
                key_function = (lambda x: x) if len(numbers[0]) == 1 else (lambda x: x[0])
                numbers = sorted(numbers, key=key_function)

            if method == "all":
                counter = Counter([find_knee(numbers, method=m) for m in METHODS])
                most_common = counter.most_common(1).pop()
                result = most_common[0]
            else:
                result = find_knee(numbers, method=method)
            print(path.name, result)
    return


if __name__ == "__main__":
    parser = get_parser()
    main(**vars(parser.parse_args()))
