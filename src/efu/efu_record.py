from typing import Any, Iterable, Mapping, Optional


class EfuRecord(dict):
    """Dictionary-like record initialized with EFU header fields."""

    __slots__ = ("last_seen", "first_seen", "last_lost")

    def __init__(
        self,
        headers: Iterable[str],
        data: Optional[Mapping[str, Any]] = None,
        *,
        last_seen: int = 0,
        first_seen: int = 0,
        last_lost: int = 0,
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
