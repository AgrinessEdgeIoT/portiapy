"""Profile tools where it is possible to create snapshots of a device's state
on any given time.
"""

import json
from enum import Enum

import portiapy.utils as utils


class ProfileStrategies(Enum):
    BY_ZERO_PORT = 1
    BY_PORTS = 2

    @property
    def endpoint(self):
        return self.name.lower().replace('_', '')


def device_profile(
    portia_config: dict,
    edge_id: str,
    strategy: ProfileStrategies=ProfileStrategies.BY_ZERO_PORT,
    interval: int=30,
    params: dict={ 'sort': True, 'precision': 'ms', 'timezone': 'Etc/UTC' }
) -> dict:
    """Retrieves a device's profile.

    Arguments:
        portia_config {dict} -- Portia's configuration arguments 
        edge_id {str} -- Edge ID that identifies the device
    
    Keyword Arguments:
        strategy {ProfileStrategies} -- strategy to use when building the
                                        profile (default: 
                                        {ProfileStrategies.BY_ZERO_PORT})
        interval {int} -- interval of time in minutes to build the profile
                          (default: {30})
        params {dict} -- params to send to the service (default: 
                         {{ 'sort', 'precision': 'ms',
                         'timezone': 'Etc/UTC' }})

    Returns:
        dict -- dictionary with the device's profile
    """
    endpoint = '/profile/device/{0}/{1}/{2}'.format(
        edge_id, strategy.endpoint, interval
    )

    response = utils.http_get_request(portia_config, endpoint, params)

    if response.status_code == 200:

        d = json.loads(response.text)
        if portia_config['debug']:
            print('[portia-debug]: {0}'.format(d.get('ports')))

        return d

    else:
        raise Exception("couldn't retrieve data")


def port_profile(
    portia_config: dict,
    edge_id: str,
    port: int,
    strategy: ProfileStrategies=ProfileStrategies.BY_ZERO_PORT,
    interval: int=30,
    params: dict={ 'sort': True, 'precision': 'ms', 'timezone': 'Etc/UTC' }
) -> dict:
    """Retrieves a port's profile.

    Arguments:
        portia_config {dict} -- Portia's configuration arguments
        edge_id {str} -- Edge ID that identifies the device
        port {int} -- port of the device
    
    Keyword Arguments:
        strategy {ProfileStrategies} -- strategy to use when building the
                                        profile (default: 
                                        {ProfileStrategies.BY_ZERO_PORT})
        interval {int} -- interval of time in minutes to build the profile
                          (default: {30})
        params {dict} -- params to send to the service (default: 
                         {{ 'sort', 'precision': 'ms',
                         'timezone': 'Etc/UTC' }})

    Returns:
        dict -- dictionary with the port's profile
    """
    endpoint = '/profile/device/{0}/port/{1}/{2}/{3}'.format(
        edge_id, port, strategy.endpoint, interval
    )

    response = utils.http_get_request(portia_config, endpoint, params)

    if response.status_code == 200:

        d = json.loads(response.text)
        if portia_config['debug']:
            print('[portia-debug]: {0}'.format(d.get('ports')))

        return d

    else:
        raise Exception("couldn't retrieve data")


def sensor_profile(
    portia_config: dict,
    edge_id: str,
    port: int,
    sensor: int,
    strategy: ProfileStrategies=ProfileStrategies.BY_ZERO_PORT,
    interval: int=30,
    params: dict={ 'sort': True, 'precision': 'ms', 'timezone': 'Etc/UTC' }
) -> dict:
    """Retrieves a sensor's profile.

    Arguments:
        portia_config {dict} -- Portia's configuration arguments
        edge_id {str} -- Edge ID that identifies the device
        port {int} -- port of the device
        sensor {int} -- sensor of the device
    
    Keyword Arguments:
        strategy {ProfileStrategies} -- strategy to use when building the
                                        profile (default: 
                                        {ProfileStrategies.BY_ZERO_PORT})
        interval {int} -- interval of time in minutes to build the profile
                          (default: {30})
        params {dict} -- params to send to the service (default: 
                         {{ 'sort', 'precision': 'ms',
                         'timezone': 'Etc/UTC' }})

    Returns:
        dict -- dictionary with the sensor's profile
    """
    endpoint = '/profile/device/{0}/port/{1}/sensor/{2}/{3}/{4}'.format(
        edge_id, port, sensor, strategy.endpoint, interval
    )

    response = utils.http_get_request(portia_config, endpoint, params)

    if response.status_code == 200:

        d = json.loads(response.text)
        if portia_config['debug']:
            print('[portia-debug]: {0}'.format(d.get('ports')))

        return d

    else:
        raise Exception("couldn't retrieve data")
