from typing import Any, Dict, List, Optional

from .array_to_efu import array_to_efu


def objects_to_efu(
    objects: List[Dict[str, Any]],
    file_path: str,
    newline: Optional[str] = None,
    encoding: str = "utf-8",
) -> None:
    """Serialize a list of dictionaries to an EFU CSV file."""
    if not objects:
        raise ValueError("objects list must not be empty")

    header_fields = list(objects[0].keys())
    rows: List[List[str]] = []
    for obj in objects:
        row: List[str] = []
        for key in header_fields:
            value = obj.get(key)
            if value is None:
                row.append("")
            else:
                row.append(str(value))
        rows.append(row)

    array_to_efu(rows, header_fields, file_path, newline=newline, encoding=encoding)
