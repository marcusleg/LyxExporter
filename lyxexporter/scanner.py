import sys
import os
from lyxexporter.bc import BC
from lyxexporter.lyxfile import LyxFile


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
            print("Scanning \"" + str(self.cli_args.path) + "\" "
                  + "for Lyx files...")

        for root, dirs, files in os.walk(self.cli_args.path):
            for name in files:
                if not name.endswith('.lyx'): continue
                f = LyxFile(os.path.join(root, name))
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
            elif self.cli_args.verbose:
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
