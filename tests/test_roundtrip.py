import pathlib
import sys

# Add package source to path
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'src'))

from efu_csv_utils import efu_to_array, array_to_efu


def test_roundtrip(tmp_path):
    root = pathlib.Path(__file__).resolve().parents[1]
    sample = root / 'samples' / 'sample1.efu'

    rows, header_fields, nl = efu_to_array(str(sample))
    out_file = tmp_path / 'out.efu'
    array_to_efu(rows, header_fields, str(out_file), newline=nl)

    with open(sample, 'rb') as f:
        original = f.read()
    with open(out_file, 'rb') as f:
        new = f.read()

    assert original == new
