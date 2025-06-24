import pathlib
import sys
import os

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'src'))

from efu import EfuRecord, EfuRecords


def test_efu_records_basic():
    header = [
        "Filename",
        "Size",
        "Date Modified",
        "Date Created",
        "Attributes",
    ]
    rec1 = EfuRecord(header, {"Filename": "foo"}, Size=1)
    rec2 = EfuRecord(header, {"Filename": "bar"}, Size=2)
    records = EfuRecords([rec1, rec2])

    assert len(records) == 2
    assert records[0]["Filename"] == "foo"
    assert records[1]["Size"] == 2


def test_append_from_path(tmp_path):
    header = [
        "Filename",
        "Size",
        "Date Modified",
        "Date Created",
        "Attributes",
    ]
    sample = tmp_path / "file.txt"
    sample.write_text("hello")

    records = EfuRecords()
    records.append_from_path(str(sample), header)

    assert len(records) == 1
    rec = records[0]
    st = os.stat(sample)
    expected_modified = int(st.st_mtime * 10_000_000) + 116444736000000000
    expected_created = int(st.st_ctime * 10_000_000) + 116444736000000000

    assert rec["Filename"] == str(sample)
    assert rec["Size"] == st.st_size
    assert rec["Date Modified"] == expected_modified
    assert rec["Date Created"] == expected_created
    assert rec["Attributes"] == 32
