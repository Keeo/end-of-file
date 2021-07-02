import logging
import re
import click
from pathlib import Path
from typing import List, Generator, Optional, Callable, TextIO
import os


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("eof")
logger.setLevel(logging.INFO)


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


def build_validator(
    extensions: Optional[List[str]],
    strategy: str,
) -> Callable[[Path], bool]:
    if extensions:
        return lambda path: path.suffix[1:] in extensions

    if strategy == "bruteforce":
        return bruteforce

    if strategy == "mimetype":
        return mimetype

    raise Exception(
        f"Please provide extensions list or valid strategy. Provided extensions: {extensions}, strategy: {strategy}."
    )


def format_file(handle: TextIO, check: bool) -> bool:
    content = handle.read()

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
        handle.write("\n")
        return False

    elif count > 1:
        handle.seek(len(content) - count)
        handle.truncate()
        handle.write("\n")
        return False

    else:
        raise Exception(f"No idea what happened, count: '{count}'.")


@click.command()
@click.option(
    "-p",
    "--path",
    default=Path("."),
    help="Root of the project, folder will be traversed",
    show_default=True,
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
):
    validator = build_validator(extensions, strategy)

    errors = []
    for filepath in walker(path, hidden):
        if not validator(filepath) or any(i in str(filepath) for i in ignore):
            continue

        with open(filepath, "r+") as f:
            logger.info(f"Checking file: '{filepath}'")
            if not format_file(f, check):
                errors.append(filepath)

    for error in errors:
        logger.info(f"Found malformatted file '{error}'")

    if check and errors:
        exit(1)


if __name__ == "__main__":
    format()
