from typing import List, Tuple


def efu_to_array(file_path: str, encoding: str = "utf-8") -> Tuple[List[List[str]], List[str], str]:
    """Parse an Everything EFU file and return rows, header fields, and newline."""
    with open(file_path, 'rb') as f:
        raw = f.read()
    newline = '\r\n' if b'\r\n' in raw else '\n'

    with open(file_path, 'r', encoding=encoding, newline='') as f:
        header_raw = f.readline()
        header_fields = header_raw.rstrip('\r\n').split(',')
        rest = f.read()

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
                if in_quote and i + 1 < length and line[i + 1] == '"':
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
        row.append(''.join(field))
        rows.append(row)
    return rows, header_fields, newline
