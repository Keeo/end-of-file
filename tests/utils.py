from pathlib import Path
from typing import Union


def assert_content(path: Path, content: Union[str, bytes], mode="r"):
    with open(path, mode) as f:
        assert f.read() == content


def write(path: Path, content: Union[str, bytes], mode="w"):
    with open(path, mode) as f:
        f.write(content)


def read(path: Path, mode="r") -> Union[str, bytes]:
    with open(path, mode) as f:
        return f.read()
