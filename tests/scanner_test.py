import unittest
from unittest.mock import patch, call

from lyxexporter.cli import parse_args
from lyxexporter.scanner import Scanner
from tests.mock_dir_entry import MockDirEntry

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
    @patch('lyxexporter.scanner.os.scandir')
    def test_scan_lyxfile_object_creation(self, mock_sd, mock_lf):
        mock_sd.return_value = MockDirEntry.make(['document.lyx'])
        mock_lf.return_value = None
        self.scanner.scan()
        mock_lf.assert_called_once_with('document.lyx')

    @patch('lyxexporter.scanner.os.scandir')
    def test_scan_empty_dir(self, mock):
        mock.return_value = []
        self.scanner.scan()
        self.assertEqual(len(self.scanner.files), 0)

    @patch('lyxexporter.scanner.os.scandir')
    def test_scan_single_lyx_file(self, mock):
        mock.return_value = MockDirEntry.make(['document.lyx'])
        self.scanner.scan()
        self.assertEqual(len(self.scanner.files), 1)

    @patch('lyxexporter.scanner.os.scandir')
    def test_scan_single_directory(self, mock):
        mock.return_value = MockDirEntry.make(['asd/'])
        self.scanner.scan()
        self.assertEqual(len(self.scanner.files), 0)

    @patch('lyxexporter.scanner.os.scandir')
    def test_scan_single_nonlyx_file(self, mock):
        mock.return_value = MockDirEntry.make(['document.doc'])
        self.scanner.scan()
        self.assertEqual(len(self.scanner.files), 0)

    @patch('lyxexporter.lyxfile.LyxFile.__init__')
    @patch('lyxexporter.scanner.os.scandir')
    def test_scan_fixture(self, mock_sd, mock_lf):
        fixture = ['dir1/', 'dir1/a.lyx', 'dir1/a.pdf', 'dir1/b.lyx'] 
        mock_sd.return_value = MockDirEntry.make(fixture)
        mock_lf.return_value = None
        self.scanner.scan()
        calls = [call('dir1/a.lyx'), call('dir1/b.lyx')]
        mock_lf.assert_has_calls(calls)
        self.assertEqual(len(self.scanner.files), 2)

    def test_check_exports_no_files_found(self):
        self.scanner.files = []
        with self.assertRaises(SystemExit):
            self.scanner.check_exports()


if __name__ == '__main__':
    unittest.main()