"""Description tools to discover a device's list of ports, sensors and
dimensions.
"""

import json

import pandas as pd

import portiapy.utils as utils


def device_ports(
    portia_config: dict,
    edge_id: str,
    last: bool=False,
    params: dict={
        'from': None,
        'to': None,
        'sort': True,
        'precision': 'ms',
        'timezone': 'Etc/UTC'
}) -> object:
    """Lists a device's ports.
    
    Arguments:
        portia_config {dict} -- Portia's configuration arguments 
        edge_id {str} -- Edge ID that identifies the device
    
    Keyword Arguments:
        last {bool} -- if the last package of each port should be returned or
                       not (default: {False})
        params {dict} -- params to send to the service (default:
                         {{ 'from', 'to', 'sort', 'precision': 'ms',
                         'timezone': 'Etc/UTC' }})
    
    Returns:
        object -- object with the list of ports
    
    Raises:
        Exception -- when the request goes wrong
    """
    if last == False:
        endpoint = '/describe/device/{0}/ports'.format(edge_id)
    else:
        endpoint = '/describe/device/{0}/ports/last'.format(edge_id)

    response = utils.http_get_request(portia_config, endpoint, params)

    if response.status_code == 200:

        d = json.loads(response.text).get('ports')

        if portia_config.get('debug'):
            print('[portia-debug]: {0}'.format(d))

        if last == True:
            d = pd.DataFrame(
                d,
                columns=['header_timestamp', 'port', 'dimension_thing_code']
            )

            d['port'] = d['port'].map(int)
            d['dimension_thing_code'] = d['dimension_thing_code'].map(int)
        else:
            d = list(map(int, d))

        return d

    else:
        raise Exception("couldn't retrieve data")

def device_port_sensors(
    portia_config: dict,
    edge_id: str,
    port: int,
    last: bool=False,
    params: dict={
        'from': None,
        'to': None,
        'sort': True,
        'precision': 'ms',
        'timezone': 'Etc/UTC'
}) -> object:
    """Lists a port's sensors.
    
    Arguments:
        portia_config {dict} -- Portia's configuration arguments
        edge_id {str} -- Edge ID that identifies the device
        port {int} -- port of the device
    
    Keyword Arguments:
        last {bool} -- if the last package of each port should be returned or
                       not (default: {False})
        params {dict} -- params to send to the service (default:
                         {{ 'from', 'to', 'sort', 'precision': 'ms',
                         'timezone': 'Etc/UTC' }})
    
    Returns:
        object -- object with the list of sensors
    
    Raises:
        Exception -- when the request goes wrong
    """
    if last == False:
        endpoint = '/describe/device/{0}/port/{1}/sensors' \
                   .format(edge_id, port)
    else:
        endpoint = '/describe/device/{0}/port/{1}/sensors/last' \
                   .format(edge_id, port)

    response = utils.http_get_request(portia_config, endpoint, params)

    if response.status_code == 200:

        d = json.loads(response.text).get('sensors')
        if portia_config.get('debug'):
            print('[portia-debug]: {0}'.format(d))

        if last == True:
            d = pd.DataFrame(
                d,
                columns=[
                    'header_timestamp',
                    'sensor',
                    'dimension_value',
                    'dimension_code',
                    'dimension_unity_code',
                    'dimension_thing_code'
                ]
            )

            d['sensor'] = d['sensor'].map(int)
            d['dimension_code'] = d['dimension_code'].map(int)
            d['dimension_unity_code'] = d['dimension_unity_code'].map(int)
            d['dimension_thing_code'] = d['dimension_thing_code'].map(int)
        else:
            d = list(map(int, d))

        return d

    else:
        raise Exception("couldn't retrieve data")

def device_port_dimensions(
    portia_config: dict,
    edge_id: str,
    port: int,
    last: bool=False,
    params: dict={
        'from': None,
        'to': None,
        'sort': True,
        'precision': 'ms',
        'timezone': 'Etc/UTC'
}) -> object:
    """Lists a port's dimensions.
    
    Arguments:
        portia_config {dict} -- Portia's configuration arguments
        edge_id {str} -- Edge ID that identifies the device
        port {int} -- port of the device
    
    Keyword Arguments:
        last {bool} -- if the last package of each port should be returned or
                       not (default: {False})
        params {dict} -- params to send to the service (default:
                         {{ 'from', 'to', 'sort', 'precision': 'ms',
                         'timezone': 'Etc/UTC' }})
    
    Returns:
        object -- object with the list of dimensions
    
    Raises:
        Exception -- when the request goes wrong
    """
    if last == False:
        endpoint = '/describe/device/{0}/port/{1}/dimensions' \
                   .format(edge_id, port)
    else:
        endpoint = '/describe/device/{0}/port/{1}/dimensions/last' \
                   .format(edge_id, port)

    response = utils.http_get_request(portia_config, endpoint, params)

    if response.status_code == 200:

        d = json.loads(response.text).get('dimensions')
        if portia_config.get('debug'):
            print('[portia-debug]: {0}'.format(d))

        if last == True:
            d = pd.DataFrame(
                d,
                columns=[
                    'header_timestamp',
                    'dimension_code',
                    'sensor',
                    'dimension_thing_code'
                ]
            )

            d['sensor'] = d['sensor'].map(int)
            d['dimension_code'] = d['dimension_code'].map(int)
            d['dimension_thing_code'] = d['dimension_thing_code'].map(int)
        else:
            d = list(map(int, d))

        return d

    else:
        raise Exception("couldn't retrieve data")

def device_port_sensor_dimensions(
    portia_config: dict,
    edge_id: str,
    port: int,
    sensor: int,
    last: bool=False,
    params: dict={
        'from': None,
        'to': None,
        'sort': True,
        'precision': 'ms',
        'timezone': 'Etc/UTC'
}) -> object:
    """Lists a sensor's dimensions.
    
    Arguments:
        portia_config {dict} -- Portia's configuration arguments
        edge_id {str} -- Edge ID that identifies the device
        port {int} -- port of the device
        sensor {int} -- sensor of the device
    
    Keyword Arguments:
        last {bool} -- if the last package of each port should be returned or
                       not (default: {False})
        params {dict} -- params to send to the service (default:
                         {{ 'from', 'to', 'sort', 'precision': 'ms',
                         'timezone': 'Etc/UTC' }})
    
    Returns:
        object -- object with the list of dimensions
    
    Raises:
        Exception -- when the request goes wrong
    """
    if last == False:
        endpoint = '/describe/device/{0}/port/{1}/sensor/{2}/dimensions' \
                   .format(edge_id, port, sensor)
    else:
        endpoint = '/describe/device/{0}/port/{1}/sensor/{2}/dimensions/last' \
                   .format(edge_id, port, sensor)

    response = utils.http_get_request(portia_config, endpoint, params)

    if response.status_code == 200:

        d = json.loads(response.text).get('dimensions')
        if portia_config.get('debug'):
            print('[portia-debug]: {0}'.format(d))

        if last == True:
            d = pd.DataFrame(
                d,
                columns=[
                    'header_timestamp',
                    'dimension_value',
                    'dimension_code',
                    'dimension_unity_code',
                    'dimension_thing_code'
                ]
            )

            d['dimension_code'] = d['dimension_code'].map(int)
            d['dimension_unity_code'] = d['dimension_unity_code'].map(int)
            d['dimension_thing_code'] = d['dimension_thing_code'].map(int)
        else:
            d = list(map(int, d))

        return d

    else:
        raise Exception("couldn't retrieve data")
