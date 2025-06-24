"""Utilities for parsing and writing Everything EFU CSV files.

The functions provided here allow EFU files to be parsed into Python objects and
written back without losing information. Newline style and quoting are preserved
so that a file round‐tripped through this library will be byte‐for‐byte
identical to the original.
"""

__version__ = "0.1.0"

from .efu_record import EfuRecord
from .efu_to_array import efu_to_array
from .efu_to_objects import efu_to_objects
from .objects_to_efu import objects_to_efu
from .array_to_efu import array_to_efu
from .cli import main

__all__ = [
    "EfuRecord",
    "efu_to_array",
    "efu_to_objects",
    "array_to_efu",
    "objects_to_efu",
    "main",
]
