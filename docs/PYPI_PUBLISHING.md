# PyPI Publishing & Packaging Guide for LabX Remote

This guide provides instructions for building, validating, and releasing `labx-remote` to the Python Package Index (PyPI).

---

## 1. Package Identification & Distribution Name

The verified distribution name is configured in `pyproject.toml`:
- **Package Name:** `labx-remote`
- **CLI Executable Script:** `labx` (`labx.cli:app`)
- **Current Version:** `1.0.0`
- **Build Backend:** `setuptools.build_meta`

---

## 2. Preparing the Build Environment

Install the official Python packaging tools:

```bash
python -m pip install --upgrade build twine
```

---

## 3. Building Source Distribution and Wheel

Clean any previous artifacts and build the distribution:

```bash
# Windows PowerShell
Remove-Item -Recurse -Force dist/* -ErrorAction SilentlyContinue

# Build sdist (.tar.gz) and pure-python wheel (.whl)
python -m build
```

This generates:
- `dist/labx_remote-1.0.0-py3-none-any.whl`
- `dist/labx_remote-1.0.0.tar.gz`

---

## 4. Validating Distribution Artifacts

Always run `twine check` to ensure long descriptions, metadata, and license fields render without errors:

```bash
twine check dist/*
```

Expected output:
```
Checking dist/labx_remote-1.0.0-py3-none-any.whl: PASSED
Checking dist/labx_remote-1.0.0.tar.gz: PASSED
```

---

## 5. Publishing to TestPyPI (Staging Verification)

Test the package release on TestPyPI before making a public production release:

```bash
twine upload --repository testpypi dist/*
```

When prompted, supply your TestPyPI API token (`__token__` as username).

Verify installation from TestPyPI in an isolated environment:
```bash
python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ labx-remote
labx --version
```

---

## 6. Production Release to PyPI

> **Note:** Only publish with explicit administrative authorization and verified PyPI credentials.

```bash
twine upload dist/*
```

Supply your PyPI API token (`__token__` username).

### Automated Release via GitHub Actions (Trusted Publishing)

Alternatively, configure GitHub Actions Trusted Publishing without storing long-lived API tokens:

```yaml
# .github/workflows/publish.yml
name: Publish to PyPI

on:
  release:
    types: [published]

permissions:
  id-token: write

jobs:
  pypi-publish:
    name: Upload release to PyPI
    runs-on: ubuntu-latest
    environment:
      name: pypi
      url: https://pypi.org/p/labx-remote
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install build tools
        run: pip install build
      - name: Build package
        run: python -m build
      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
```

