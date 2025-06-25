import pathlib
import sys
import socket
import json
import hashlib
import base64

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'src'))

from efu.root import Root


def test_root_initialization():
    root = Root()
    assert root.hostname == socket.gethostname()


def test_canonical_hash():
    data = {"b": 2, "a": 1}
    h = Root.canonical_hash(data)

    json_str = json.dumps(data, separators=(",", ":"), sort_keys=True, ensure_ascii=False)
    digest = hashlib.sha1(json_str.encode('utf-8')).digest()
    expected = base64.urlsafe_b64encode(digest).decode('ascii').rstrip('=')[:10]
    assert h == expected
