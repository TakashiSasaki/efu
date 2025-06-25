import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'src'))

from efu import EfuRecord, EfuRecords, objects_to_efu


def test_objects_to_efu(tmp_path):
    objs = [
        {
            "Filename": "C:\\msys64",
            "Size": None,
            "Date Modified": 133876022280081366,
            "Date Created": 133739602603410395,
            "Attributes": 16,
        },
        {
            "Filename": "C:\\msys64\\autorebase.bat",
            "Size": 82,
            "Date Modified": 133262362720000000,
            "Date Created": 133739602600000000,
            "Attributes": 32,
        },
        {
            "Filename": "C:\\msys64\\clang64",
            "Size": 0,
            "Date Modified": 133665511886007850,
            "Date Created": 133665511886007850,
            "Attributes": 16,
        },
    ]

    out_file = tmp_path / "out.efu"
    objects_to_efu(objs, str(out_file), newline="\r\n")

    expected = (
        "Filename,Size,Date Modified,Date Created,Attributes\r\n"
        "\"C:\\msys64\",,133876022280081366,133739602603410395,16\r\n"
        "\"C:\\msys64\\autorebase.bat\",82,133262362720000000,133739602600000000,32\r\n"
        "\"C:\\msys64\\clang64\",0,133665511886007850,133665511886007850,16\r\n"
    )

    with open(out_file, "r", newline="") as f:
        content = f.read()
    assert content == expected


def test_objects_to_efu_with_efu_records(tmp_path):
    header = [
        "Filename",
        "Size",
        "Date Modified",
        "Date Created",
        "Attributes",
    ]
    records = EfuRecords([
        EfuRecord(
            header,
            {
                "Filename": "C:\\msys64",
                "Size": None,
                "Date Modified": 133876022280081366,
                "Date Created": 133739602603410395,
                "Attributes": 16,
            },
        ),
        EfuRecord(
            header,
            {
                "Filename": "C:\\msys64\\autorebase.bat",
                "Size": 82,
                "Date Modified": 133262362720000000,
                "Date Created": 133739602600000000,
                "Attributes": 32,
            },
        ),
        EfuRecord(
            header,
            {
                "Filename": "C:\\msys64\\clang64",
                "Size": 0,
                "Date Modified": 133665511886007850,
                "Date Created": 133665511886007850,
                "Attributes": 16,
            },
        ),
    ])

    out_file = tmp_path / "out_records.efu"
    objects_to_efu(records, str(out_file), newline="\r\n")

    expected = (
        "Filename,Size,Date Modified,Date Created,Attributes\r\n"
        "\"C:\\msys64\",,133876022280081366,133739602603410395,16\r\n"
        "\"C:\\msys64\\autorebase.bat\",82,133262362720000000,133739602600000000,32\r\n"
        "\"C:\\msys64\\clang64\",0,133665511886007850,133665511886007850,16\r\n"
    )

    with open(out_file, "r", newline="") as f:
        content = f.read()
    assert content == expected
