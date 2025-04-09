from pathlib import Path

import pytest

from pre_commit_pep639.check_glob_resolve import (
    UnmatchedGlobError,
    check_file,
    try_glob,
)


def test_try_glob_literal_successful(tmp_path: Path) -> None:
    (tmp_path / "LICENSE").touch()
    try_glob("LICENSE", base_dir=tmp_path)


def test_try_glob_glob_successful(tmp_path: Path) -> None:
    (tmp_path / "LICENSE").touch()
    try_glob("LICEN[CS]E*", base_dir=tmp_path)


def test_try_glob_no_match_raises(tmp_path: Path) -> None:
    with pytest.raises(UnmatchedGlobError):
        try_glob("LICENSE", base_dir=tmp_path)


SAMPLE_GLOB_SINGLE = """\
[project]
license-files = ["LICENSE"]
"""

NO_LICENSE_FILE_FIELD = """\
[project]
"""


def test_file_pipeline_successful(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    toml_file = tmp_path / "pyproject.toml"
    toml_file.write_text(SAMPLE_GLOB_SINGLE)
    (tmp_path / "LICENSE").touch()

    res = check_file(toml_file)
    assert res is False

    captured = capsys.readouterr()
    assert not captured.out


def test_file_pipeline_passthrough(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    toml_file = tmp_path / "pyproject.toml"
    toml_file.write_text(NO_LICENSE_FILE_FIELD)
    (tmp_path / "LICENSE").touch()

    res = check_file(toml_file)
    assert res is False

    captured = capsys.readouterr()
    assert not captured.out


def test_file_pipeline_raised(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    toml_file = tmp_path / "pyproject.toml"
    toml_file.write_text(SAMPLE_GLOB_SINGLE)

    res = check_file(toml_file)
    assert res is True

    captured = capsys.readouterr()
    assert "Unmatched glob: 'LICENSE'" in captured.out
