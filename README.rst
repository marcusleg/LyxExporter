LyxExporter
===========

This CLI utility assists you in keeping your PDFs exports of your
`Lyx <http://www.lyx.org>`_ and Latex files up to date.

It scans a given directory for \*.lyx and \*.tex files and checks if their 
corresponding PDFs are present and up to date. If any PDFs are missing or outdated 
the user will be prompted with the choice to let the program export them.

Quickstart
----------
.. sourcecode:: console

    # pip3 install https://github.com/OrangeFoil/LyxExporter/archive/master.zip
    $ lyxexporter
    [Not exported] /home/orangefoil/sample1.lyx
    [  Outdated  ] /home/orangefoil/sample2.lyx
    23 files scanned. [1 not exported] [1 outdated]

    Do you want to export all missing and outdated PDFs now? [y/N] y
    Export successful /home/orangefoil/sample1.lyx
    Export successful /home/orangefoil/sample2.lyx
