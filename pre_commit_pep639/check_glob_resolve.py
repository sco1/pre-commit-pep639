import argparse
import sys
import tomllib
from collections import abc
from pathlib import Path

from pre_commit_pep639.core_utils import extract_metadata_base

CWD = Path()


class UnmatchedGlobError(Exception): ...  # noqa: D101


def get_license_globs(toml_file: Path) -> list[str]:
    """
    Check the provided TOML file its `license-files` field.

    The provided TOML file is assumed to contain a `project` table, which contains a list of glob
    patterns in a `license-files` field.
    """
    with toml_file.open("rb") as f:
        contents = tomllib.load(f)

    base = extract_metadata_base(contents)
    if base is None:
        # Unsupported metadata spec
        return []

    return base.get("license-files", [])  # type: ignore[no-any-return]


def try_glob(glob: str, base_dir: Path = CWD) -> None:
    """
    Check the provided glob pattern for matches relative to the directory containing pyproject.toml.

    If the glob does not match any files, an `UnmatchedGlobError` is raised for downstream handling.
    """
    glob_match = list(base_dir.glob(glob))
    if not glob_match:
        raise UnmatchedGlobError


def main(argv: abc.Sequence[str] | None = None) -> int:  # noqa: D103
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", type=Path)
    args = parser.parse_args(argv)

    ec = 0
    for file in args.filenames:
        # Per PEP 639, globs should be relative to the directory containing pyproject.toml
        # This hook should only be executing for pyproject.toml files, so the assumption can be made
        # here that we should be operating relative to the file's parent.
        base_dir = file.parent

        license_globs = get_license_globs(file)
        if not license_globs:
            continue

        unmatched = []
        for glob in license_globs:
            try:
                try_glob(glob, base_dir=base_dir)
            except UnmatchedGlobError:
                unmatched.append(glob)

        if unmatched:
            print(f"{file}")
            for glob in unmatched:
                print(f"    Unmatched glob: '{glob}'")

            ec = 1

    return ec


if __name__ == "__main__":
    sys.exit(main())
