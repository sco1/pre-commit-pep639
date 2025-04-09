from pathlib import Path

import pytest

from pre_commit_pep639.check_glob_syntax import check_file

SAMPLE_GLOB_SINGLE = """\
[project]
license-files = ["LICENSE"]
"""


def test_check_glob_syntax_success(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    toml_file = tmp_path / "pyproject.toml"
    toml_file.write_text(SAMPLE_GLOB_SINGLE)

    res = check_file(toml_file)
    assert res is False

    captured = capsys.readouterr()
    assert not captured.out


SAMPLE_NO_GLOBS = """\
[project]
"""


def test_check_glob_syntax_no_glob_success(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    toml_file = tmp_path / "pyproject.toml"
    toml_file.write_text(SAMPLE_NO_GLOBS)

    res = check_file(toml_file)
    assert res is False

    captured = capsys.readouterr()
    assert not captured.out


SAMPLE_GLOB_LEADING_SLASH = r"""[project]
license-files = [".\\LICENSE"]
"""


def test_check_glob_syntax_leading_slash_fails(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    toml_file = tmp_path / "pyproject.toml"
    toml_file.write_text(SAMPLE_GLOB_LEADING_SLASH)

    res = check_file(toml_file)
    assert res is True

    captured = capsys.readouterr()
    assert "Forward slash" in captured.out


SAMPLE_GLOB_PARENT_DIRECTORY = """\
[project]
license-files = ["../LICENSE"]
"""


def test_check_glob_syntax_parent_directory_fails(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    toml_file = tmp_path / "pyproject.toml"
    toml_file.write_text(SAMPLE_GLOB_PARENT_DIRECTORY)

    res = check_file(toml_file)
    assert res is True

    captured = capsys.readouterr()
    assert "Parent directory" in captured.out


SAMPLE_GLOB_MULTI_ISSUE = r"""[project]
license-files = ["..\\LICENSE"]
"""


def test_check_glob_syntax_multi_issue_fails(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    toml_file = tmp_path / "pyproject.toml"
    toml_file.write_text(SAMPLE_GLOB_MULTI_ISSUE)

    res = check_file(toml_file)
    assert res is True

    captured = capsys.readouterr()
    assert "Forward slash" in captured.out
    assert "Parent directory" in captured.out


SAMPLE_MULTI_GLOB_MIXED_VALID = """\
[project]
license-files = ["AUTHORS*", "../LICENSE"]
"""


def test_check_glob_syntax_mixed_valid(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    toml_file = tmp_path / "pyproject.toml"
    toml_file.write_text(SAMPLE_MULTI_GLOB_MIXED_VALID)

    res = check_file(toml_file)
    assert res is True

    captured = capsys.readouterr()
    assert "../LICENSE" in captured.out
    assert "Parent directory" in captured.out
