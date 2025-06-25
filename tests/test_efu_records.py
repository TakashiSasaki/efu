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


def test_extend_from_directory(tmp_path):
    header = [
        "Filename",
        "Size",
        "Date Modified",
        "Date Created",
        "Attributes",
    ]

    dir1 = tmp_path / "dir1"
    dir1.mkdir()
    file1 = dir1 / "file1.txt"
    file1.write_text("a")

    dir2 = tmp_path / "dir2"
    dir2.mkdir()
    file2 = dir2 / "file2.txt"
    file2.write_text("b")

    records = EfuRecords()
    records.extend_from_directory(str(tmp_path), header)

    expected_paths = {
        str(tmp_path),
        str(dir1),
        str(file1),
        str(dir2),
        str(file2),
    }

    filenames = {rec["Filename"] for rec in records}
    assert filenames == expected_paths
    assert len(records) == len(expected_paths)

    rec_file1 = next(r for r in records if r["Filename"] == str(file1))
    st_file1 = os.stat(file1)
    expected_modified = int(st_file1.st_mtime * 10_000_000) + 116444736000000000
    expected_created = int(st_file1.st_ctime * 10_000_000) + 116444736000000000
    assert rec_file1["Size"] == st_file1.st_size
    assert rec_file1["Date Modified"] == expected_modified
    assert rec_file1["Date Created"] == expected_created
    assert rec_file1["Attributes"] == 32


def test_extend_repository_root():
    header = [
        "Filename",
        "Size",
        "Date Modified",
        "Date Created",
        "Attributes",
    ]
    root = pathlib.Path(__file__).resolve().parents[1]

    records = EfuRecords()
    records.extend_from_directory(str(root), header)

    filenames = {rec["Filename"] for rec in records}
    assert str(root) in filenames
    assert str(root / "README.md") in filenames
    assert str(root / "pyproject.toml") in filenames
    assert len(records) >= 3

