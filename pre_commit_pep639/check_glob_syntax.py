import argparse
import sys
import typing as t
from collections import abc, defaultdict
from pathlib import Path

from pre_commit_pep639.core_utils import get_license_globs


class InvalidPathDelimiterError(Exception): ...  # noqa: D101


class InvalidParentDirectoryError(Exception): ...  # noqa: D101


EXCEPTION_T: t.TypeAlias = InvalidPathDelimiterError | InvalidParentDirectoryError


def check_file(toml_file: Path) -> bool:
    r"""
    Helper processing pipeline for a `pyproject.toml` file.

    The following syntax issues are currently checked:
        * Presence of leading slash character (`\`) in glob
        * Presence of parent directory indicator (`..`) in glob

    Returns `True` and emits warning(s) if syntax issues are encountered, otherwise returns `False`.
    """
    license_globs = get_license_globs(toml_file)
    if not license_globs:
        return False

    violations: dict[str, list[EXCEPTION_T]] = defaultdict(list)
    for glob in license_globs:
        if "\\" in glob:
            violations[glob].append(InvalidPathDelimiterError())

        if ".." in glob:
            violations[glob].append(InvalidParentDirectoryError())

    if any((v for v in violations.values())):
        print(f"{toml_file}")
        for glob, issues in violations.items():
            for issue in issues:
                if isinstance(issue, InvalidPathDelimiterError):
                    print(f"    Forward slash character in glob: '{glob}'")
                elif isinstance(issue, InvalidParentDirectoryError):  # pragma: no branch
                    print(f"    Parent directory indicator in glob: '{glob}'")

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
