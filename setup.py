import re

from setuptools import setup


def version():
    version_file_name = "dictable/__init__.py"
    with open(version_file_name, 'rt') as version_file:
        version_file_content = version_file.read()

        version_regex = r"^__version__ = ['\"]([^'\"]*)['\"]"
        match = re.search(version_regex, version_file_content, re.M)
        if match:
            return match.group(1)
        else:
            raise RuntimeError("Unable to find version string in %s." % (version_file_name,))


setup(name='dictable',
      version=version(),
      author='Eryk Humberto Oliveira Alves',
      author_email='erykwho@gmail.com',
      url='https://github.com/otrabalhador/dictable/',
      packages=['dictable'],
      include_package_data=True,
      keywords='dict table query dictable dictsql table row list dictionary',
      classifiers=[
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          "Topic :: Utilities",
          'Topic :: Software Development :: Libraries :: Python Modules',
      ])
