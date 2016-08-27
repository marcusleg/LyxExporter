"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='lyxexporter',
    version='1.0.1dev',
    description='Scans a directory for *.lyx files and makes sure they are '
                + 'exported to PDF',
    long_description=long_description,
    url='https://github.com/OrangeFoil/LyxExporter',
    author='Marcus Legendre',
    author_email='marcus.legendre@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',

        'Environment :: Console',

        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',

        'Operating System :: POSIX',

        'Topic :: Text Processing :: Markup :: LaTeX',
        'Topic :: Utilities',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='latex lyx pdf export',
    packages=['lyxexporter'],
    install_requires=[],
    test_suite="tests",
    entry_points={
        'console_scripts': [
            'lyxexporter=lyxexporter.cli:main',
        ],
    },
)
