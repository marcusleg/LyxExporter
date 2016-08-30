import unittest
from unittest.mock import patch, call

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

    @patch('lyxexporter.lyxfile.LyxFile.__init__')
    @patch('lyxexporter.scanner.os.walk')
    def test_scan_lyxfile_object_creation(self, mock_sd, mock_lf):
        mock_sd.return_value = [['.', [], ['document.lyx']]]
        mock_lf.return_value = None
        self.scanner.scan()
        mock_lf.assert_called_once_with('./document.lyx')

    @patch('lyxexporter.scanner.os.walk')
    def test_scan_empty_dir(self, mock):
        mock.return_value = []
        self.scanner.scan()
        self.assertEqual(len(self.scanner.files), 0)

    @patch('lyxexporter.scanner.os.walk')
    def test_scan_single_lyx_file(self, mock):
        mock.return_value = [['.', [], ['document.lyx']]]
        self.scanner.scan()
        self.assertEqual(len(self.scanner.files), 1)

    @patch('lyxexporter.scanner.os.walk')
    def test_scan_single_nonlyx_file(self, mock):
        mock.return_value = [['.', [], ['document.doc']]]
        self.scanner.scan()
        self.assertEqual(len(self.scanner.files), 0)

    @patch('lyxexporter.lyxfile.LyxFile.__init__')
    @patch('lyxexporter.scanner.os.walk')
    def test_scan_fixture(self, mock_sd, mock_lf):
        mock_sd.return_value = [
            ['dir1/', [], ['a.lyx', 'a.pdf']],
            ['dir2/', [], ['b.lyx', 'c.xls']]
        ]
        mock_lf.return_value = None
        self.scanner.scan()
        calls = [call('dir1/a.lyx'), call('dir2/b.lyx')]
        mock_lf.assert_has_calls(calls)
        self.assertEqual(len(self.scanner.files), 2)

    def test_check_exports_no_files_found(self):
        self.scanner.files = []
        with self.assertRaises(SystemExit):
            self.scanner.check_exports()


if __name__ == '__main__':
    unittest.main()