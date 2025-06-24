from typing import Iterable
from collections import UserList

from .efu_record import EfuRecord


class EfuRecords(UserList[EfuRecord]):
    """List-like collection for :class:`EfuRecord` objects."""

    def __init__(self, records: Iterable[EfuRecord] = ()) -> None:
        super().__init__(list(records))

    def append_from_path(self, file_path: str, headers: Iterable[str]) -> None:
        """Create an :class:`EfuRecord` from ``file_path`` and append it."""
        record = EfuRecord(headers)
        record.populate_from_path(file_path)
        self.append(record)
