import os
from pathlib import Path
import pytest
from click import BadParameter
from src.end_of_file import (
    validate_extensions,
    walker,
    bruteforce,
    mimetype,
    format_file,
)
from tests.utils import write, read


def test_format_file_no_line(tmp_path: Path):
    bin_path = tmp_path.joinpath("file.txt")
    write(bin_path, "dsadsa")

    assert not format_file(bin_path, True)
    assert not format_file(bin_path, False)
    assert format_file(bin_path, False)
    assert read(bin_path) == "dsadsa\n"


def test_format_file_multiple_lines(tmp_path):
    bin_path = tmp_path.joinpath("file.txt")
    write(bin_path, "dsadsa\t\n\n  \n   \n\t\n")

    assert not format_file(bin_path, True)
    assert not format_file(bin_path, False)
    assert format_file(bin_path, False)
    assert read(bin_path) == "dsadsa\n"


def test_bruteforce(tmp_path: Path):
    bin_path = tmp_path.joinpath("file.bin")

    with open(bin_path, "wb") as f:
        f.write(os.urandom(1024))
    assert not bruteforce(bin_path)

    with open(bin_path, "w") as f:
        f.write("dsadsa")
    assert bruteforce(bin_path)


def test_mimetype(tmp_path: Path):
    bin_path = tmp_path.joinpath("file.txt")
    with open(bin_path, "wb") as f:
        f.write(os.urandom(1024))
    assert mimetype(bin_path)

    bin_path = tmp_path.joinpath("file.bin")
    with open(bin_path, "w") as f:
        f.write("dsadsa")
    assert not mimetype(bin_path)


def test_walker(tmp_path: Path):
    a = tmp_path.joinpath("a.m3")
    b = tmp_path.joinpath("b.fFa")
    a.touch()
    b.touch()
    tmp_path.joinpath(".sample").touch()

    tmp_path.joinpath(".gldsa").mkdir()
    tmp_path.joinpath(".gldsa/file").touch()
    tmp_path.joinpath(".gldsa/.file").touch()

    paths = list(walker(tmp_path, False))
    assert sorted(paths) == sorted([a, b])


def test_validate_extensions():
    result = validate_extensions(None, None, "ext")
    assert result == ["ext"]

    result = validate_extensions(None, None, "ext,ds,md4")
    assert result == ["ext", "ds", "md4"]

    result = validate_extensions(None, None, "")
    assert result == ""

    result = validate_extensions(None, None, None)
    assert result is None

    with pytest.raises(BadParameter):
        validate_extensions(None, None, "ext;md4")

    with pytest.raises(BadParameter):
        validate_extensions(None, None, "e-4")

    with pytest.raises(BadParameter):
        validate_extensions(None, None, ";")
