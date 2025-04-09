from pathlib import Path

import pytest

from pre_commit_pep639.check_glob_resolve import UnmatchedGlobError, get_license_globs, try_glob

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


def test_try_glob_literal_successful(tmp_path: Path) -> None:
    (tmp_path / "LICENSE").touch()
    try_glob("LICENSE", base_dir=tmp_path)


def test_try_glob_glob_successful(tmp_path: Path) -> None:
    (tmp_path / "LICENSE").touch()
    try_glob("LICEN[CS]E*", base_dir=tmp_path)


def test_try_glob_no_match_raises(tmp_path: Path) -> None:
    with pytest.raises(UnmatchedGlobError):
        try_glob("LICENSE", base_dir=tmp_path)
