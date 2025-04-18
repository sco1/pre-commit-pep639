import argparse
import sys
from collections import abc
from pathlib import Path

from pre_commit_pep639.core_utils import get_license_globs

CWD = Path()


class UnmatchedGlobError(Exception): ...  # noqa: D101


def try_glob(glob: str, base_dir: Path = CWD) -> None:
    """
    Check the provided glob pattern for matches relative to the directory containing pyproject.toml.

    If the glob does not match any files, an `UnmatchedGlobError` is raised for downstream handling.
    """
    glob_match = list(base_dir.glob(glob))
    if not glob_match:
        raise UnmatchedGlobError


def check_file(toml_file: Path) -> bool:
    """
    Helper processing pipeline for a `pyproject.toml` file.

    Returns `True` and emits warning(s) if an unmatched glob is detected, otherwise returns `False`.
    """
    # Per PEP 639, globs should be relative to the directory containing pyproject.toml
    # This hook should only be executing for pyproject.toml files, so the assumption can be made
    # here that we should be operating relative to the file's parent.
    base_dir = toml_file.parent

    license_globs = get_license_globs(toml_file)
    if not license_globs:
        return False

    unmatched = []
    for glob in license_globs:
        try:
            try_glob(glob, base_dir=base_dir)
        except UnmatchedGlobError:
            unmatched.append(glob)

    if unmatched:
        print(f"{toml_file}")
        for glob in unmatched:
            print(f"    Unmatched glob: '{glob}'")

        return True
    else:
        return False


def main(argv: abc.Sequence[str] | None = None) -> int:  # noqa: D103
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", type=Path)
    args = parser.parse_args(argv)

    ec = 0
    for file in args.filenames:
        raised_error = check_file(file)
        if raised_error:
            ec = 1

    return ec


if __name__ == "__main__":
    sys.exit(main())
