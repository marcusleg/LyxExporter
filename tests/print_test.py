import unittest

from lyxexporter.print import Print

class TestPrint(unittest.TestCase):
    def test_format_no_formatting(self):
        message = Print.format("some text")
        self.assertEqual(message, "some text")

    def test_format_invalid_color(self):
        message = Print.format("some text", color='notacolor')
        self.assertEqual(message, "some text")

    def test_format_color_red(self):
        message = Print.format("text", color='ReD')
        self.assertAlmostEqual(message, "\033[91mtext\033[0m")

    def test_format_bold(self):
        message = Print.format("text", bold=True)
        self.assertAlmostEqual(message, "\033[1mtext\033[0m")

    def test_format_underline(self):
        message = Print.format("text", underline=True)
        self.assertAlmostEqual(message, "\033[4mtext\033[0m")

    def test_format_blue_bold_underline(self):
        message = Print.format("text", color='BLUE', bold=True, underline=True)
        self.assertAlmostEqual(message, "\033[4m\033[1m\033[94mtext\033[0m")


if __name__ == '__main__':
    unittest.main()
