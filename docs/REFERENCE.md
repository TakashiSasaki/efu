# EFU CSV Parser and Serializer Specification

This document describes the design, behavior, and API of the `efu` module, which provides custom parsing and serialization of Everything EFU (CSV) files for lossless round-trip processing.

---

## 1. Overview

* **Purpose**: Enable reading and writing of Everything EFU files such that a file can be parsed into memory (rows of strings) and written back exactly byte-for-byte identical to the original.
* **Key Features**:

  * Detects and preserves original newline style (`\r\n` or `\n`).
  * Reads header line, splits it into fields, and reconstructs it when writing.
  * Parses quoted and unquoted fields correctly, handling escaped quotes (`""`).
  * Distinguishes between numeric fields, empty fields (NULL), and string fields for quoting rules.
  * Serializes data rows to preserve exact structure: unquoted numeric and empty fields, quoted text fields.

---

## 2. API

### 2.1 `efu_to_array`

```python
def efu_to_array(file_path: str, encoding: str = 'utf-8') -> Tuple[List[List[str]], str, str]
```

* **Inputs**:

  * `file_path` (`str`): Path to the EFU file to parse.
  * `encoding` (`str`, optional): Text encoding for file I/O (default `'utf-8'`).

* **Outputs (tuple)**:

  1. `rows` (`List[List[str]]`): A list of data rows (each a list of field strings). The header row is excluded.
  2. `header_fields` (`List[str]`): Header row split on commas.
  3. `newline` (`str`): The detected newline sequence in the file (`'\r\n'` or `'\n'`).

* **Behavior**:

  1. Reads entire file in binary to detect newline style.
  2. Opens file in text mode to read the header line (split into `header_fields`) plus remainder (`rest`).
  3. Splits `rest` by the detected newline.
  4. For each non-empty line:

     * Iterates character by character.
     * Toggles `in_quote` on `"` (unless doubled quotes `""`, which produce a literal `"`).
     * Splits fields on unquoted commas.
     * Collects characters into fields, preserving all content.
  5. Appends last field of each line.

* **Edge Cases**:

  * Empty lines after final newline are skipped.
  * Lines with consecutive commas produce empty-string fields (`''`).
  * Fields containing commas or quotes must be quoted and escaped in source; parser handles that.

### 2.2 `array_to_efu`

```python
def array_to_efu(
    rows: List[List[str]],
    header_fields: List[str],
    file_path: str,
    newline: Optional[str] = None,
    encoding: str = 'utf-8'
) -> None
```

* **Inputs**:

  * `rows` (`List[List[str]]`): Data rows (from `efu_to_array`), each a list of field strings.
  * `header_fields` (`List[str]`): Header row values split on commas.
  * `file_path` (`str`): Destination path for the output EFU file.
  * `newline` (`str`, optional): Newline sequence to use for data rows; defaults to `'\n'` if not provided.
  * `encoding` (`str`, optional): Text encoding for file I/O (default `'utf-8'`).

* **Behavior**:

  1. Opens `file_path` in write-text mode with `newline=''` to control newlines manually.
  2. Writes the header reconstructed from `header_fields`.
  3. For each row in `rows`:

     * For each field string:

       * **`needs_quote(field)`** determines if the field is to be quoted:

         * Returns `False` if the field is an empty string (`''`) or if `field.isdigit()` is `True` (pure integer digits).
         * Returns `True` otherwise (any non-digit or mixed content).
       * If `needs_quote`:

         * Escapes `"` by doubling (`""`).
         * Encloses the result in `"` characters.
       * Else: writes the raw field (digit string or empty) without quotes.
     * Joins fields with commas (no spaces), appends the `newline` sequence, and writes the line.

* **Preserved Properties**:

  * Original header line and newline style.
  * Unquoted numeric fields and empty (NULL) fields as consecutive commas.
  * Quoted string fields with correct escaping.

* **Edge Cases**:

  * Fields with leading/trailing spaces are treated as text and quoted.
  * Zero-length value (`''`) always written as empty (no quotes): `, ,` yields `,,`.

### 2.3 `efu_to_objects`

```python
def efu_to_objects(file_path: str, encoding: str = 'utf-8') -> List[Dict[str, Any]]
```

* **Returns**: List of dictionaries using header names as keys. Empty fields become
  `None` and digit-only fields are converted to `int`.

### 2.4 `objects_to_efu`

```python
def objects_to_efu(
    objects: List[Dict[str, Any]],
    file_path: str,
    newline: Optional[str] = None,
    encoding: str = 'utf-8'
) -> None
```

* **Inputs**:

  * `objects` (`List[Dict[str, Any]]`): Row dictionaries. ``None`` values become empty fields.
  * `file_path` (`str`): Destination EFU file path.
  * `newline` (`str`, optional): Newline sequence for data rows; default `'\n'`.
  * `encoding` (`str`, optional): Text encoding (default `'utf-8'`).

* **Behavior**:

  1. Header fields are taken from the keys of the first object.
  2. Values are converted to strings with ``str()`` (``None`` -> ``''``).
  3. Delegates to `array_to_efu` for final serialization.

### 2.5 `EfuRecord`

`EfuRecord` represents a single EFU row and tracks when the file metadata was
successfully retrieved or lost.

* **Attributes**:
  * `last_seen` (`int | None`): POSIX timestamp when metadata was last obtained.
  * `first_seen` (`int | None`): Set on first successful call to
    `populate_from_path` if it was `None`.
  * `last_lost` (`int | None`): Timestamp recorded when metadata retrieval
    fails (e.g., file missing).

`populate_from_path(path)` fills the record fields using `os.stat` and updates
these timestamps:

1. On success, `last_seen` is set to `int(time.time())`; if `first_seen` is
   unset, it is also set to that value.
2. On failure, `last_lost` is set to the current time and the original
   `OSError` is re-raised.

---

## 3. Examples

Given an input EFU file:

```
Filename,Size,Date Modified,Date Created,Attributes\r\n
"\\server\\share",,133935749084528561,133935749084528561,16\r\n
...\r\n
```

```python
rows, header_fields, nl = efu_to_array('input.efu')
array_to_efu(rows, header_fields, 'output.efu', newline=nl)
# 'output.efu' is now byte-for-byte identical to 'input.efu'
```

---

## 4. Error Handling

* File not found or I/O errors propagate as standard `IOError`/`OSError`.
* Malformed CSV (unbalanced quotes) leads to incorrect parsing; library does not validate strict CSV grammar beyond quoted-field handling.

---

## 5. Limitations

* `efu_to_array` does not convert numeric strings to Python numeric types; use
  `efu_to_objects` for typed values.
* ISO/locale-specific encodings other than UTF-8 must be specified.
* No streaming: entire file is loaded into memory; may not scale for extremely large EFU files.

---
## Installation and Usage with Poetry

This project uses [Poetry](https://python-poetry.org/) for packaging and dependency management. After installing Poetry, run:

```bash
poetry install
```

The command installs the `efu` package from `src` in Poetry's virtual environment. Use `poetry run` to execute scripts that depend on the library:

```bash
poetry run python examples/my_script.py
```

*End of specification.*
