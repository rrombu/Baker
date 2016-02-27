# Setup script for Py2Exe
# Usage: in console write "py setup.py py2exe" and get the results at "dist" folder
from distutils.core import setup
from shutil import rmtree
import py2exe

setup(
    windows=['baker.py'],
    zipfile=None,
    options={'py2exe': {'includes': ['sip', 'PyQt4.QtCore', 'PyQt4.QtGui'],
                        'bundle_files': 1, 'compressed': True}},
    name='Baker',
    version='1.0',
    packages=[''],
    url='',
    license='',
    author='Roman Budnik',
    author_email='',
    description='Anime convert and repack utility'
)

rmtree('build')
rmtree('__pycache__')
