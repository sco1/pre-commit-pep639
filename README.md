# pre-commit-pep639
[![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fsco1%2Fpre-commit-pep639%2Frefs%2Fheads%2Fmain%2Fpyproject.toml&logo=python&logoColor=FFD43B)](https://github.com/sco1/pre-commit-pep639/blob/main/pyproject.toml)
[![GitHub Release](https://img.shields.io/github/v/release/sco1/pre-commit-pep639)](https://github.com/sco1/pre-commit-pep639/releases)
[![GitHub License](https://img.shields.io/github/license/sco1/pre-commit-pep639?color=magenta)](https://github.com/sco1/pre-commit-pep639/blob/main/LICENSE)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/sco1/pre-commit-pep639/main.svg)](https://results.pre-commit.ci/latest/github/sco1/pre-commit-pep639/main)

A pre-commit hook for [PEP639](https://peps.python.org/pep-0639/) compliance in your `pyproject.toml`.

## Using `pre-commit-pep639` With pre-commit
Add this to your `.pre-commit-config.yaml`

```yaml
-   repo: https://github.com/sco1/pre-commit-pep639
    rev: v0.1.0
    hooks:
    - id: check-classifiers
    - id: check-glob-resolve
    - id: check-glob-syntax
```

## Hooks
**NOTE:** Unless otherwise noted, any metadata specification arrangements that are not explicitly supported should pass through without failing the hook. For example, if you have a build tool `foo` that specifies its metadata in a `[tools.foo]` table, its contents will not be checked.

### `check-classifiers`
Check classifiers for license specification. Note that currently only `pyproject.toml` is inspected, if present.

Two metadata specification types are currently supported:

* PEP621 compliant: The provided TOML file is assumed to contain a `project` table, which contains a list of PyPI classifiers in the `classifiers` field.
* Poetry: The provided TOML file is assumed to contain a `tools.poetry` table, which contains a list of PyPI classifiers in the `classifiers` field.

### `check-glob-resolve`
Check that [`license-files` glob(s)](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#license-files) match file(s) in the repo.

**NOTE:** Globs are checked relative to `pyproject.toml`'s parent directory, though in most cases this should be the same as the repository's root.

### `check-glob-syntax`
Check that [`license-files` glob(s)](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#license-files) do not contain syntax errors.

The following syntax issues are currently checked:

* Presence of leading slash character (`\`) in glob
* Presence of parent directory indicator (`..`) in glob

## Python Version Support
Starting with Python 3.11, a best attempt is made to support Python versions until they reach EOL, after which support will be formally dropped by the next minor or major release of this package, whichever arrives first. The status of Python versions can be found [here](https://devguide.python.org/versions/).
