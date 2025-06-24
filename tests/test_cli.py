import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'src'))

from efu import main as cli_main


def test_cli_roundtrip(tmp_path, capsys):
    root = pathlib.Path(__file__).resolve().parents[1]
    sample = root / 'samples' / 'sample1.efu'
    out_file = tmp_path / 'out.efu'

    cli_main([str(sample), str(out_file)])

    with open(sample, 'rb') as f:
        original = f.read()
    with open(out_file, 'rb') as f:
        new = f.read()

    assert new == original
    assert capsys.readouterr().out.strip() == "Round-trip successful: files are identical"
