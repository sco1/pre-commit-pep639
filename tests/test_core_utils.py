import tomllib

from pre_commit_pep639.core_utils import extract_metadata_base

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
