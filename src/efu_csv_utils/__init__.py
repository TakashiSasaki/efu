# efu_csv_utils.py
# Custom CSV parser and serializer for Everything EFU files

import os
from typing import List, Optional, Tuple


def parse_efu(file_path: str, encoding: str = 'utf-8') -> Tuple[List[List[str]], str, str]:
    """
    Parse an Everything EFU (CSV) file into a list of rows (excluding header),
    return rows, raw header line (including newline), and detected newline style.
    """
    # Read raw bytes to detect newline and header line
    with open(file_path, 'rb') as f:
        raw = f.read()
    newline = '\r\n' if b'\r\n' in raw else '\n'

    # Read file in text preserving newlines
    with open(file_path, 'r', encoding=encoding, newline='') as f:
        # Read header raw (first line with newline)
        header_raw = f.readline()
        # Read rest of content
        rest = f.read()

    # Split rest into lines by newline
    lines = rest.split(newline)
    rows: List[List[str]] = []
    for line in lines:
        if line == '':
            continue
        row: List[str] = []
        field: List[str] = []
        in_quote = False
        i = 0
        length = len(line)
        while i < length:
            ch = line[i]
            if ch == '"':
                # escaped quote or quote toggle
                if in_quote and i+1 < length and line[i+1] == '"':
                    field.append('"')
                    i += 2
                else:
                    in_quote = not in_quote
                    i += 1
            elif ch == ',' and not in_quote:
                row.append(''.join(field))
                field = []
                i += 1
            else:
                field.append(ch)
                i += 1
        # append the last field
        row.append(''.join(field))
        rows.append(row)
    return rows, header_raw, newline


def write_efu(rows: List[List[str]], header_raw: str, file_path: str, newline: Optional[str] = None, encoding: str = 'utf-8') -> None:
    """
    Serialize rows to EFU file preserving newline style,
    writing original header raw, then quoting data rows appropriately.
    - header_raw: original header line with its newline
    - newline: style for data rows (default '\n')
    """
    nl = newline or '\n'

    def needs_quote(value: str) -> bool:
        # Do not quote purely numeric values or empty strings representing NULL
        if value == "":
            return False
        return not value.isdigit()

    with open(file_path, 'w', encoding=encoding, newline='') as f:
        # Write original header unchanged
        f.write(header_raw)
        # Write data rows
        for row in rows:
            out_fields: List[str] = []
            for field in row:
                if needs_quote(field):
                    esc = field.replace('"', '""')
                    out_fields.append(f'"{esc}"')
                else:
                    out_fields.append(field)
            f.write(','.join(out_fields) + nl)


def main(argv: Optional[List[str]] = None) -> None:
    """Command line interface for parsing and writing EFU files."""
    import argparse

    parser = argparse.ArgumentParser(description="Parse and write EFU files")
    parser.add_argument("input", help="Path to the input EFU file")
    parser.add_argument("output", help="Path to write the output EFU file")
    args = parser.parse_args(argv)

    rows, header_raw, nl = parse_efu(args.input)
    write_efu(rows, header_raw, args.output, newline=nl)

    # Verify round-trip
    with open(args.input, "rb") as f:
        orig = f.read()
    with open(args.output, "rb") as f:
        new = f.read()
    if orig == new:
        print("Round-trip successful: files are identical")
    else:
        print("Round-trip failed: files differ")


if __name__ == "__main__":
    main()
