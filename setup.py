#!/usr/bin/env python
from distutils.core import setup
import os

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

with open(os.path.join(os.path.dirname(__file__), 'LICENSE')) as _license:
    LICENSE = _license.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(name='ipsetpy',
      license=LICENSE,
      version='v0.0.1a2',
      description='Python ipset bindings and helper',
      long_description=README,
      author='Sandor Attila Gerendi',
      author_email='python@gsaforge.com',
      url='https://github.com/sanyi/ipsetpy',
      packages=[
          'ipsetpy'
      ],
      package_dir={
          'ipsetpy': 'ipsetpy'
      },
      classifiers=[
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: POSIX',
          'Programming Language :: Python :: 3.4',
          ],

      data_files=[
          ('', ['LICENSE', 'README.md', 'TODO.md'])
      ],)
