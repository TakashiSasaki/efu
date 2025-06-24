from typing import Any, Dict, List

from .efu_to_array import efu_to_array


def efu_to_objects(file_path: str, encoding: str = "utf-8") -> List[Dict[str, Any]]:
    """Parse an EFU file and return a list of row dictionaries."""
    rows, header_fields, _ = efu_to_array(file_path, encoding=encoding)

    objects: List[Dict[str, Any]] = []
    for row in rows:
        obj: Dict[str, Any] = {}
        for i, header in enumerate(header_fields):
            value = row[i] if i < len(row) else ""
            if value == "":
                obj[header] = None
            elif value.isdigit():
                obj[header] = int(value)
            else:
                obj[header] = value
        objects.append(obj)

    return objects
