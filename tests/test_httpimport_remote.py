import importlib
import httpimport


def test_import_remote_efu_module():
    url = 'https://raw.githubusercontent.com/TakashiSasaki/efu/refs/heads/main/src/'
    with httpimport.remote_repo(url=url):
        module = importlib.import_module('efu')
        assert hasattr(module, '__version__')
        assert module.__version__ == '0.1.1'
