LyxExporter
===========

This CLI utility program helps you keeping your PDFs exports from the
`Lyx Document Processor <http://www.lyx.org>` up to date.
It scans a given directory for *.lyx files and checks if they have
been exported to PDF and if the PDFs are older than the Lyx file they are based
on. If any any PDFs are missing or outdated the user will be prompted with the
choice to let the program export them.

Quickstart
----------
.. sourcecode:: console

    # pip3 install https://github.com/OrangeFoil/LyxExporter/archive/master.zip
    $ lyxexporter
    [Not exported] /home/orangefoil/sample1.lyx
    [  Outdated  ] /home/orangefoil/sample2.lyx
    23 files scanned. [1 not exported] [1 outdated]

    Do you want to export all missing and outdated PDFs now? [y/N] y
    Export successful /home/orangefoil/Dropbox/FH/sample1.lyx
    Export successful /home/orangefoil/Dropbox/FH/sample2.lyx
