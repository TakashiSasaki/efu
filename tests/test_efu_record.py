import pathlib
import sys

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
    assert rec.last_seen == 0
    assert rec.first_seen == 0
    assert rec.last_lost == 0
    assert rec.root is None

    rec2 = EfuRecord(header, last_seen=1, first_seen=2, last_lost=3, root="foo")
    assert rec2.last_seen == 1
    assert rec2.first_seen == 2
    assert rec2.last_lost == 3
    assert rec2.root == "foo"

    rec3 = EfuRecord(header, root=10)
    assert rec3.root == 10
