import pathlib
import sys
import os
import time
import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'src'))

from efu import EfuRecord


def test_efu_record_initialization():
    header = [
        "Filename",
        "Size",
        "Date Modified",
        "Date Created",
        "Attributes",
    ]
    rec = EfuRecord(header)
    assert list(rec.keys()) == header
    assert all(value is None for value in rec.values())


def test_efu_record_with_data():
    header = [
        "Filename",
        "Size",
        "Date Modified",
        "Date Created",
        "Attributes",
    ]
    rec = EfuRecord(header, {"Filename": "foo"}, Size=100)
    assert rec["Filename"] == "foo"
    assert rec["Size"] == 100
    for key in header:
        assert key in rec


def test_efu_record_attributes():
    header = ["Filename"]
    rec = EfuRecord(header)
    assert rec.last_seen is None
    assert rec.first_seen is None
    assert rec.last_lost is None
    assert rec.root is None

    rec2 = EfuRecord(header, last_seen=1, first_seen=2, last_lost=3, root="foo")
    assert rec2.last_seen == 1
    assert rec2.first_seen == 2
    assert rec2.last_lost == 3
    assert rec2.root == "foo"

    rec3 = EfuRecord(header, root=10)
    assert rec3.root == 10


def test_populate_from_path(tmp_path):
    header = [
        "Filename",
        "Size",
        "Date Modified",
        "Date Created",
        "Attributes",
    ]
    sample = tmp_path / "file.txt"
    sample.write_text("hello")

    rec = EfuRecord(header)
    rec.populate_from_path(str(sample))

    st = os.stat(sample)
    expected_modified = int(st.st_mtime * 10_000_000) + 116444736000000000
    expected_created = int(st.st_ctime * 10_000_000) + 116444736000000000

    assert rec["Filename"] == str(sample)
    assert rec["Size"] == st.st_size
    assert rec["Date Modified"] == expected_modified
    assert rec["Date Created"] == expected_created
    assert rec["Attributes"] == 32


def test_populate_updates_last_seen(tmp_path):
    header = [
        "Filename",
        "Size",
        "Date Modified",
        "Date Created",
        "Attributes",
    ]

    sample = tmp_path / "file.txt"
    sample.write_text("hello")

    rec = EfuRecord(header)
    before = int(time.time()) - 1
    rec.populate_from_path(str(sample))
    after = int(time.time()) + 1

    assert rec.last_lost is None
    assert rec.last_seen is not None
    assert rec.first_seen is not None
    assert before <= rec.last_seen <= after
    assert before <= rec.first_seen <= after


def test_populate_updates_last_lost(tmp_path):
    header = ["Filename"]
    sample = tmp_path / "missing.txt"
    rec = EfuRecord(header)
    before = int(time.time()) - 1
    with pytest.raises(FileNotFoundError):
        rec.populate_from_path(str(sample))
    after = int(time.time()) + 1

    assert rec.last_seen is None
    assert rec.last_lost is not None
    assert before <= rec.last_lost <= after


def test_populate_keeps_first_seen_if_set(tmp_path):
    header = ["Filename"]
    sample = tmp_path / "file.txt"
    sample.write_text("hello")

    rec = EfuRecord(header, first_seen=12345)
    before = int(time.time()) - 1
    rec.populate_from_path(str(sample))
    after = int(time.time()) + 1

    assert rec.first_seen == 12345
    assert rec.last_lost is None
    assert rec.last_seen is not None
    assert before <= rec.last_seen <= after
