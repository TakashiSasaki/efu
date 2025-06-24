import pathlib
import sys

# Add package source to path
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'src'))

from efu_csv_utils import parse_efu, write_efu


def test_roundtrip(tmp_path):
    root = pathlib.Path(__file__).resolve().parents[1]
    sample = root / 'sample1.efu'

    rows, header_raw, nl = parse_efu(str(sample))
    out_file = tmp_path / 'out.efu'
    write_efu(rows, header_raw, str(out_file), newline=nl)

    with open(sample, 'rb') as f:
        original = f.read()
    with open(out_file, 'rb') as f:
        new = f.read()

    assert original == new
