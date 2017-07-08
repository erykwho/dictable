import os
from setuptools import setup


# Utility function to read the README file.  
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='dict-table',
      long_description=read('README.md'),
      version='0.0.1',
      author='Eryk Humberto Oliveira Alves',
      author_email='erykwho@gmail.com',
      url='https://github.com/otrabalhador/dict-table/',
      packages=['dict_table', 'dict_table.utils'],
      keywords='dict table query',
      classifiers=[
          "Topic :: Utilities",
      ])