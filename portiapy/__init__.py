"""
PortiaPy
========

A Python stub for Agriness Edge's Portia REST API. 

__authors__ = ['Lucas Góes', 'Matheus Mota']
__emails__ = ['lucas@agrinessedge.com', 'matheus@agrinessedge.com']
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
