from typer.testing import CliRunner

from knarrow.cli import app

runner = CliRunner()


def test_manual_input():
    with open("tests/cli/test.txt") as file:
        text = file.read()
    print(text)
    result = runner.invoke(app, ["-"], input=text)
    assert result.exit_code == 0
    assert result.stdout.strip() == "<stdin> 3"


def test_method():
    result = runner.invoke(app, ["--method", "c_method", "-"], input=b"1\n2\n3\n5\n")
    assert result.exit_code == 0
    assert result.stdout.strip() == "<stdin> 3"


def test_sort_input_file():
    result = runner.invoke(app, ["--sort", "--output", "index", "--smoothing", "0.01", "tests/cli/shuf_delim.txt"])
    assert result.exit_code == 0
    assert result.stdout.strip() == "shuf_delim.txt 14"
