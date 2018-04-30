# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.md') as f:
        readme = f.read()

with open('LICENSE.md') as f:
        license = f.read()

setup(
        name='DivaPythonTools',
        version='0.1.0',
        description='A set of Python tools to help users with: 1. The preparation of Diva input files: data, contours, parameters; 2. The execution of the Diva interpolation tool; 3. The reading of output files (analysis, finite-element mesh); 4. The input and output plotting.',
        long_description=readme,
        author='Charles Troupin',
        author_email='charles.troupin@gmail.com',
        url='https://github.com/gher-ulg/DivaPythonTools',
        license=license,
        packages=find_packages(exclude=('test', 'Notebooks', 'data', 'figures'))
)
