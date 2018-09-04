#####################################
#              Profile              #
#####################################

# Libraries
from enum import Enum             # Support for enumerations
import json                       # JSON encoder and decoder
import portiapy.utils as utils

# Enums
class ProfileStrategies(Enum):
	BY_ZERO_PORT = 1
	BY_PORTS     = 2

# Functions
def about():
    print("portiapy.profile - an Agriness Edge project")

def resolveStrategy(strategy):
    if strategy == ProfileStrategies.BY_ZERO_PORT:
        return 'byzeroport'
    else:
        return 'byports'

########################################
# deviceProfile
########################################
# /profile/device/:device/:strategy/:interval
########################################
def deviceProfile(portiaConfig, edgeId, strategy=ProfileStrategies.BY_ZERO_PORT, interval=30, params={ 'precision': 'ms', 'sort': True }):

    endpoint = '/profile/device/{0}/{1}/{2}{3}'.format( edgeId, resolveStrategy(strategy), interval, utils.buildGetParams(params) )
    response = utils.httpGetRequest(portiaConfig, endpoint)

    if response.status_code == 200:

        d = json.loads(response.text)
        if portiaConfig['debug']:
            print( '[portia-debug]: {0}'.format(d['ports']) )
        return d

    else:
        raise Exception('couldn\'t retrieve data')

########################################
# portProfile
########################################
# /profile/device/:device/port/:port/:strategy/:interval
########################################
def portProfile(portiaConfig, edgeId, port, strategy=ProfileStrategies.BY_ZERO_PORT, interval=30, params={ 'precision': 'ms', 'sort': True }):

    endpoint = '/profile/device/{0}/port/{1}/{2}/{3}{4}'.format( edgeId, port, resolveStrategy(strategy), interval, utils.buildGetParams(params) )
    response = utils.httpGetRequest(portiaConfig, endpoint)

    if response.status_code == 200:

        d = json.loads(response.text)
        if portiaConfig['debug']:
            print( '[portia-debug]: {0}'.format(d['ports']) )
        return d

    else:
        raise Exception('couldn\'t retrieve data')

########################################
# sensorProfile
########################################
# /profile/device/:device/port/:port/sensor/:sensor/:strategy/:interval
########################################
def sensorProfile(portiaConfig, edgeId, port, sensor, strategy=ProfileStrategies.BY_ZERO_PORT, interval=30, params={ 'precision': 'ms', 'sort': True }):

    endpoint = '/profile/device/{0}/port/{1}/sensor/{2}/{3}/{4}{5}'.format( edgeId, port, sensor, resolveStrategy(strategy), interval, utils.buildGetParams(params) )
    response = utils.httpGetRequest(portiaConfig, endpoint)

    if response.status_code == 200:

        d = json.loads(response.text)
        if portiaConfig['debug']:
            print( '[portia-debug]: {0}'.format(d['ports']) )
        return d

    else:
        raise Exception('couldn\'t retrieve data')
