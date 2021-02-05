"""Select tools to fetch a device's events based on its ports, sensors, dimensions and event codes.
"""

import portiapy.utils as utils


def query_by_port_sensor(
    portia_config: dict,
    edge_id: str,
    port: int,
    sensor: int,
    last: bool=False,
    params: dict={
        'from': None,
        'to': None,
        'order': None,
        'limit': None,
        'precision': 'ms',
        'timezone': 'Etc/UTC'
    }) -> object:
    """Retrieves a device's events by its port and sensor.
    
    Arguments:
        portia_config {dict} -- Portia's configuration arguments
        edge_id {str} -- Edge ID that identifies the device
        port {int} -- port of the device
        sensor {int} -- sensor of the device
    
    Keyword Arguments:
        last {bool} -- if the last event should be returned or not
                       (default: {False})
        params {dict} -- params to send to the service (default: {{ 'from',
                         'to', 'order', 'limit', 'precision': 'ms',
                         'timezone': 'Etc/UTC' }})

    Returns:
        object -- object with the device's events
    """
    accept_header = portia_config.get('Accept')

    if accept_header is None:
        accept_header = 'text/csv'

    header = {'Accept': accept_header}

    if last == False:
        endpoint = '/events/device/{0}/port/{1}/sensor/{2}'.format(
            edge_id, port, sensor
        )
    else:
        endpoint = '/events/device/{0}/port/{1}/sensor/{2}/last'.format(
            edge_id, port, sensor
        )

    response = utils.http_get_request(
        portia_config, endpoint, params=params, optional_headers=header
    )

    return utils.convert(accept_header, portia_config, response)


def query_by_port_dimension(
    portia_config: dict,
    edge_id: str,
    port: int,
    dimension_code: int,
    last: bool=False,
    params: dict={
        'from': None,
        'to': None,
        'order': None,
        'limit': None,
        'precision': 'ms',
        'timezone': 'Etc/UTC'
    }) -> object:
    """Retrieves a device's events by its port and dimension code.
    
    Arguments:
        portia_config {dict} -- Portia's configuration arguments
        edge_id {str} -- Edge ID that identifies the device
        port {int} -- port of the device
        dimension_code {int} -- dimension code of the device
    
    Keyword Arguments:
        last {bool} -- if the last event should be returned or not
                       (default: {False})
        params {dict} -- params to send to the service (default: {{ 'from',
                         'to', order', 'limit', 'precision': 'ms',
                         'timezone': 'Etc/UTC' }})

    Returns:
        object -- object with the device's events
    """
    accept_header = portia_config.get('Accept')

    if accept_header is None:
        accept_header = 'text/csv'

    header = {'Accept': accept_header}

    if last == False:
        endpoint = '/events/device/{0}/port/{1}/dimension/{2}'.format(
            edge_id, port, dimension_code
        )
    else:
        endpoint = '/events/device/{0}/port/{1}/dimension/{2}/last'.format(
            edge_id, port, dimension_code
        )

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
    last: bool=False,
    params: dict={
        'from': None,
        'to': None,
        'order': None,
        'limit': None,
        'precision': 'ms',
        'timezone': 'Etc/UTC'
    }) -> object:
    """Retrieves a device's events by its port, sensor and dimension code.
    
    Arguments:
        portia_config {dict} -- Portia's configuration arguments
        edge_id {str} -- Edge ID that identifies the device
        port {int} -- port of the device
        sensor {int} -- sensor of the device
        dimension_code {int} -- dimension code of the device
    
    Keyword Arguments:
        last {bool} -- if the last event should be returned or not
                       (default: {False})
        params {dict} -- params to send to the service (default: {{ 'from',
                         'to', 'order', 'lower_bound', 'upper_bound', 'order',
                         'limit', 'precision': 'ms', 'timezone': 'Etc/UTC' }})

    Returns:
        object -- object with the device's events
    """
    accept_header = portia_config.get('Accept')

    if accept_header is None:
        accept_header = 'text/csv'

    header = {'Accept': accept_header}

    if last == False:
        endpoint = '/events/device/{0}/port/{1}/sensor/{2}/dimension/{3}' \
                   .format(edge_id, port, sensor, dimension_code)
    else:
        endpoint = ('/events/device/{0}/port/{1}/sensor/{2}/dimension/{3}'
                    '/last'.format(edge_id, port, sensor, dimension_code))

    response = utils.http_get_request(
        portia_config, endpoint, params=params, optional_headers=header
    )

    return utils.convert(accept_header, portia_config, response)


