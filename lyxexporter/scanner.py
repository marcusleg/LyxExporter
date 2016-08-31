import sys
import os
from lyxexporter.lyxfile import LyxFile
from lyxexporter.print import Print


class Scanner:
    """scans the given directory for *.lyx files """
    def __init__(self, cli_args):
        self.files = []
        self.outdated_files = []
        self.notexported_files = []
        self.cli_args = cli_args
        self.check_valid_path()

    def check_valid_path(self):
        if not os.path.isdir(self.cli_args.path):
            raise NotADirectoryError("Invalid directory")

    def scan(self):
        """populates the "files" array with all *.lyx files """
        if self.cli_args.verbose:
            Print.scanning_directory(self.cli_args.path)

        for root, dirs, files in os.walk(self.cli_args.path):
            for name in files:
                if not name.endswith('.lyx'):
                    continue
                f = LyxFile(os.path.join(root, name))
                self.files.append(f)

    def check_exports(self):
        """checks the "files" array for Lyx files that were not exported to PDF
        and PDFs that are older than the Lyx file"""
        if len(self.files) == 0:
            Print.no_lyx_files_found()
            sys.exit()

        for filename in self.files:
            if not filename.is_exported():
                Print.not_exported(str(filename))
                self.notexported_files.append(filename)
            elif filename.is_outdated():
                Print.is_outdated(str(filename))
                self.outdated_files.append(filename)
            elif self.cli_args.verbose:
                Print.up_to_date(str(filename))

    def print_report(self):
        """prints how many files were scanned, and how many of those were not
        exported yet or are outdated"""
        Print.num_files_scanned(len(self.files))

        if len(self.notexported_files) > 0:
            Print.num_not_exported(len(self.notexported_files))
        if len(self.outdated_files) > 0:
            Print.num_outdated(len(self.outdated_files))
        if len(self.notexported_files) == 0 and len(self.outdated_files) == 0:
            Print.everything_up_to_date()

        Print.linebreak()

    def prompt_export(self):
        """exports outdated/unexported files if users chooses to"""
        if len(self.notexported_files) == 0 and len(self.outdated_files) == 0:
            return False

        choice = input("\nDo you want to export all missing and outdated PDFs"
                       + " now? [y/N] ")
        if choice.lower() in ["y", "yes"]:
            for lyxfile in self.notexported_files + self.outdated_files:
                lyxfile.export()
        return True
