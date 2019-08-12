#!/usr/bin/env python
from os.path import join

from setuptools import setup, find_packages


MODULE_NAME = 'portiapy'
REPO_NAME = 'portiapy'


with open('../README.md') as f:
    readme = f.read()


setup(
    name=MODULE_NAME,
    description='A small package for handling Agriness Edge\'s REST API',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/AgrinessEdgeIoT/{:s}'.format(REPO_NAME),
    author='Matheus Mota, Lucas Góes',
    author_email='matheus@agrinessedge.com, lucas@agrinessedge.com',
    packages=find_packages(exclude=('tests', 'docs')),
    version=open(join(MODULE_NAME, 'VERSION')).read().strip(),
    install_requires=['requests>=2.20.0', 'pytz>=2018.5',
                      'python-dateutil>=2.7.3', 'plotly>=3.1.1',
                      'pandas>=0.23.4', 'arrow>=0.12.1'],
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ),
    data_files=[('VERSION', [join(MODULE_NAME, 'VERSION')])]
)
