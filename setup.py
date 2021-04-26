# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in custext/__init__.py
from custext import __version__ as version

setup(
	name='custext',
	version=version,
	description='ERPNext custom extension modules',
	author='VAlignIt',
	author_email='ghouseam@valignit.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
