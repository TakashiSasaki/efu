import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'src'))

from efu import efu_to_objects


def test_efu_to_objects(tmp_path):
    csv_content = (
        "Filename,Size,Date Modified,Date Created,Attributes\r\n"
        "\"C:\\msys64\",,133876022280081366,133739602603410395,16\r\n"
        "\"C:\\msys64\\autorebase.bat\",82,133262362720000000,133739602600000000,32\r\n"
        "\"C:\\msys64\\clang64\",0,133665511886007850,133665511886007850,16\r\n"
    )
    sample_file = tmp_path / "sample.efu"
    sample_file.write_text(csv_content, newline="")

    objs = efu_to_objects(str(sample_file))

    assert objs == [
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
