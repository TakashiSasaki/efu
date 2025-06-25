import os
import socket
import uuid
from typing import Optional, Any
import json
import hashlib
import base64


class Root:
    """Information about a machine and path."""

    def __init__(self, path: Optional[str] = None) -> None:
        self.hostname: Optional[str] = None
        self.mac_address: Optional[str] = None
        self.ip_address: Optional[str] = None
        self.path: Optional[str] = None

        try:
            self.hostname = socket.gethostname()
        except Exception:
            self.hostname = None

        try:
            node = uuid.getnode()
            self.mac_address = ":".join(
                f"{(node >> i) & 0xFF:02x}" for i in range(40, -1, -8)
            )
        except Exception:
            self.mac_address = None

        try:
            if self.hostname:
                self.ip_address = socket.gethostbyname(self.hostname)
            else:
                self.ip_address = None
        except Exception:
            self.ip_address = None

        if path is not None:
            try:
                self.path = os.fspath(path)
            except Exception:
                self.path = None
        else:
            try:
                self.path = os.getcwd()
            except Exception:
                self.path = None

    @staticmethod
    def canonical_hash(data: Any) -> str:
        """Return first 10 chars of base64url SHA1 of canonical JSON of ``data``."""
        json_str = json.dumps(data, separators=(",", ":"), sort_keys=True, ensure_ascii=False)
        digest = hashlib.sha1(json_str.encode("utf-8")).digest()
        b64 = base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")
        return b64[:10]

    def __str__(self) -> str:
        return self.hostname=======
