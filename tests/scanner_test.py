import unittest
from unittest.mock import patch

from lyxexporter.cli import parse_args
from lyxexporter.scanner import Scanner

class TestScanner(unittest.TestCase):
    def setUp(self):
        cli_args = parse_args([])
        self.scanner = Scanner(cli_args)

    @patch('lyxexporter.scanner.os.path')
    def test_check_valid_path(self, mock):
        mock.isdir.return_value = False
        with self.assertRaises(NotADirectoryError):
            self.scanner.check_valid_path()

    def test_check_exports_no_files_found(self):
        self.scanner.files = []
        with self.assertRaises(SystemExit):
            self.scanner.check_exports()
