from typer.testing import CliRunner

from knarrow.__about__ import __version__
from knarrow.cli import app

runner = CliRunner()


def test_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert str(__version__) in result.stdout


def test_manual_input():
    # FIXME input does not seem to be working ??
    result = runner.invoke(app, [], input=b"1\n2\n3\n5\n")
    assert result.exit_code == 0
    assert result.stdout == "stdin 3"


def test_method():
    # FIXME input does not seem to be working ??
    result = runner.invoke(app, ["--method", "c_method"], input=b"1\n2\n3\n5\n")
    assert result.exit_code == 0
    assert result.stdout == "stdin 3"


def test_sort_input_file():
    result = runner.invoke(app, ["--sort", "--output", "index", "--smoothing", "0.01", "tests/cli/shuf_delim.txt"])
    assert result.exit_code == 0
    assert result.stdout.strip() == "shuf_delim.txt 14"
