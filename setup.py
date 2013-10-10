import os
import glob
from distutils.core import setup

modules = list(map(lambda d: d[:-3], glob.glob(os.path.join('*.py'))))
modules.remove('setup')

setup(name="openmensa-parsers",
      version="1.0",
      description="A collection with parsers for openmensa",
      author="Malte Swart",
      author_email="mswart@devtation.de",
      url="https://github.com/mswart/openmensa-parsers.git",
      py_modules=modules + ['pyopenmensa/__init__', 'pyopenmensa/feed'])
