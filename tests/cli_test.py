import unittest

from lyxexporter.cli import *

class TestCLI(unittest.TestCase):
    def test_platform_check(self):
        sys.platform = 'win32'
        with self.assertRaises(SystemExit):
            platform_check()
        
        sys.platform = 'linux'
        self.assertTrue(platform_check())

    def test_parge_args(self):
        cli_args = parse_args([])
        self.assertEqual(cli_args.path, '.')
        self.assertFalse(cli_args.verbose)

        cli_args = parse_args(['-v'])
        self.assertTrue(cli_args.verbose)

        cli_args = parse_args(['some_directory/'])
        self.assertEqual(cli_args.path, 'some_directory/')
        

if __name__ == '__main__':
    unittest.main()