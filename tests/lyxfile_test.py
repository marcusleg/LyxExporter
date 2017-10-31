import unittest
from unittest.mock import patch

from lyxexporter.lyxfile import LyxFile


class TestLyxFile(unittest.TestCase):
    cli_args = {'path': '.', 'lyx_only': False, 'tex_only': False,
                'verbose': False, 'version': False, 'yes': False}

    def test_init(self):
        lyxfile = LyxFile('somedir/abc.lyx', self.cli_args)
        self.assertEqual(lyxfile.lyx_file, 'somedir/abc.lyx')
        self.assertEqual(lyxfile.pdf_file, 'somedir/abc.pdf')

    def test_str(self):
        lyxfile = LyxFile('somedir/abc.lyx', self.cli_args)
        self.assertEqual(str(lyxfile), 'somedir/abc.lyx')

    @patch('lyxexporter.lyxfile.os.path.isfile')
    def test_is_exported_true(self, mock):
        mock.return_value = True
        lyxfile = LyxFile('somedir/abc.lyx', self.cli_args)
        self.assertTrue(lyxfile.is_exported())

    @patch('lyxexporter.lyxfile.os.path.isfile')
    def test_is_exported_false(self, mock):
        mock.return_value = False
        lyxfile = LyxFile('somedir/abc.lyx', self.cli_args)
        self.assertFalse(lyxfile.is_exported())

    @patch('lyxexporter.lyxfile.os.path.getmtime')
    def test_is_outdated_true(self, mock):
        def side_effected_outdated(filename):
            return 1 if filename[-3:] == 'pdf' else 2
        mock.side_effect = side_effected_outdated
        lyxfile = LyxFile('somedir/abc.lyx', self.cli_args)
        self.assertTrue(lyxfile.is_outdated())

    @patch('lyxexporter.lyxfile.os.path.getmtime')
    def test_is_outdated_false(self, mock):
        def side_effected_not_outdated(filename):
            return 2 if filename[-3:] == 'pdf' else 1
        mock.side_effect = side_effected_not_outdated
        lyxfile = LyxFile('somedir/abc.lyx', self.cli_args)
        self.assertFalse(lyxfile.is_outdated())

    @patch('lyxexporter.print.Print.export_successful')
    @patch('lyxexporter.lyxfile.subprocess.check_output')
    def test_export_successful(self, mock_sco, mock_p):
        lyxfile = LyxFile('somedir/abc.lyx', self.cli_args)
        lyxfile.export()
        self.assertTrue(mock_sco.called)
        mock_p.assert_called_once_with('somedir/abc.lyx')

    @patch('lyxexporter.print.Print.export_failed')
    @patch('lyxexporter.lyxfile.subprocess.check_output')
    def test_export_failed(self, mock_sco, mock_p):
        import subprocess
        mock_sco.side_effect = subprocess.CalledProcessError(1, '')
        lyxfile = LyxFile('somedir/abc.lyx', self.cli_args)
        self.assertFalse(lyxfile.export())
        self.assertTrue(mock_sco.called)
        mock_p.assert_called_once_with('somedir/abc.lyx')
