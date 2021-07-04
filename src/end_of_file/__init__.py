import logging
import re
import click
from pathlib import Path
from typing import List, Generator, Optional, Callable, TextIO
import os
import subprocess


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("eof")
logger.setLevel(logging.INFO)


def get_git_files(path: Path) -> List[Path]:
    result = subprocess.run(["git", "ls-files"], stdout=subprocess.PIPE, cwd=path)
    if result.returncode != 0:
        raise Exception("Could not get git to return files.")

    rows = result.stdout.decode().strip().split("\n")
    return list(map(lambda row: path.joinpath(row), rows))


def walker(
    path: Path,
    with_hidden: bool,
) -> Generator[Path, None, None]:
    for root, dirs, files in os.walk(path):
        if not with_hidden:
            files = [f for f in files if not f[0] == "."]
            dirs[:] = [d for d in dirs if not d[0] == "."]

        for name in files:
            yield Path(root).joinpath(name)


def validate_extensions(ctx, param, value) -> List[str]:
    if not value:
        return value

    regex = r"^[a-zA-Z0-9,]+$"
    if not re.match(regex, value):
        raise click.BadParameter(
            f"Extensions parameter must match following regex: '{regex}', got '{value}'."
        )

    return value.split(",")


def bruteforce(path: Path) -> bool:
    try:
        with open(path, "r") as f:
            f.readline()
            return True

    except UnicodeDecodeError:
        return False


def mimetype(path: Path) -> bool:
    import mimetypes

    mimetype, encoding = mimetypes.guess_type(path)
    return mimetype and mimetype.startswith("text")


def format_file(filepath: Path, check: bool) -> bool:
    with open(filepath, "r+") as f:
        content = f.read()

        if not content:
            return True

        count = 0
        for tail in reversed(content):
            if tail in ["\n", " ", "\t"]:
                count += 1

            else:
                break

        if count == 1:
            return True

        if check:
            return False

        elif count == 0:
            f.write("\n")
            return False

        elif count > 1:
            f.seek(len(content) - count)
            f.truncate()
            f.write("\n")
            return False

        else:
            raise Exception(f"No idea what happened, count: '{count}'.")


@click.command()
@click.argument(
    "path",
    default=".",
    type=click.Path(exists=True),
)
@click.option(
    "-e",
    "--extensions",
    help="Comma separated list of extensions or nothing",
    callback=validate_extensions,
)
@click.option(
    "-c",
    "--check",
    help="Reports malformatted files and exits with error",
    is_flag=True,
    default=False,
)
@click.option(
    "-s",
    "--strategy",
    help="Strategy used to determine if file is text file in case extensions are not provided",
    type=click.Choice(["bruteforce", "mimetype"], case_sensitive=False),
    default="bruteforce",
    show_default=True,
)
@click.option(
    "-g",
    "--git",
    help="Format only files managed by git (git ls-files)",
    is_flag=True,
)
@click.option(
    "-i",
    "--ignore",
    help="Paths containing provided string are skipped",
    multiple=True,
)
@click.option(
    "-h",
    "--hidden",
    help="Includes also hidden files",
    is_flag=True,
    default=False,
    show_default=True,
)
def format(
    path: Path,
    extensions: Optional[List[str]],
    check: bool,
    strategy: str,
    ignore: List[str],
    hidden: bool,
    git: Optional[bool],
):
    path = Path(path)
    rulebook = RuleBook.factory(
        path,
        extensions,
        strategy,
        ignore,
        git,
    )

    errors = []
    for filepath in walker(path, hidden):
        if not rulebook.is_valid(filepath):
            continue

        logger.info(f"Checking file: '{filepath}'")
        if not format_file(filepath, check):
            errors.append(filepath)

    for error in errors:
        logger.info(f"Found malformatted file '{error}'")

    if check and errors:
        exit(1)


class RuleBook:
    rules: List[Callable[[Path], bool]] = []

    def __init__(self, rules: List[Callable[[Path], bool]]):
        self.rules = rules

    def is_valid(self, path: Path) -> bool:
        return all(rule(path) for rule in self.rules)

    @staticmethod
    def factory(
        path: Path,
        extensions: List[str],
        strategy: str,
        ignore: List[str],
        git: bool,
    ):
        rules: List[Callable[[Path], bool]] = []

        rules.append(lambda p: all(i not in str(p) for i in ignore))

        if extensions:
            rules.append(lambda path: path.suffix[1:] in extensions)

        if strategy == "bruteforce":
            rules.append(bruteforce)

        if strategy == "mimetype":
            rules.append(mimetype)

        if git:
            git_paths = get_git_files(path)
            rules.append(lambda p: p in git_paths)

        return RuleBook(rules)


if __name__ == "__main__":
    format()
