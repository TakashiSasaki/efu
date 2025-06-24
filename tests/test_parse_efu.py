import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'src'))

from efu_csv_utils import efu_to_array


def test_parse_efu_simple(tmp_path):
    csv_content = (
        "Filename,Size,Date Modified,Date Created,Attributes\r\n"
        "\"C:\\msys64\",,133876022280081366,133739602603410395,16\r\n"
        "\"C:\\msys64\\autorebase.bat\",82,133262362720000000,133739602600000000,32\r\n"
        "\"C:\\msys64\\clang64\",0,133665511886007850,133665511886007850,16\r\n"
    )

    sample_file = tmp_path / "sample.efu"
    sample_file.write_text(csv_content, newline="")

    rows, header, nl = efu_to_array(str(sample_file))

    assert header == [
        "Filename",
        "Size",
        "Date Modified",
        "Date Created",
        "Attributes",
    ]
    assert rows == [
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
    assert nl == "\r\n"
