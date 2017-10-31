import os
import subprocess
from lyxexporter.print import Print


class LyxFile:
    """Lyx file object"""
    def __init__(self, location, cli_args):
        self.lyx_file = location
        self.pdf_file = location[:-4] + '.pdf'
        self.cli_args = cli_args

    def __str__(self):
        return self.lyx_file

    def is_exported(self):
        """checks if Lyx file was exported to PDF"""
        return True if os.path.isfile(self.pdf_file) else False

    def is_outdated(self):
        """checks if the PDF is older than the Lyx file"""
        lyx_timestamp = os.path.getmtime(self.lyx_file)
        pdf_timestamp = os.path.getmtime(self.pdf_file)
        return True if lyx_timestamp > pdf_timestamp else False

    def export(self):
        """exports the Lyx file to PDF"""
        try:
            subprocess.check_output(
                ["lyx -e pdf2 \"" + str(self.lyx_file) + "\""],
                shell=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as ex:
            Print.export_failed(str(self))
            if self.cli_args["verbose"]:
                print(ex.output.decode('ascii'))
        else:
            Print.export_successful(str(self))

        return True if self.is_exported and not self.is_outdated else False
