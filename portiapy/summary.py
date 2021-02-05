"""Select tools to summarize a device's data based on its ports, sensors and
dimensions.
"""

from enum import Enum

import portiapy.utils as utils


class SummaryStrategies(Enum):
    PER_MINUTE = 1
    PER_HOUR = 2
    PER_DAY = 3
    PER_MONTH = 4
    PER_YEAR = 5

    @property
    def endpoint(self):
        return self.name.lower().replace('_', '')


def query_by_dimension(
    portia_config: dict,
    dimension_code: int,
    devices: list,
    strategy: SummaryStrategies=SummaryStrategies.PER_HOUR,
    interval: int=1,
    params: dict={
        'from': None,
        'to': None,
        'lower_bound': None,
        'upper_bound': None,
        'offset': 0,
        'fill': None,
        'order': None,
        'limit': None,
        'avg': True,
        'min': True,
        'max': True,
        'sum': False,
        'median': False,
        'mode': False,
        'stddev': False,
        'spread': False,
        'last_timestamp': False,
        'precision': 'ms',
        'timezone': 'Etc/UTC'
    }) -> object:
    """Summarizes multiple devices by one dimension.
    
    Arguments:
        portia_config {dict} -- Portia's configuration arguments
        dimension_code {int} -- dimension code of the device
        devices {list} -- list of devices to summarize
    
    Keyword Arguments:
        strategy {SummaryStrategies} -- strategy to use when summarizing
                                        (default: {SummaryStrategies.PER_HOUR})
        interval {int} -- interval of time to summarize (default: {1})
        params {dict} -- params to send to the service (default: {{ 'from',
                         'to', 'lower_bound', 'upper_bound', 'offset': 0,
                         'fill', 'order', 'limit', 'min', 'max', 'sum', 'avg',
                         'median', 'mode', 'stddev', 'spread',
                         'last_timestamp', precision': 'ms',
                         'timezone': 'Etc/UTC'}})

    Returns:
        object -- object with the device's summarized dimensions
    """
    accept_header = portia_config.get('Accept')

    if accept_header is None:
        accept_header = 'text/csv'

    header = {'Accept': accept_header}

    endpoint = '/summary/dimension/{0}/{1}/{2}' \
               .format(dimension_code, strategy.endpoint, interval)

    response = utils.http_post_request(
        portia_config,
        endpoint,
        { 'devices': devices },
        params=params,
        optional_headers=header
    )

    return utils.convert(accept_header, portia_config, response)


def query_device_by_dimension(
    portia_config: dict,
    edge_id: str,
    dimension_code: int,
    series: list,
    strategy: SummaryStrategies=SummaryStrategies.PER_HOUR,
    interval: int=1,
    params: dict={
        'from': None,
        'to': None,
        'lower_bound': None,
        'upper_bound': None,
        'offset': 0,
        'fill': None,
        'order': None,
        'limit': None,
        'avg': True,
        'min': True,
        'max': True,
        'sum': False,
        'median': False,
        'mode': False,
        'stddev': False,
        'spread': False,
        'last_timestamp': False,
        'precision': 'ms',
        'timezone': 'Etc/UTC'
    }) -> object:
    """Summarizes multiple series of a device by one dimension.
    
    Arguments:
        portia_config {dict} -- Portia's configuration arguments
        edge_id {str} -- Edge ID that identifies the device
        dimension_code {int} -- dimension code of the device
        series {list} -- list of series to summarize
    
    Keyword Arguments:
        strategy {SummaryStrategies} -- strategy to use when summarizing
                                        (default: {SummaryStrategies.PER_HOUR})
        interval {int} -- interval of time to summarize (default: {1})
        params {dict} -- params to send to the service (default: {{ 'from',
                         'to', 'lower_bound', 'upper_bound', 'offset': 0,
                         'fill', 'order', 'limit', 'min', 'max', 'sum', 'avg',
                         'median', 'mode', 'stddev', 'spread',
                         'last_timestamp', precision': 'ms',
                         'timezone': 'Etc/UTC'}})

    Returns:
        object -- object with the device's summarized dimensions
    """
    accept_header = portia_config.get('Accept')

    if accept_header is None:
        accept_header = 'text/csv'

    header = {'Accept': accept_header}

    endpoint = '/summary/device/{0}/dimension/{1}/{2}/{3}' \
               .format(edge_id, dimension_code, strategy.endpoint, interval)

    response = utils.http_post_request(
        portia_config,
        endpoint,
        { 'series': series },
        params=params,
        optional_headers=header
    )

    return utils.convert(accept_header, portia_config, response)


