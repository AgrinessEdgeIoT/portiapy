#####################################
#              Select               #
#####################################

# Libraries
from io import StringIO           # Read and write strings as files
import pandas                     # Data analysis tools for Python
import portiapy.utils as utils

# Functions
def about():
    print("portiapy.select - an Agriness Edge project")

########################################
# queryByPortSensor
########################################
# /select/device/:device/port/:port/sensor/:sensor OR
# /select/device/:device/port/:port/sensor/:sensor/last
########################################
def queryByPortSensor(portiaConfig, edgeId, port, sensor, last=False, params={ 'from': None, 'to': None, 'order': None, 'precision': 'ms', 'limit': None }):
    """Returns a pandas data frame with the portia select resultset"""

    header = {'Accept': 'text/csv'}

    if last == False:
        endpoint = '/select/device/{0}/port/{1}/sensor/{2}{3}'.format( edgeId, port, sensor, utils.buildGetParams(params) )
    else:
        endpoint = '/select/device/{0}/port/{1}/sensor/{2}/last{3}'.format( edgeId, port, sensor, utils.buildGetParams(params) )

    response = utils.httpGetRequest(portiaConfig, endpoint, header)

    if response.status_code == 200:
        try:

            dimensionSeries = pandas.read_csv( StringIO(response.text), sep=';' )
            if portiaConfig['debug']:
                print( '[portia-debug]: {0} rows'.format( len(dimensionSeries.index) ) )

            return dimensionSeries

        except Exception as err:
            raise Exception( 'couldn\'t create pandas data frame: {}'.format(err) )
    else:
        raise Exception('couldn\'t retrieve data')

########################################
# queryByPortDimension
########################################
# /select/device/:device/port/:port/dimension/:dimension OR
# /select/device/:device/port/:port/dimension/:dimension/last
########################################
def queryByPortDimension(portiaConfig, edgeId, port, dimensionCode, last=False, params={ 'from': None, 'to': None, 'order': None, 'precision': 'ms', 'limit': None }):
    """Returns a pandas data frame with the portia select resultset"""

    header = {'Accept': 'text/csv'}

    if last == False:
        endpoint = '/select/device/{0}/port/{1}/dimension/{2}{3}'.format( edgeId, port, dimensionCode, utils.buildGetParams(params) )
    else:
        endpoint = '/select/device/{0}/port/{1}/dimension/{2}/last{3}'.format( edgeId, port, dimensionCode, utils.buildGetParams(params) )

    response = utils.httpGetRequest(portiaConfig, endpoint, header)

    if response.status_code == 200:
        try:

            dimensionSeries = pandas.read_csv( StringIO(response.text), sep=';' )
            if portiaConfig['debug']:
                print( '[portia-debug]: {0} rows'.format( len(dimensionSeries.index) ) )

            return dimensionSeries

        except Exception as err:
            raise Exception( 'couldn\'t create pandas data frame: {}'.format(err) )
    else:
        raise Exception('couldn\'t retrieve data')

########################################
# queryByPortSensorDimension
########################################
# /select/device/:device/port/:port/sensor/:sensor/dimension/:dimension OR
# /select/device/:device/port/:port/sensor/:sensor/dimension/:dimension/last
########################################
def queryByPortSensorDimension(portiaConfig, edgeId, port, sensor, dimensionCode, last=False, params={ 'from': None, 'to': None, 'order': None, 'precision': 'ms', 'limit': None }):
    """Returns a pandas data frame with the portia select resultset"""

    header = {'Accept': 'text/csv'}

    if last == False:
        endpoint = '/select/device/{0}/port/{1}/sensor/{2}/dimension/{3}{4}'.format( edgeId, port, sensor, dimensionCode, utils.buildGetParams(params) )
    else:
        endpoint = '/select/device/{0}/port/{1}/sensor/{2}/dimension/{3}/last{4}'.format( edgeId, port, sensor, dimensionCode, utils.buildGetParams(params) )

    response = utils.httpGetRequest(portiaConfig, endpoint, header)

    if response.status_code == 200:
        try:

            dimensionSeries = pandas.read_csv( StringIO(response.text), sep=';' )
            if portiaConfig['debug']:
                print( '[portia-debug]: {0} rows'.format( len(dimensionSeries.index) ) )

            return dimensionSeries

        except Exception as err:
            raise Exception( 'couldn\'t create pandas data frame: {}'.format(err) )
    else:
        raise Exception('couldn\'t retrieve data')
