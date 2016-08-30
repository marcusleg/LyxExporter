#!/usr/bin/python3.5
"""
The MIT License (MIT)

Copyright (c) 2015 Marcus Legendre

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import argparse
import sys
from lyxexporter.scanner import Scanner
from lyxexporter.print import Print


def platform_check():
    if sys.platform == "win32":
        sys.exit("This programm is not compatible with Windows")
    return True

def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('path', nargs='?', default=".")
    parser.add_argument("-v", "--verbose",
                        help="increase output verbosity",
                        action="store_true")
    return parser.parse_args(args)

def main():
    platform_check()
    cli_args = parse_args(sys.argv[1:])

    try:
        scanner = Scanner(cli_args)
    except NotADirectoryError:
        Print.invalid_directory()
        sys.exit(1)

    scanner.scan()
    scanner.check_exports()
    scanner.print_report()
    scanner.prompt_export()

if __name__ == "__main__":
    main()
