import os
import socket
import uuid
from typing import Optional


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

