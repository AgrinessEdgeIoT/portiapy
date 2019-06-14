from setuptools import setup, find_packages

__version__ = '1.1.6'

with open('../README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='portiapy',
    version=__version__,
    author='Matheus Mota, Lucas Góes',
    description='A small package for handling Agriness Edge\'s REST API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/AgrinessEdgeIoT/portiapy',
    packages=find_packages(),
    install_requires=['requests>=2.20.0', 'pytz>=2018.5', 'python-dateutil>=2.7.3', 'plotly>=3.1.1', 'pandas>=0.23.4', 'arrow>=0.12.1'],
    #scripts=['portia'],
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ),
)