def query_by_port_sensor_event(
    portia_config: dict,
    edge_id: str,
    port: int,
    sensor: int,
    event_code: int,
    last: bool=False,
    params: dict={
        'from': None,
        'to': None,
        'order': None,
        'limit': None,
        'precision': 'ms',
        'timezone': 'Etc/UTC'
    }) -> object:
    """Retrieves a device's events by its port and sensor.
    
    Arguments:
        portia_config {dict} -- Portia's configuration arguments
        edge_id {str} -- Edge ID that identifies the device
        port {int} -- port of the device
        sensor {int} -- sensor of the device
        event_code {int} -- event code of the device
    
    Keyword Arguments:
        last {bool} -- if the last event should be returned or not
                       (default: {False})
        params {dict} -- params to send to the service (default: {{ 'from',
                         'to', 'order', 'limit', 'precision': 'ms',
                         'timezone': 'Etc/UTC' }})

    Returns:
        object -- object with the device's events
    """
    accept_header = portia_config.get('Accept')

    if accept_header is None:
        accept_header = 'text/csv'

    header = {'Accept': accept_header}

    if last == False:
        endpoint = '/events/device/{0}/port/{1}/sensor/{2}/event/{3}'.format(
            edge_id, port, sensor, event_code
        )
    else:
        endpoint = '/events/device/{0}/port/{1}/sensor/{2}/event/{3}/last' \
        		   .format(edge_id, port, sensor, event_code)

    response = utils.http_get_request(
        portia_config, endpoint, params=params, optional_headers=header
    )

    return utils.convert(accept_header, portia_config, response)


def query_by_port_dimension_event(
    portia_config: dict,
    edge_id: str,
    port: int,
    dimension_code: int,
    event_code: int,
    last: bool=False,
    params: dict={
        'from': None,
        'to': None,
        'order': None,
        'limit': None,
        'precision': 'ms',
        'timezone': 'Etc/UTC'
    }) -> object:
    """Retrieves a device's events by its port and dimension code.
    
    Arguments:
        portia_config {dict} -- Portia's configuration arguments
        edge_id {str} -- Edge ID that identifies the device
        port {int} -- port of the device
        dimension_code {int} -- dimension code of the device
        event_code {int} -- event code of the device
    
    Keyword Arguments:
        last {bool} -- if the last event should be returned or not
                       (default: {False})
        params {dict} -- params to send to the service (default: {{ 'from',
                         'to', order', 'limit', 'precision': 'ms',
                         'timezone': 'Etc/UTC' }})

    Returns:
        object -- object with the device's events
    """
    accept_header = portia_config.get('Accept')

    if accept_header is None:
        accept_header = 'text/csv'

    header = {'Accept': accept_header}

    if last == False:
        endpoint = '/events/device/{0}/port/{1}/dimension/{2}/event/{3}' \
        		   .format(edge_id, port, dimension_code, event_code)
    else:
        endpoint = '/events/device/{0}/port/{1}/dimension/{2}/event/{3}/last' \
        		   .format(edge_id, port, dimension_code, event_code)

    response = utils.http_get_request(
        portia_config, endpoint, params=params, optional_headers=header
    )

    return utils.convert(accept_header, portia_config, response)


def query_by_port_sensor_dimension_event(
    portia_config: dict,
    edge_id: str,
    port: int,
    sensor: int,
    dimension_code: int,
    event_code: int,
    last: bool=False,
    params: dict={
        'from': None,
        'to': None,
        'order': None,
        'limit': None,
        'precision': 'ms',
        'timezone': 'Etc/UTC'
    }) -> object:
    """Retrieves a device's events by its port, sensor and dimension code.
    
    Arguments:
        portia_config {dict} -- Portia's configuration arguments
        edge_id {str} -- Edge ID that identifies the device
        port {int} -- port of the device
        sensor {int} -- sensor of the device
        dimension_code {int} -- dimension code of the device
        event_code {int} -- event code of the device
    
    Keyword Arguments:
        last {bool} -- if the last event should be returned or not
                       (default: {False})
        params {dict} -- params to send to the service (default: {{ 'from',
                         'to', 'order', 'lower_bound', 'upper_bound', 'order',
                         'limit', 'precision': 'ms', 'timezone': 'Etc/UTC' }})

    Returns:
        object -- object with the device's events
    """
    accept_header = portia_config.get('Accept')

    if accept_header is None:
        accept_header = 'text/csv'

    header = {'Accept': accept_header}

    if last == False:
        endpoint = ('/events/device/{0}/port/{1}/sensor/{2}/dimension/{3}'
        		    '/event/{4}'.format(
        		   		edge_id, port, sensor, dimension_code, event_code
        		   ))
    else:
        endpoint = ('/events/device/{0}/port/{1}/sensor/{2}/dimension/{3}'
        			'/event/{4}/last'.format(
        				edge_id, port, sensor, dimension_code, event_code
        		   ))

    response = utils.http_get_request(
        portia_config, endpoint, params=params, optional_headers=header
    )

    return utils.convert(accept_header, portia_config, response)
