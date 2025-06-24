# EFU Time Columns (FILETIME) Specification

This document explains how the `Date Modified` and `Date Created` columns in an Everything EFU file are represented as Windows FILETIME values, and how to interpret and convert them.

---

## 1. Overview

* Everything exports the timestamps for file modification and creation as raw **Windows FILETIME** values.
* These are 64-bit unsigned integers representing the number of 100-nanosecond intervals elapsed since January 1, 1601 UTC.

## 2. Windows FILETIME Definition

* **Epoch**: January 1, 1601 00:00:00 UTC
* **Unit**: 100 nanoseconds (0.0000001 seconds)
* **Storage**: 64-bit unsigned integer (DWORD64)
* **API Constants**: Used by Win32 functions such as `GetFileTime` and `SetFileTime`.

## 3. EFU CSV Representation

* EFU header fields: `Date Modified`, `Date Created`.
* Each value is output as a decimal string of the 64-bit FILETIME integer, e.g. `133935749084528561`.
* No quoting is applied when the field consists only of digits.

## 4. Conversion to Unix Time and Human-Readable Format

To convert a raw FILETIME value to a standard Unix-based datetime:

1. **Subtract the FILETIME epoch difference** (in 100-ns units):

   ```python
   EPOCH_DIFF = 116444736000000000  # (number of 100-ns ticks from 1601-01-01 to 1970-01-01)
   secs_since_unix = (filetime_value - EPOCH_DIFF) / 10_000_000  # seconds
   ```
2. **Convert to UTC datetime**:

   ```python
   import datetime
   dt_utc = datetime.datetime.utcfromtimestamp(secs_since_unix)
   ```
3. **Apply local time zone if needed** (e.g. JST = UTC+9):

   ```python
   dt_jst = dt_utc + datetime.timedelta(hours=9)
   ```

**Example**: FILETIME `133935749084528561` expands to:

* Unix seconds: `1749101308.452856` (UTC)
* UTC datetime: `2025-06-05T05:28:28.452856+00:00`
* Japan Standard Time: `2025-06-05T14:28:28.452856+09:00`

## 5. Usage in Custom Parsing

When writing a custom EFU parser/serializer, preserve the raw FILETIME value as-is:

* Store as string internally (no numeric conversion), then write back unchanged.
* When post-processing, use the conversion algorithm above to display or filter by date.

---

*End of EFU Time Columns Specification*
