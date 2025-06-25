import socket
import json
import hashlib
import base64
from typing import Any


class Root:
    """Represent host information for EFU records."""

    def __init__(self) -> None:
        try:
            hostname = socket.gethostname()
        except Exception as e:
            raise RuntimeError("Unable to obtain hostname") from e
        if not hostname:
            raise RuntimeError("Hostname could not be determined")
        self.hostname = hostname

    @staticmethod
    def canonical_hash(data: Any) -> str:
        """Return first 10 chars of base64url SHA1 of canonical JSON of ``data``."""
        json_str = json.dumps(data, separators=(",", ":"), sort_keys=True, ensure_ascii=False)
        digest = hashlib.sha1(json_str.encode("utf-8")).digest()
        b64 = base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")
        return b64[:10]

    def __str__(self) -> str:
        return self.hostname
