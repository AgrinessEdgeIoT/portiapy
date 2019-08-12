"""A small package for handling Agriness Edge's REST API.

Functions: about, version
"""

from .version import __version__


__all__ = ['axioms', 'describe', 'phases', 'portia', 'profile', 'select',
		   'specs', 'summary', 'utils']


name = 'portiapy'

portiaConfigExample = {
	'baseurl': 'http://localhost',
	'authorization': '<your API key>',
	'debug': False,
	'Accept': 'text/csv'
}

NAME = name

PORTIA_CONFIG_EXAMPLE = portiaConfigExample


def about():
    print('portiapy - an Agriness Edge project')

def version():
	print('portiapy - v{0}'.format(__version__))
