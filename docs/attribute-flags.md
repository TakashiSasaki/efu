# Windows File Attribute Flags Specification

This document describes the file attribute letters displayed by Everything (EFU), their corresponding Windows API constants, numeric values, and bit positions when representing the FILE_ATTRIBUTE bits.

## 1. Attribute Letters and Meanings

Everything uses the following letters in the `Attributes` column to indicate file or directory properties:

| Letter | Description                        |
|--------|------------------------------------|
| R      | Read-Only                          |
| H      | Hidden                             |
| S      | System                             |
| D      | Directory                          |
| A      | Archive                            |
| N      | Normal (no other attributes set)   |

> **Note:** `N` is displayed by Everything when the file has the `FILE_ATTRIBUTE_NORMAL` bit set (value 128) and no other attribute bits.

## 2. Corresponding Windows Constants and Values

Each attribute letter maps to a Windows API constant. These constants are defined in the WinBase.h header for file operations, and are used by functions like `GetFileAttributes` and `SetFileAttributes`.

| Letter | Constant Name                   | Hex Value    | Decimal Value | Bit Position | Description                                                    |
|--------|---------------------------------|--------------|---------------|--------------|----------------------------------------------------------------|
| R      | FILE_ATTRIBUTE_READONLY         | `0x00000001` | 1             | 0            | File is read-only.                                             |
| H      | FILE_ATTRIBUTE_HIDDEN           | `0x00000002` | 2             | 1            | File is hidden.                                                |
| S      | FILE_ATTRIBUTE_SYSTEM           | `0x00000004` | 4             | 2            | File is a system file.                                         |
| D      | FILE_ATTRIBUTE_DIRECTORY        | `0x00000010` | 16            | 4            | Entry is a directory.                                          |
| A      | FILE_ATTRIBUTE_ARCHIVE          | `0x00000020` | 32            | 5            | File is marked for archival.                                   |
| N      | FILE_ATTRIBUTE_NORMAL           | `0x00000080` | 128           | 7            | Normal file; no other attributes set (displayed as 'N').       |

### Combining Flags

File attributes are bitwise flags and can be combined by OR-ing their values. For example:

- A directory and system file: `D | S` → `0x10 | 0x04` = `0x14` (displayed as "DS").
- A hidden, read-only file: `H | R` → `0x02 | 0x01` = `0x03` (displayed as "RH").

When displaying, Everything concatenates the letters in the order `DHSARN` for any bits set.

---

*End of Specification*
