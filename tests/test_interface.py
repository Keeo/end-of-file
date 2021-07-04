import os
from dataclasses import dataclass
from functools import reduce
from pathlib import Path
from typing import List, Tuple, Dict

import pytest
from click.testing import CliRunner
from src.end_of_file import format
from tests.utils import write, assert_content


@pytest.fixture
def runner():
    return CliRunner()


@dataclass
class Content:
    value: str
    result: str
    exit_code: int
    type: str


@pytest.fixture
def contents() -> Dict[str, List[Content]]:
    options = [
        Content("ddsa\n fdsa fds\n.\n", "ddsa\n fdsa fds\n.\n", 0, "correct"),
        Content("dsadsa\n.", "dsadsa\n.\n", 1, "missing"),
        Content("dsa  \ndsa\n\n\n   \n\n", "dsa  \ndsa\n", 1, "extra"),
        Content("", "", 0, "empty"),
    ]

    return reduce(
        lambda acc, curr: acc.setdefault(curr.type, list()).append(curr) or acc,
        options,
        dict(),
    )


def test_interface(tmp_path: Path, runner, contents: Dict[str, List[Content]]):
    for lists in contents.values():
        for content in lists:

            with open(tmp_path.joinpath("sample.txt"), "w") as f:
                f.write(content.value)

            result = runner.invoke(format, [str(tmp_path), "--check"])
            assert result.exit_code == content.exit_code
            with open(os.path.join(tmp_path, "sample.txt"), "r") as f:
                assert f.read() == content.value

            result = runner.invoke(format, [str(tmp_path)])
            assert result.exit_code == 0
            with open(os.path.join(tmp_path, "sample.txt"), "r") as f:
                assert f.read() == content.result


def test_hidden(tmp_path: Path, runner):
    content = "dsadsa"
    filepath = tmp_path.joinpath(".sample.txt")
    write(filepath, content)

    result = runner.invoke(format, [str(tmp_path), "--check"])
    assert_content(filepath, content)
    assert result.exit_code == 0

    result = runner.invoke(format, [str(tmp_path), "--check", "--hidden"])
    assert_content(filepath, content)
    assert result.exit_code == 1

    result = runner.invoke(format, [str(tmp_path), "--hidden"])
    assert_content(filepath, content + "\n")
    assert result.exit_code == 0


def test_ignore(tmp_path: Path, runner):
    content = "dsadsa"
    filepath = tmp_path.joinpath("sample.txt")
    write(filepath, content)

    result = runner.invoke(format, [str(tmp_path), "-i", "sample"])
    assert_content(filepath, content)
    assert result.exit_code == 0

    result = runner.invoke(format, [str(tmp_path), "-i", "smple", "-i", "dsa"])
    assert_content(filepath, content + "\n")
    assert result.exit_code == 0
