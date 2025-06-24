import importlib
import pathlib
import httpimport
import pytest

REMOTE_URL = 'https://raw.githubusercontent.com/TakashiSasaki/efu/refs/heads/main/src/'

@pytest.fixture(scope='session')
def remote_efu():
    with httpimport.remote_repo(url=REMOTE_URL):
        module = importlib.import_module('efu_csv_utils')
    return module


def test_parse_efu_simple_remote(tmp_path, remote_efu):
    parse_efu = remote_efu.efu_to_array

    csv_content = (
        "Filename,Size,Date Modified,Date Created,Attributes\r\n"
        "\"C:\\msys64\",,133876022280081366,133739602603410395,16\r\n"
        "\"C:\\msys64\\autorebase.bat\",82,133262362720000000,133739602600000000,32\r\n"
        "\"C:\\msys64\\clang64\",0,133665511886007850,133665511886007850,16\r\n"
    )

    sample_file = tmp_path / 'sample.efu'
    sample_file.write_text(csv_content, newline='')

    rows, header, nl = parse_efu(str(sample_file))

    assert header == [
        'Filename',
        'Size',
        'Date Modified',
        'Date Created',
        'Attributes',
    ]
    assert rows == [
        ['C:\\msys64', '', '133876022280081366', '133739602603410395', '16'],
        [
            'C:\\msys64\\autorebase.bat',
            '82',
            '133262362720000000',
            '133739602600000000',
            '32',
        ],
        [
            'C:\\msys64\\clang64',
            '0',
            '133665511886007850',
            '133665511886007850',
            '16',
        ],
    ]
    assert nl == '\r\n'


def test_write_efu_simple_remote(tmp_path, remote_efu):
    write_efu = remote_efu.array_to_efu

    header = [
        'Filename',
        'Size',
        'Date Modified',
        'Date Created',
        'Attributes',
    ]
    rows = [
        ['C:\\msys64', '', '133876022280081366', '133739602603410395', '16'],
        [
            'C:\\msys64\\autorebase.bat',
            '82',
            '133262362720000000',
            '133739602600000000',
            '32',
        ],
        [
            'C:\\msys64\\clang64',
            '0',
            '133665511886007850',
            '133665511886007850',
            '16',
        ],
    ]

    out_file = tmp_path / 'out.efu'
    write_efu(rows, header, str(out_file), newline='\r\n')

    expected = (
        'Filename,Size,Date Modified,Date Created,Attributes\r\n'
        '\"C:\\msys64\",,133876022280081366,133739602603410395,16\r\n'
        '\"C:\\msys64\\autorebase.bat\",82,133262362720000000,133739602600000000,32\r\n'
        '\"C:\\msys64\\clang64\",0,133665511886007850,133665511886007850,16\r\n'
    )

    with open(out_file, 'r', newline='') as f:
        content = f.read()
    assert content == expected


def test_objects_to_efu_remote(tmp_path, remote_efu):
    objects_to_efu = remote_efu.objects_to_efu

    objs = [
        {
            'Filename': 'C:\\msys64',
            'Size': None,
            'Date Modified': 133876022280081366,
            'Date Created': 133739602603410395,
            'Attributes': 16,
        },
        {
            'Filename': 'C:\\msys64\\autorebase.bat',
            'Size': 82,
            'Date Modified': 133262362720000000,
            'Date Created': 133739602600000000,
            'Attributes': 32,
        },
        {
            'Filename': 'C:\\msys64\\clang64',
            'Size': 0,
            'Date Modified': 133665511886007850,
            'Date Created': 133665511886007850,
            'Attributes': 16,
        },
    ]

    out_file = tmp_path / 'out.efu'
    objects_to_efu(objs, str(out_file), newline='\r\n')

    expected = (
        'Filename,Size,Date Modified,Date Created,Attributes\r\n'
        '\"C:\\msys64\",,133876022280081366,133739602603410395,16\r\n'
        '\"C:\\msys64\\autorebase.bat\",82,133262362720000000,133739602600000000,32\r\n'
        '\"C:\\msys64\\clang64\",0,133665511886007850,133665511886007850,16\r\n'
    )

    with open(out_file, 'r', newline='') as f:
        content = f.read()
    assert content == expected


def test_efu_to_objects_remote(tmp_path, remote_efu):
    efu_to_objects = remote_efu.efu_to_objects

    csv_content = (
        'Filename,Size,Date Modified,Date Created,Attributes\r\n'
        '\"C:\\msys64\",,133876022280081366,133739602603410395,16\r\n'
        '\"C:\\msys64\\autorebase.bat\",82,133262362720000000,133739602600000000,32\r\n'
        '\"C:\\msys64\\clang64\",0,133665511886007850,133665511886007850,16\r\n'
    )
    sample_file = tmp_path / 'sample.efu'
    sample_file.write_text(csv_content, newline='')

    objs = efu_to_objects(str(sample_file))

    assert objs == [
        {
            'Filename': 'C:\\msys64',
            'Size': None,
            'Date Modified': 133876022280081366,
            'Date Created': 133739602603410395,
            'Attributes': 16,
        },
        {
            'Filename': 'C:\\msys64\\autorebase.bat',
            'Size': 82,
            'Date Modified': 133262362720000000,
            'Date Created': 133739602600000000,
            'Attributes': 32,
        },
        {
            'Filename': 'C:\\msys64\\clang64',
            'Size': 0,
            'Date Modified': 133665511886007850,
            'Date Created': 133665511886007850,
            'Attributes': 16,
        },
    ]


def test_roundtrip_remote(tmp_path, remote_efu):
    parse_efu = remote_efu.efu_to_array
    write_efu = remote_efu.array_to_efu
    root = pathlib.Path(__file__).resolve().parents[1]
    sample = root / 'samples' / 'sample1.efu'

    rows, header_fields, nl = parse_efu(str(sample))
    out_file = tmp_path / 'out.efu'
    write_efu(rows, header_fields, str(out_file), newline=nl)

    with open(sample, 'rb') as f:
        original = f.read()
    with open(out_file, 'rb') as f:
        new = f.read()

    assert original == new

