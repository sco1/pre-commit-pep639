import tomllib
import typing as t
from pathlib import Path


def extract_metadata_base(toml_contents: dict[str, t.Any]) -> dict[str, t.Any] | None:
    """
    Check the provided TOML data for the base metadata table.

    Two metadata specifications types are currently supported:
        * PEP621 compliant: The provided TOML file is assumed to contain a `project` table
        * Poetry: The provided TOML file is assumed to contain a `tools.poetry` table
    """
    if "project" in toml_contents:
        return toml_contents["project"]  # type: ignore[no-any-return]
    elif "tool" in toml_contents:
        if "poetry" in toml_contents["tool"]:
            return toml_contents["tool"]["poetry"]  # type: ignore[no-any-return]
        else:
            # Unsupported metadata specification
            return None
    else:
        # Project metadata could not be found
        return None


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
