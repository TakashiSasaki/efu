from typing import List, Optional


def array_to_efu(
    rows: List[List[str]],
    header_fields: List[str],
    file_path: str,
    newline: Optional[str] = None,
    encoding: str = "utf-8",
) -> None:
    """Serialize rows to an EFU file preserving newline style."""
    nl = newline or "\n"

    def needs_quote(value: str) -> bool:
        if value == "":
            return False
        return not value.isdigit()

    with open(file_path, "w", encoding=encoding, newline="") as f:
        f.write(",".join(header_fields) + nl)
        for row in rows:
            out_fields: List[str] = []
            for field in row:
                if needs_quote(field):
                    esc = field.replace('"', '""')
                    out_fields.append(f'"{esc}"')
                else:
                    out_fields.append(field)
            f.write(",".join(out_fields) + nl)
