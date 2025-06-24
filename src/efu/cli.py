from typing import List, Optional

from .array_to_efu import array_to_efu
from .efu_to_array import efu_to_array


def main(argv: Optional[List[str]] = None) -> None:
    """Command line interface for parsing and writing EFU files."""
    import argparse

    parser = argparse.ArgumentParser(description="Parse and write EFU files")
    parser.add_argument("input", help="Path to the input EFU file")
    parser.add_argument("output", help="Path to write the output EFU file")
    args = parser.parse_args(argv)

    rows, header_fields, nl = efu_to_array(args.input)
    array_to_efu(rows, header_fields, args.output, newline=nl)

    with open(args.input, "rb") as f:
        orig = f.read()
    with open(args.output, "rb") as f:
        new = f.read()
    if orig == new:
        print("Round-trip successful: files are identical")
    else:
        print("Round-trip failed: files differ")
