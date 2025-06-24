# REMOTE Import Usage Guide

This document explains how to import the `efu_csv_utils` package directly from the remote repository using the `httpimport` package. This approach allows you to use the library without installing it locally.

---

## Requirements

- Python 3.10 or newer
- The [`httpimport`](https://pypi.org/project/httpimport/) package

Install `httpimport` with pip if you don't already have it:

```bash
pip install httpimport
```

## Basic Usage

1. Define the URL to the directory containing `efu_csv_utils` on GitHub:

```python
REMOTE_URL = "https://raw.githubusercontent.com/TakashiSasaki/efu/refs/heads/main/src/"
```

2. Use `httpimport.remote_repo` as a context manager and import `efu_csv_utils`:

```python
import importlib
import httpimport

with httpimport.remote_repo(url=REMOTE_URL):
    efu_csv_utils = importlib.import_module("efu_csv_utils")
```

3. Call functions from the imported module as usual:

```python
rows, header_fields, nl = efu_csv_utils.parse_efu("sample.efu")
```

## Notes

- The files are downloaded temporarily each time the context manager is entered.
- A network connection to GitHub is required while importing.
- This method mirrors the approach used in the test suite (`tests/test_httpimport_*.py`).

*End of REMOTE import guide*
