from pathlib import Path

import pytest

from pre_commit_pep639.check_classifiers import LicenseClassifierError, find_license_classifiers

SAMPLE_TOML_NO_LICENSE_CLASSIFIER = """\
[project]
name = "hello-world"
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Typing :: Typed",
]
"""


def test_toml_has_classifiers_no_license_passes(tmp_path: Path) -> None:
    toml_file = tmp_path / "pyproject.toml"
    toml_file.write_text(SAMPLE_TOML_NO_LICENSE_CLASSIFIER)

    find_license_classifiers(toml_file)


SAMPLE_TOML_NO_CLASSIFIERS = """\
[project]
name = "hello-world"
"""


def test_toml_has_no_classifiers_passes(tmp_path: Path) -> None:
    toml_file = tmp_path / "pyproject.toml"
    toml_file.write_text(SAMPLE_TOML_NO_CLASSIFIERS)

    find_license_classifiers(toml_file)


SAMPLE_TOML_HAS_LICENSE_CLASSIFIER = """\
[project]
name = "hello-world"
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Typing :: Typed",
]
"""


def test_toml_has_license_classifiers_raises(tmp_path: Path) -> None:
    toml_file = tmp_path / "pyproject.toml"
    toml_file.write_text(SAMPLE_TOML_HAS_LICENSE_CLASSIFIER)

    with pytest.raises(LicenseClassifierError):
        find_license_classifiers(toml_file)


SAMPLE_POETRY_TOML_NO_LICENSE_CLASSIFIER = """\
[tool.poetry]
name = "hello-world"
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Typing :: Typed",
]
"""


def test_poetry_toml_has_classifiers_no_license_passes(tmp_path: Path) -> None:
    toml_file = tmp_path / "pyproject.toml"
    toml_file.write_text(SAMPLE_POETRY_TOML_NO_LICENSE_CLASSIFIER)

    find_license_classifiers(toml_file)


SAMPLE_POETRY_TOML_NO_CLASSIFIERS = """\
[tool.poetry]
name = "hello-world"
"""


def test_poetry_toml_has_no_classifiers_passes(tmp_path: Path) -> None:
    toml_file = tmp_path / "pyproject.toml"
    toml_file.write_text(SAMPLE_POETRY_TOML_NO_CLASSIFIERS)

    find_license_classifiers(toml_file)


SAMPLE_POETRY_TOML_HAS_LICENSE_CLASSIFIER = """\
[tool.poetry]
name = "hello-world"
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Typing :: Typed",
]
"""


def test_poetry_toml_has_license_classifiers_raises(tmp_path: Path) -> None:
    toml_file = tmp_path / "pyproject.toml"
    toml_file.write_text(SAMPLE_POETRY_TOML_HAS_LICENSE_CLASSIFIER)

    with pytest.raises(LicenseClassifierError):
        find_license_classifiers(toml_file)


SAMPLE_TOML_UNSUPPORTED_TOOL = """\
[tool.dingdong]
name = "hello-world"
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Typing :: Typed",
]
"""


def test_toml_unknown_tool_passes(tmp_path: Path) -> None:
    toml_file = tmp_path / "pyproject.toml"
    toml_file.write_text(SAMPLE_TOML_UNSUPPORTED_TOOL)

    find_license_classifiers(toml_file)


SAMPLE_TOML_UNKNOWN_TABLE = """\
[metadata]
name = "hello-world"
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Typing :: Typed",
]
"""


def test_toml_unknown_table_passes(tmp_path: Path) -> None:
    toml_file = tmp_path / "pyproject.toml"
    toml_file.write_text(SAMPLE_TOML_UNKNOWN_TABLE)

    find_license_classifiers(toml_file)
