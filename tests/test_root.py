import pathlib
import sys
import socket
import base64
import json
import jcs
import uuid
import hashlib
import os

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'src'))

from efu import Root

def test_root_basic(tmp_path):
    r = Root(str(tmp_path))
    assert r.path == str(tmp_path)
    assert r.hostname is None or isinstance(r.hostname, str)
    assert r.ip_address is None or isinstance(r.ip_address, str)
    assert r.mac_address is None or isinstance(r.mac_address, str)


def test_hostname_failure(monkeypatch):
    def bad_hostname():
        raise OSError('fail')

    monkeypatch.setattr(socket, 'gethostname', bad_hostname)
    monkeypatch.setattr(socket, 'gethostbyname', lambda x: (_ for _ in ()).throw(RuntimeError('should not be called')))
    monkeypatch.setattr(uuid, 'getnode', lambda: 0x010203040506)

    r = Root('/tmp')
    assert r.hostname is None
    assert r.ip_address is None
    assert r.mac_address == '01:02:03:04:05:06'

def test_root_initialization():
    root = Root()
    assert root.hostname == socket.gethostname()


def test_root_default_path():
    expected = os.path.abspath(os.getcwd())
    root = Root()
    assert root.path == expected


def test_canonical_hash():
    data = {"b": 2, "a": 1}
    h = Root.canonical_hash(data)

    json_bytes = jcs.canonicalize(data)
    digest = hashlib.sha1(json_bytes).digest()
    expected = base64.urlsafe_b64encode(digest).decode('ascii').rstrip('=')[:10]
    assert h == expected


def test_to_json(tmp_path):
    r = Root(str(tmp_path))
    js = r.to_json()
    data = json.loads(js)
    assert data['path'] == str(tmp_path)
    assert js == jcs.canonicalize(data).decode('utf-8')


def test_str(tmp_path):
    r = Root(str(tmp_path))
    s = str(r)
    data = json.loads(s)
    assert data['path'] == str(tmp_path)
