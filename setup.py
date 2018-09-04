from setuptools import setup, find_packages

__version__ = '1.0.0'

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='portiapy',
    version=__version__,
    author='Matheus Mota, Lucas Góes',
    author_email='matheus@agrinessedge.com, lucas@agrinessedge.com',
    description='A small package for handling Agriness Edge rest API',
    long_description=long_description,
    url='https://github.com/agrinessedge/edge-playground',
    packages=find_packages(),
    setup_requires=['requests>=2.19.1', 'pytz>=2018.5', 'python-dateutil>=2.7.3', 'plotly>=3.1.1', 'pandas>=0.23.4', 'arrow>=0.12.1'],
    #scripts=['portia'],
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ),
)
