import os
import subprocess
from lyxexporter.print import Print


class TexFile:
    """Tex file object"""
    def __init__(self, location):
        self.tex_file = location
        self.pdf_file = location[:-4] + '.pdf'

    def __str__(self):
        return self.tex_file

    def is_exported(self):
        """checks if Tex file was exported to PDF"""
        return True if os.path.isfile(self.pdf_file) else False

    def is_outdated(self):
        """checks if the PDF is older than the Tex file"""
        tex_timestamp = os.path.getmtime(self.tex_file)
        pdf_timestamp = os.path.getmtime(self.pdf_file)
        return True if tex_timestamp > pdf_timestamp else False

    def export(self):
        """exports the Tex file to PDF"""
        try:
            devnull = open(os.devnull, "w")
            print("pdflatex -interaction nonstopmode -output-directory \""
                  + os.path.dirname(self.tex_file) + "\" \""
                  + str(self.tex_file) + "\"")
            subprocess.check_call(
                ["pdflatex -interaction nonstopmode -output-directory \""
                 + os.path.dirname(self.tex_file) + "\" \""
                 + str(self.tex_file) + "\""],
                shell=True, stdout=devnull, stderr=devnull)
            devnull.close()
        except subprocess.CalledProcessError:
            Print.export_failed(str(self))
        else:
            Print.export_successful(str(self))

        return True if self.is_exported and not self.is_outdated else False
