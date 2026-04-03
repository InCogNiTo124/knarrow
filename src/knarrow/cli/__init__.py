# SPDX-FileCopyrightText: 2021-present InCogNiTo124 <msmetko@msmetko.xyz>
#
# SPDX-License-Identifier: Apache-2.0

import enum
from functools import partial
from pathlib import Path
import sys
from typing import List, Optional

try:
    import typer
    from knarrow import find_knee
    from knarrow.main import _METHODS
except ImportError:
    print("Please install 'knarrow[cli]' to use this command.")
    sys.exit(1)


from ..__about__ import __version__


# Build enum members: ALL + one per method (uppercased)
_method_members = {"ALL": "all", **{m.upper(): m for m in _METHODS}}
Method = enum.Enum("Method", _method_members, type=str)


class Output(str, enum.Enum):
    INDEX = "index"
    VALUE = "value"


app = typer.Typer()


def stdin_callback(value: Optional[Path]) -> List[Path]:
    return value if value else [Path("/dev/stdin")]


def version_callback(value: bool) -> None:
    if value:
        print(f"knarrow v{__version__}\nType `knarrow --help` for further info.")
        raise typer.Exit(0)


@app.command()
def main(
    method: Method = typer.Option(
        "all", help="The method to use to calculate the knee's position"
    ),
    files: List[Path] = typer.Argument(
        allow_dash=True,
        exists=True,
        dir_okay=False,
        readable=True,
        help="List of input files (default: stdin)",
        show_default=False,
    ),
    sort: bool = typer.Option(False, help="Whether or not to sort the input"),
    delimiter: str = typer.Option(
        ",",
        help="If the input is 2-dimensional, split the dimensions by this option's value",
    ),
    output: Output = typer.Option(
        "value",
        help="Type of output. Value means value itself, index means it's ordinal number",
    ),
    smoothing: float = typer.Option(
        0.0, min=0.0, help="Cubic spline smoothing parameter"
    ),
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
    ),  # version boilerplate
):
    for path in files:
        file = sys.stdin if str(path) == "-" else path.open("r")
        with file:
            rows = list(map(str.strip, file))
            split = partial(str.split, sep=delimiter)
            values = map(split, rows)
            numbers = list(tuple(float(value) for value in row) for row in values)
            indices = list(range(len(numbers)))
            if sort:
                indices.sort(key=lambda i: numbers[i])
                key_function = (
                    (lambda x: x) if len(numbers[0]) == 1 else (lambda x: x[0])
                )
                numbers.sort(key=key_function)

            if method == Method.ALL:
                knee = find_knee(numbers, method="all", sort=sort, smoothing=smoothing)
            else:
                knee = find_knee(
                    numbers, method=method.value, sort=sort, smoothing=smoothing
                )

            result = indices[knee] if output == Output.INDEX else rows[indices[knee]]
            print(file.name if str(path) == "-" else path.name, result)
    return
