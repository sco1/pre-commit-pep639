import tomllib
from pathlib import Path

import pytest

from pre_commit_pep639.core_utils import extract_metadata_base, get_license_globs

SAMPLE_PEP_621_TOML = """\
[project]
name = "foo"
version = "1.0.0"
"""


def test_extract_621_base() -> None:
    contents = tomllib.loads(SAMPLE_PEP_621_TOML)
    truth_base = {"name": "foo", "version": "1.0.0"}

    assert extract_metadata_base(contents) == truth_base


SAMPLE_POETRY_TOML = """\
[tool.poetry]
name = "bar"
version = "2.0.0"
"""


def test_extract_poetry_base() -> None:
    contents = tomllib.loads(SAMPLE_POETRY_TOML)
    truth_base = {"name": "bar", "version": "2.0.0"}

    assert extract_metadata_base(contents) == truth_base


SAMPLE_GLOB_SINGLE = """\
[project]
license-files = ["LICENSE"]
"""

SAMPLE_GLOB_MULTI = """\
[project]
license-files = ["LICEN[CS]E*", "AUTHORS.md"]
"""

NO_LICENSE_FILE_FIELD = """\
[project]
"""

UNKNOWN_METADATA_TABLE = """\
[dingdong]
license-files = ["LICENSE"]
"""


GET_GLOB_CASES: tuple[tuple[str, list[str]], ...] = (
    (SAMPLE_GLOB_SINGLE, ["LICENSE"]),
    (SAMPLE_GLOB_MULTI, ["LICEN[CS]E*", "AUTHORS.md"]),
    (NO_LICENSE_FILE_FIELD, []),
    (UNKNOWN_METADATA_TABLE, []),
)


@pytest.mark.parametrize(("toml_data", "truth_globs"), GET_GLOB_CASES)
def test_get_license_globs(toml_data: str, truth_globs: list[str], tmp_path: Path) -> None:
    toml_file = tmp_path / "pyproject.toml"
    toml_file.write_text(toml_data)

    assert get_license_globs(toml_file) == truth_globs
