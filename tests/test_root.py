import pathlib
import sys
import socket
import uuid

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
