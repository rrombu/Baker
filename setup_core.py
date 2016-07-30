# Setup script for Py2Exe
# Usage: in console write "py setup_core.py py2exe" and get the results at "dist" folder
from distutils.core import setup
from shutil import rmtree
import py2exe

version = '0.9.5'
author = 'Roman Budnik'
author_email = ''
description = 'Anime convert and repack tool'

setup(
    console=[{"script":'baker.py', "dest_base":"baker_core"}],
    zipfile=None,
    options={'py2exe': {'includes': ["sip"],
                        'bundle_files': 1, 'compressed': True}},
    name='Baker Core',
    version=version,
    author=author,
    description=description,
    packages=[''], url='', license='', author_email=''
)


rmtree('build')
rmtree('__pycache__')
