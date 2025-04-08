import argparse
import sys
import tomllib
from collections import abc
from pathlib import Path

from pre_commit_pep639.core_utils import extract_metadata_base


class LicenseClassifierError(Exception): ...  # noqa: D101


def find_license_classifiers(toml_file: Path) -> None:
    """
    Check the provided TOML file for the presence of a `License :: ...` classifier.

    Two metadata specifications types are currently supported:
        * PEP621 compliant: The provided TOML file is assumed to contain a `project` table, which
        contains a list of PyPI classifiers in the `classifiers` field.
        * Poetry: The provided TOML file is assumed to contain a `tools.poetry` table, which
        contains a list of PyPI classifiers in the `classifiers` field.
    """
    with toml_file.open("rb") as f:
        contents = tomllib.load(f)

    base = extract_metadata_base(contents)
    if base is None:
        # Unsupported metadata spec
        return

    classifiers = base.get("classifiers", None)
    if classifiers is None:
        # No classifiers found
        return

    for c in classifiers:
        if c.startswith("License ::"):
            raise LicenseClassifierError()


def main(argv: abc.Sequence[str] | None = None) -> int:  # noqa: D103
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", type=Path)
    args = parser.parse_args(argv)

    ec = 0
    for file in args.filenames:
        try:
            find_license_classifiers(file)
        except LicenseClassifierError:
            print(f"{file}: License classifier found in project metadata")
            ec = 1

    return ec


if __name__ == "__main__":
    sys.exit(main())
