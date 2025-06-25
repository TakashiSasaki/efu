from typing import Any, Iterable, Mapping, Optional, Union
import os
import stat
import time


FILETIME_EPOCH = 116444736000000000


def _to_filetime(timestamp: float) -> int:
    """Convert POSIX timestamp to Windows FILETIME."""
    return int(timestamp * 10_000_000) + FILETIME_EPOCH


class EfuRecord(dict):
    """Dictionary-like record initialized with EFU header fields."""

    __slots__ = ("last_seen", "first_seen", "last_lost", "root")

    def __init__(
        self,
        headers: Iterable[str],
        data: Optional[Mapping[str, Any]] = None,
        *,
        last_seen: Optional[int] = None,
        first_seen: Optional[int] = None,
        last_lost: Optional[int] = None,
        root: Optional[Union[str, int]] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__({key: None for key in headers})
        if data:
            self.update(data)
        if kwargs:
            self.update(kwargs)
        self.last_seen = last_seen
        self.first_seen = first_seen
        self.last_lost = last_lost
        self.root = root

    def populate_from_path(self, file_path: str) -> None:
        """Populate record fields using metadata from ``file_path``.

        Updates ``last_seen`` when metadata is successfully retrieved and
        ``last_lost`` when retrieval fails.
        """
        try:
            st = os.stat(file_path)
        except OSError:
            self.last_lost = int(time.time())
            raise
        else:
            now = int(time.time())
            self.last_seen = now
            if self.first_seen is None:
                self.first_seen = now

        if "Filename" in self:
            self["Filename"] = file_path
        if "Size" in self:
            self["Size"] = st.st_size
        if "Date Modified" in self:
            self["Date Modified"] = _to_filetime(st.st_mtime)
        if "Date Created" in self:
            self["Date Created"] = _to_filetime(st.st_ctime)
        if "Attributes" in self:
            attr = 16 if stat.S_ISDIR(st.st_mode) else 32
            if not os.access(file_path, os.W_OK):
                attr |= 1
            self["Attributes"] = attr

        # populate additional fields generically
        for key in self.keys():
            if key not in {
                "Filename",
                "Size",
                "Date Modified",
                "Date Created",
                "Attributes",
            }:
                # For unknown fields, leave as-is (None)
                pass
