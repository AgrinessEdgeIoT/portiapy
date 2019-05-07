#####################################
#              Summary              #
#####################################

# Libraries
from enum import Enum             # Support for enumerations
from io import StringIO           # Read and write strings as files
import pandas                     # Data analysis tools for Python
import portiapy.utils as utils

# Enums
class SummaryStrategies(Enum):
    PER_MINUTE = 1
    PER_HOUR   = 2
    PER_DAY    = 3
    PER_MONTH  = 4
    PER_YEAR   = 5

# Functions
def about():
    print("portiapy.summary - an Agriness Edge project")

def resolveStrategy(strategy):
    if strategy == SummaryStrategies.PER_MINUTE:
        return 'perminute'
    elif strategy == SummaryStrategies.PER_HOUR:
        return 'perhour'
    elif strategy == SummaryStrategies.PER_DAY:
        return 'perday'
    elif strategy == SummaryStrategies.PER_MONTH:
        return 'permonth'
    else:
        return 'peryear'

########################################
# devicePortSensorDimensions
########################################
# /summary/device/:device/port/:port/sensor/:sensor/:strategy/:interval
########################################
def queryByPortSensor(portiaConfig, edgeId, port, sensor, strategy=SummaryStrategies.PER_HOUR, interval=1, params={ 'from': None, 'to': None, 'order': None, 'precision': 'ms', 'offset': 0, 'min': True, 'max': True, 'sum': True, 'avg': True, 'median': True, 'mode': False, 'stddev': False, 'spread': False }):
    """Returns a pandas data frame with the portia select resultset"""

    header = {'Accept': 'text/csv'}
    endpoint = '/summary/device/{0}/port/{1}/sensor/{2}/{3}/{4}{5}'.format( edgeId, port, sensor, resolveStrategy(strategy), interval, utils.buildGetParams(params) )
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
# devicePortSensorDimensions
########################################
# /summary/device/:device/port/:port/sensor/:sensor/dimension/:dimension/:strategy/:interval
########################################
def queryByPortSensorDimension(portiaConfig, edgeId, port, sensor, dimensionCode, strategy=SummaryStrategies.PER_HOUR, interval=1, params={ 'from': None, 'to': None, 'order': None, 'precision': 'ms', 'offset': 0, 'min': True, 'max': True, 'sum': True, 'avg': True, 'median': True, 'mode': False, 'stddev': False, 'spread': False }):
    """Returns a pandas data frame with the portia select resultset"""

    header = {'Accept': 'text/csv'}
    endpoint = '/summary/device/{0}/port/{1}/sensor/{2}/dimension/{3}/{4}/{5}{6}'.format( edgeId, port, sensor, dimensionCode, resolveStrategy(strategy), interval, utils.buildGetParams(params) )
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
