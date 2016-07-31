# Setup script for Py2Exe
# Usage: in console write "py setup.py py2exe" and get the results at "dist" folder
from distutils.core import setup
from shutil import rmtree, copyfile
import py2exe

version = '0.9.7'
author = 'Roman Budnik'
author_email = ''
description = 'Anime convert and repack tool'

setup(
    windows=[{"script": 'main.py', "dest_base": "baker"}],
    zipfile=None,
    options={'py2exe': {'includes': ['sip', 'PyQt4.QtCore', 'PyQt4.QtGui'],
                        'bundle_files': 1, 'compressed': True}},
    name='Baker',
    version=version,
    author=author,
    description=description,
    packages=[''], url='', license='', author_email=''
)

copyfile("config.json", "dist\\config.json")
copyfile("README.md", "dist\\README.md")
rmtree('build')
rmtree('__pycache__')