def query_by_port_sensor(
    portia_config: dict,
    edge_id: str,
    port: int,
    sensor: int,
    strategy: SummaryStrategies=SummaryStrategies.PER_HOUR,
    interval: int=1,
    params: dict={
        'from': None,
        'to': None,
        'lower_bound': None,
        'upper_bound': None,
        'offset': 0,
        'fill': None,
        'order': None,
        'limit': None,
        'avg': True,
        'min': True,
        'max': True,
        'sum': False,
        'median': False,
        'mode': False,
        'stddev': False,
        'spread': False,
        'last_timestamp': False,
        'precision': 'ms',
        'timezone': 'Etc/UTC'
    }) -> object:
    """Summarizes a device by port and sensor.
    
    Arguments:
        portia_config {dict} -- Portia's configuration arguments
        edge_id {str} -- Edge ID that identifies the device
        port {int} -- port of the device
        sensor {int} -- sensor of the device
    
    Keyword Arguments:
        strategy {SummaryStrategies} -- strategy to use when summarizing
                                        (default: {SummaryStrategies.PER_HOUR})
        interval {int} -- interval of time to summarize (default: {1})
        params {dict} -- params to send to the service (default: {{ 'from',
                         'to', 'lower_bound', 'upper_bound', 'offset': 0,
                         'fill', 'order', 'limit', 'min', 'max', 'sum', 'avg',
                         'median', 'mode', 'stddev', 'spread',
                         'last_timestamp', precision': 'ms',
                         'timezone': 'Etc/UTC'}})

    Returns:
        object -- object with the device's summarized dimensions
    """
    accept_header = portia_config.get('Accept')

    if accept_header is None:
        accept_header = 'text/csv'

    header = {'Accept': accept_header}

    endpoint = '/summary/device/{0}/port/{1}/sensor/{2}/{3}/{4}' \
               .format(edge_id, port, sensor, strategy.endpoint, interval)

    response = utils.http_get_request(
        portia_config, endpoint, params=params, optional_headers=header
    )

    return utils.convert(accept_header, portia_config, response)


def query_by_port_sensor_dimension(
    portia_config: dict,
    edge_id: str,
    port: int,
    sensor: int,
    dimension_code: int,
    strategy: SummaryStrategies=SummaryStrategies.PER_HOUR,
    interval: int=1,
    params: dict={
        'from': None,
        'to': None,
        'lower_bound': None,
        'upper_bound': None,
        'offset': 0,
        'fill': None,
        'order': None,
        'limit': None,
        'avg': True,
        'min': True,
        'max': True,
        'sum': False,
        'median': False,
        'mode': False,
        'stddev': False,
        'spread': False,
        'last_timestamp': False,
        'precision': 'ms',
        'timezone': 'Etc/UTC'
    }) -> object:
    """Summarizes a device by port, sensor and dimension code.
    
    Arguments:
        portia_config {dict} -- Portia's configuration arguments
        edge_id {str} -- Edge ID that identifies the device
        port {int} -- port of the device
        sensor {int} -- sensor of the device
        dimension_code {int} -- dimension code of the device
    
    Keyword Arguments:
        strategy {SummaryStrategies} -- strategy to use when summarizing
                                        (default: {SummaryStrategies.PER_HOUR})
        interval {int} -- interval of time to summarize (default: {1})
        params {dict} -- params to send to the service (default: {{ 'from',
                         'to', 'lower_bound', 'upper_bound', 'offset': 0,
                         'fill', 'order', 'limit', 'min', 'max', 'sum', 'avg',
                         'median', 'mode', 'stddev', 'spread',
                         'last_timestamp', precision': 'ms',
                         'timezone': 'Etc/UTC'}})

    Returns:
        object -- object with the device's summarized dimensions
    """
    accept_header = portia_config.get('Accept')

    if accept_header is None:
        accept_header = 'text/csv'

    header = {'Accept': accept_header}

    endpoint = ('/summary/device/{0}/port/{1}/sensor/{2}/dimension/{3}/{4}'
                '/{5}'.format(
                    edge_id,
                    port,
                    sensor,
                    dimension_code,
                    strategy.endpoint,
                    interval
                ))

    response = utils.http_get_request(
        portia_config, endpoint, params=params, optional_headers=header
    )

    return utils.convert(accept_header, portia_config, response)
