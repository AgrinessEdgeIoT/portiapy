#!/usr/bin/env python
from os.path import join

from setuptools import setup, find_packages


MODULE_NAME = 'portiapy'
REPO_NAME = 'portiapy'


with open('./README.md') as f:
    readme = f.read()


setup(
    name=MODULE_NAME,
    description='A small package for handling Agriness Edge\'s REST API',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/AgrinessEdgeIoT/{:s}'.format(REPO_NAME),
    author='Matheus Mota, Lucas Góes',
    author_email='matheus@agrinessedge.com, lucas@agrinessedge.com',
    packages=find_packages(exclude=('binder', 'tests', 'docs')),
    version=open(join(MODULE_NAME, 'VERSION')).read().strip(),
    install_requires=[
        'arrow>=1.2.3',
        'pandas>=1.5.3',
        'plotly>=5.13.1',
        'python-dateutil>=2.8.2',
        'python-dotenv>=1.0.0',
        'pytz>=2022.7.1',
        'requests>=2.28.2'
    ],
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ),
    include_package_data=True
)
