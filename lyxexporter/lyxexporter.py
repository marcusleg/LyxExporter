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
from pathlib import Path
import subprocess


# command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('path', nargs='?', default=".")
parser.add_argument("-v", "--verbose",
                    help="increase output verbosity",
                    action="store_true")
args = parser.parse_args()


class BC:
    """helper class that holds variables for bash colours"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class LyxFile:
    """Lyx file object"""
    def __init__(self, location):
        self.lyx_file = Path(location)
        self.pdf_file = Path(str(self.lyx_file)[:-3] + "pdf")

    def __str__(self):
        return str(self.lyx_file.resolve())

    def is_exported(self):
        """checks if Lyx file was exported to PDF"""
        return True if self.pdf_file.exists() else False

    def is_outdated(self):
        """checks if the PDF is older than the Lyx file"""
        if self.pdf_file.stat().st_mtime < self.lyx_file.stat().st_mtime:
            return True
        else:
            return False

    def export(self):
        """exports the Lyx file to PDF"""
        try:
            subprocess.check_call(["lyx -e pdf \"" + str(self.lyx_file)
                                  + "\""], shell=True)
        except subprocess.CalledProcessError as error:
            print(BC.RED + "Export failed " + BC.ENDC + str(self))
        else:
            print(BC.GREEN + "Export successful " + BC.ENDC
                  + str(self))

        return True if self.is_exported and not self.is_outdated else False



class Scanner:
    """scans the given directory for *.lyx files """
    files = []
    outdated_files = []
    notexported_files = []

    def __init__(self, path):
        self.path = Path(path)

        if not self.path.exists():
            raise NotADirectoryError(BC.RED + "Invalid directory" + BC.ENDC)

        self.scan()

    def scan(self):
        """populates the "files" array with all *.lyx files """
        if args.verbose:
            print("Scanning \"" + str(self.path.resolve()) + "\" "
                  +"for Lyx files...")

        for file in list(self.path.glob('**/*.lyx')):
            f = LyxFile(file)
            self.files.append(f)

    def check_exports(self):
        """checks the "files" array for Lyx files that were not exported to PDF
        and PDFs that are older than the Lyx file"""
        if len(self.files) == 0:
            print(BC.BLUE + "no Lyx files found" + BC.ENDC)
            sys.exit()

        for file in self.files:
            if not file.is_exported():
                print("[" + BC.RED + "Not exported" + BC.ENDC + "] "
                      + str(file))
                self.notexported_files.append(file)
            elif file.is_outdated():
                print("[  " + BC.YELLOW + "Outdated" + BC.ENDC + "  ] "
                      + str(file))
                self.outdated_files.append(file)
            elif args.verbose:
                print("[ " + BC.GREEN + "Up-to-date" + BC.ENDC + " ] "
                      + str(file))

    def print_report(self):
        """prints how many files were scanned, and how many of those were not
        exported yet or are outdated"""
        print(BC.BOLD + str(len(self.files)) + " files scanned" + BC.ENDC,
              end=". ")

        if len(self.notexported_files) > 0:
            print("[" + BC.BOLD + str(len(self.notexported_files)) + BC.ENDC
                  + BC.RED + " not exported" + BC.ENDC + "]",
                  end=" ")
        if len(self.outdated_files) > 0:
            print("[" + BC.BOLD + str(len(self.outdated_files)) + BC.ENDC
                  + BC.YELLOW + " outdated" + BC.ENDC + "]", end="")
        if len(self.notexported_files) == 0 and len(self.outdated_files) == 0:
            print(BC.GREEN + "All PDFs are exported and up-to-date" + BC.ENDC,
                  end="")

        print("")

    def prompt_export(self):
        """exports outdated/unexported files if users chooses to"""
        if len(self.notexported_files) == 0 and len(self.outdated_files) == 0:
            return

        choice = input("\nDo you want to export all missing and outdated PDFs"
                       + " now? [y/N] ")
        if choice.lower() in ["y", "yes"]:
            for file in self.notexported_files + self.outdated_files:
                file.export()


def main():
    scanner = Scanner(args.path)
    scanner.check_exports()
    scanner.print_report()
    scanner.prompt_export()

if __name__ == "__main__":
    main()
