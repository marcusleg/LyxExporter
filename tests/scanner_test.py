import unittest
from unittest.mock import patch, call, MagicMock

from lyxexporter.cli import parse_args
from lyxexporter.scanner import Scanner


def mock_lyxfile(location, exported, outdated):
    """Returns mocked Lyxfile object"""
    mock = MagicMock()
    mock.__str__.return_value = location
    mock.is_exported.return_value = exported
    mock.is_outdated.return_value = outdated
    return mock


class TestScanner(unittest.TestCase):
    def setUp(self):
        cli_args = parse_args([])
        self.scanner = Scanner(cli_args)

    @patch('lyxexporter.scanner.os.path')
    def test_check_valid_path(self, mock):
        mock.isdir.return_value = False
        with self.assertRaises(NotADirectoryError):
            self.scanner.check_valid_path()

    @patch('lyxexporter.print.Print.scanning_directory')
    @patch('lyxexporter.scanner.os.path.isdir')
    @patch('lyxexporter.scanner.os.walk')
    def test_scan_verbose_print(self, mock_ow, mock_op, mock_p):
        mock_ow.return_value = []
        mock_op.return_value = True
        scanner = Scanner(parse_args(['-v', 'somedir/']))
        scanner.scan()
        mock_p.assert_called_once_with('somedir/')

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

    @patch('lyxexporter.print.Print.no_lyx_files_found')
    def test_check_exports_no_files_found(self, mock):
        self.scanner.files = []
        with self.assertRaises(SystemExit):
            self.scanner.check_exports()
        mock.assert_called_once_with()

    @patch('lyxexporter.print.Print.not_exported')
    def test_check_exports_1_file_not_exported(self, mock_p):
        mock_lf = mock_lyxfile('abc.lyx', False, False)
        self.scanner.files.append(mock_lf)
        self.scanner.check_exports()
        self.assertEqual(len(self.scanner.notexported_files), 1)
        self.assertEqual(len(self.scanner.outdated_files), 0)
        mock_p.assert_called_once_with('abc.lyx')

    @patch('lyxexporter.print.Print.is_outdated')
    def test_check_exports_1_file_outdated(self, mock_p):
        mock_lf = mock_lyxfile('abc.lyx', True, True)
        self.scanner.files.append(mock_lf)
        self.scanner.check_exports()
        self.assertEqual(len(self.scanner.notexported_files), 0)
        self.assertEqual(len(self.scanner.outdated_files), 1)
        mock_p.assert_called_once_with('abc.lyx')

    @patch('lyxexporter.print.Print.is_outdated')
    def test_check_exports_1_file_up2date(self, mock_p):
        mock_lf = mock_lyxfile('abc.lyx', True, False)
        self.scanner.files.append(mock_lf)
        self.scanner.check_exports()
        self.assertEqual(len(self.scanner.notexported_files), 0)
        self.assertEqual(len(self.scanner.outdated_files), 0)

    @patch('lyxexporter.print.Print.linebreak')
    @patch('lyxexporter.print.Print.everything_up_to_date')
    @patch('lyxexporter.print.Print.num_files_scanned')
    def test_print_report_nothing_to_do(self, mock1, mock2, mock3):
        self.scanner.print_report()
        mock1.assert_called_once_with(0)
        mock2.assert_called_once_with()
        mock3.assert_called_once_with()

    @patch('lyxexporter.print.Print.linebreak')
    @patch('lyxexporter.print.Print.num_not_exported')
    @patch('lyxexporter.print.Print.num_outdated')
    @patch('lyxexporter.print.Print.num_files_scanned')
    def test_print_report_2_files(self, mock_pnfs, mock_po, mock_pnne, mock_lb):
        mockfile1 = mock_lyxfile('a.lyx', False, False)
        mockfile2 = mock_lyxfile('b.lyx', True, False)
        self.scanner.files.append(mockfile1)
        self.scanner.files.append(mockfile2)
        self.scanner.notexported_files.append(mockfile1)
        self.scanner.outdated_files.append(mockfile2)
        self.scanner.print_report()
        mock_pnfs.assert_called_once_with(2)
        mock_po.assert_called_once_with(1)
        mock_pnne.assert_called_once_with(1)
        mock_lb.assert_called_once_with()

    def test_prompt_export_nothing_to_do(self):
        self.assertFalse(self.scanner.prompt_export())

    @patch('lyxexporter.scanner.input')
    def test_prompt_export_user_input(self, mock_i):
        mock_i.return_value = 'n'
        mock_lf = mock_lyxfile('abc.lyx', False, False)
        self.scanner.notexported_files.append(mock_lf)
        self.assertTrue(self.scanner.prompt_export())
        self.assertTrue(mock_i.called)

    @patch('lyxexporter.scanner.input')
    def test_prompt_export_1_file_not_exported_input_no(self, mock_i):
        mock_i.return_value = 'n'
        mock_lf = mock_lyxfile('abc.lyx', False, False)
        self.scanner.notexported_files.append(mock_lf)
        self.scanner.prompt_export()
        mock_lf.export.assert_not_called()

    @patch('lyxexporter.scanner.input')
    def test_prompt_export_1_file_not_exported_input_yes(self, mock_i):
        mock_i.return_value = 'Y'
        mock_lf = mock_lyxfile('abc.lyx', False, False)
        self.scanner.notexported_files.append(mock_lf)
        self.scanner.prompt_export()
        mock_lf.export.assert_called_once_with()

    @patch('lyxexporter.scanner.input')
    def test_prompt_export_1_file_outdated_input_yes(self, mock_i):
        mock_i.return_value = 'yes'
        mock_lf = mock_lyxfile('abc.lyx', True, False)
        self.scanner.outdated_files.append(mock_lf)
        self.scanner.prompt_export()
        mock_lf.export.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()
