from pathlib import Path
import sys
from lyxexporter.bc import BC
from lyxexporter.lyxfile import LyxFile


class Scanner:
    """scans the given directory for *.lyx files """
    files = []
    outdated_files = []
    notexported_files = []

    def __init__(self, cli_args):
        self.cli_args = cli_args
        self.path = Path(self.cli_args.path)

        if not self.path.exists():
            raise NotADirectoryError("Invalid directory")

        self.scan()

    def scan(self):
        """populates the "files" array with all *.lyx files """
        if self.cli_args.verbose:
            print("Scanning \"" + str(self.path.resolve()) + "\" "
                  + "for Lyx files...")

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
