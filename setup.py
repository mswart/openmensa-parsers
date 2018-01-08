from distutils.core import setup

from setuptools import find_packages

setup(name="openmensa-parsers",
      version="1.0",
      description="A collection with parsers for openmensa",
      author="Malte Swart",
      author_email="mswart@devtation.de",
      url="https://github.com/mswart/openmensa-parsers.git",
      packages=find_packages(),
      py_modules=['parse', 'wsgihandler'],
      requires=['beautifulsoup4', 'lxml', 'pyopenmensa'])
