#####################################
#              Describe             #
#####################################

# Libraries
import json                       # JSON encoder and decoder
import pandas                     # Data analysis tools for Python
import portiapy.utils as utils

# Functions
def about():
    print("portiapy.describe - an Agriness Edge project")

########################################
# devicePorts
########################################
# /describe/device/:device/ports OR
# /describe/device/:device/ports/last
########################################
def devicePorts(portiaConfig, edgeId, last=False, params={ 'from': None, 'to': None, 'precision': 'ms', 'sort': True }):

    if last == False:
        endpoint = '/describe/device/{0}/ports{1}'.format( edgeId, utils.buildGetParams(params) )
    else:
        endpoint = '/describe/device/{0}/ports/last{1}'.format( edgeId, utils.buildGetParams(params) )

    response = utils.httpGetRequest(portiaConfig, endpoint)

    if response.status_code == 200:

        d = json.loads(response.text)['ports']
        if portiaConfig['debug']:
            print( '[portia-debug]: {0}'.format(d) )

        if last == True:
            d = pandas.DataFrame(d, columns=['header_timestamp', 'port', 'dimension_thing_code'])
        return d

    else:
        raise Exception('couldn\'t retrieve data')

########################################
# devicePortSensors
########################################
# /describe/device/:device/port/:port/sensors OR
# /describe/device/:device/port/:port/sensors/last
########################################
def devicePortSensors(portiaConfig, edgeId, port, last=False, params={ 'from': None, 'to': None, 'precision': 'ms', 'sort': True }):

    if last == False:
        endpoint = '/describe/device/{0}/port/{1}/sensors{2}'.format( edgeId, port, utils.buildGetParams(params) )
    else:
        endpoint = '/describe/device/{0}/port/{1}/sensors/last{2}'.format( edgeId, port, utils.buildGetParams(params) )

    response = utils.httpGetRequest(portiaConfig, endpoint)

    if response.status_code == 200:

        d = json.loads(response.text)['sensors']
        if portiaConfig['debug']:
            print( '[portia-debug]: {0}'.format(d) )

        if last == True:
            d = pandas.DataFrame(d, columns=['header_timestamp', 'sensor', 'dimension_value', 'dimension_code', 'dimension_unity_code', 'dimension_thing_code'])
        return d

    else:
        raise Exception('couldn\'t retrieve data')

########################################
# devicePortDimensions
########################################
# /describe/device/:device/port/:port/dimensions OR
# /describe/device/:device/port/:port/dimensions/last
########################################
def devicePortDimensions(portiaConfig, edgeId, port, last=False, params={ 'from': None, 'to': None, 'precision': 'ms', 'sort': True }):

    if last == False:
        endpoint = '/describe/device/{0}/port/{1}/dimensions{2}'.format( edgeId, port, utils.buildGetParams(params) )
    else:
        endpoint = '/describe/device/{0}/port/{1}/dimensions/last{2}'.format( edgeId, port, utils.buildGetParams(params) )

    response = utils.httpGetRequest(portiaConfig, endpoint)

    if response.status_code == 200:

        d = json.loads(response.text)['dimensions']
        if portiaConfig['debug']:
            print( '[portia-debug]: {0}'.format(d) )

        if last == True:
            d = pandas.DataFrame(d, columns=['header_timestamp', 'dimension_code', 'sensor', 'dimension_thing_code'])
        return d

    else:
        raise Exception('couldn\'t retrieve data')

########################################
# devicePortSensorDimensions
########################################
# /describe/device/:device/port/:port/sensor/:sensor/dimensions OR
# /describe/device/:device/port/:port/sensor/:sensor/dimensions/last
########################################
def devicePortSensorDimensions(portiaConfig, edgeId, port, sensor, last=False, params={ 'from': None, 'to': None, 'precision': 'ms', 'sort': True }):

    if last == False:
        endpoint = '/describe/device/{0}/port/{1}/sensor/{2}/dimensions{3}'.format( edgeId, port, sensor, utils.buildGetParams(params) )
    else:
        endpoint = '/describe/device/{0}/port/{1}/sensor/{2}/dimensions/last{3}'.format( edgeId, port, sensor, utils.buildGetParams(params) )

    response = utils.httpGetRequest(portiaConfig, endpoint)

    if response.status_code == 200:

        d = json.loads(response.text)['dimensions']
        if portiaConfig['debug']:
            print( '[portia-debug]: {0}'.format(d) )

        if last == True:
            d = pandas.DataFrame(d, columns=['header_timestamp', 'dimension_value', 'dimension_code', 'dimension_unity_code', 'dimension_thing_code'])
        return d

    else:
        raise Exception('couldn\'t retrieve data')
