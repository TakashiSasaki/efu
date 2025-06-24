import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'src'))

from efu import array_to_efu


def test_write_efu_simple(tmp_path):
    header = [
        "Filename",
        "Size",
        "Date Modified",
        "Date Created",
        "Attributes",
    ]
    rows = [
        ["C:\\msys64", "", "133876022280081366", "133739602603410395", "16"],
        [
            "C:\\msys64\\autorebase.bat",
            "82",
            "133262362720000000",
            "133739602600000000",
            "32",
        ],
        [
            "C:\\msys64\\clang64",
            "0",
            "133665511886007850",
            "133665511886007850",
            "16",
        ],
    ]

    out_file = tmp_path / "out.efu"
    array_to_efu(rows, header, str(out_file), newline="\r\n")

    expected = (
        "Filename,Size,Date Modified,Date Created,Attributes\r\n"
        "\"C:\\msys64\",,133876022280081366,133739602603410395,16\r\n"
        "\"C:\\msys64\\autorebase.bat\",82,133262362720000000,133739602600000000,32\r\n"
        "\"C:\\msys64\\clang64\",0,133665511886007850,133665511886007850,16\r\n"
    )

    with open(out_file, "r", newline="") as f:
        content = f.read()
    assert content == expected
