from pathlib import Path
import subprocess
from lyxexporter.bc import BC


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
            subprocess.check_call(["lyx -e pdf2 \"" + str(self.lyx_file)
                                  + "\""], shell=True)
        except subprocess.CalledProcessError:
            print(BC.RED + "Export failed " + BC.ENDC + str(self))
        else:
            print(BC.GREEN + "Export successful " + BC.ENDC + str(self))

        return True if self.is_exported and not self.is_outdated else False
