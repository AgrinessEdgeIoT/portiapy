"""Utility constants, methods and classes used by all modules.
"""

import json
import time
from io import StringIO

import arrow
import requests
import pandas as pd
from dateutil import tz
import plotly.offline as plotly
import plotly.graph_objs as plotlygo


THING_CODES = {
    0:  'NotSpecified',
    1:  'Sensor_Agriness_TU',
    2:  'Sensor_Agriness_AirQ',
    3:  'Collector_Agriness_Hydro_v1',
    4:  'Sensor_Agriness_AnimalScale',
    5:  'Collector_Agriness_CycleCounter_v1',
    6:  'Collector_Inobram_Smaai_v5',
    7:  'Sensor_Agriness_HydroEDN15-100',
    8:  'Sensor_Agriness_HydroQMS',
    9:  'Sensor_Agriness_HydroTemp',
    10: 'T4_Agriness_v0',
    11: 'Collector_Agriness_Universal_v1',
    12: 'Collector_Inobram_Smaai_v3',
    13: 'Collector_Inobram_Smaai_v4',
    14: 'T4_Agriness_v1',
    15: 'Sensor_Inobram_T',
    16: 'Sensor_Inobram_TU',
    17: 'Sensor_Inobram_Exhaustor',
    18: 'Sensor_Inobram_Nebulizer',
    19: 'Sensor_Inobram_Heater',
    20: 'Sensor_Inobram_Dimmer',
    21: 'Sensor_Inobram_PE',
    22: 'Sensor_Inobram_H2O',
    23: 'Sensor_Inobram_CO2',
    24: 'Sensor_Inobram_U',
    25: 'Sensor_Inobram_AnimalScale',
    26: 'Sensor_Inobram_SiloScale',
    27: 'T4_Agriness_Virtual_v0',
    28: 'Collector_Inobram_Ambientte_v1',
    29: 'Collector_Agriness_Bluetooth_v1',
    30: 'Sensor_Datamars_AnimalScale_v2',
    31: 'T4_Agriness_Network_v0',
    32: 'Sensor_Inobram_Inlet',
    33: 'Sensor_Inobram_Curtain',
    34: 'Sensor_Datamars_AnimalScale_v3',
    35: 'Sensor_GSI_T',
    36: 'Sensor_GSI_U',
    37: 'Sensor_GSI_H2O',
    38: 'Sensor_GSI_AnimalScale',
    39: 'Sensor_GSI_Exhaustor',
    40: 'Collector_AgNet_Gateway_v1',
    41: 'Sensor_AgNet_T1',
    42: 'Sensor_AgNet_U',
    43: 'Collector_Roboagro_v1',
    44: 'Collector_GSI_EDGE_v1',
    45: 'Collector_BigDutchman_Viper_v1',
    46: 'Sensor_BigDutchman_T',
    47: 'Sensor_BigDutchman_U',
    48: 'Sensor_BigDutchman_H2O',
    49: 'Sensor_BigDutchman_AnimalScale',
    50: 'Sensor_BigDutchman_PE',
    51: 'Sensor_BigDutchman_NH3',
    52: 'Sensor_BigDutchman_CO2',
    53: 'T4_Agriness_v2',
    54: 'Sensor_AgNet_Light',
    55: 'Sensor_AgNet_ExtT',
    56: 'Sensor_AgNet_ExtU',
    57: 'Sensor_AgNet_H2O',
    58: 'Sensor_AgNet_CO2',
    59: 'Sensor_AgNet_NH3',
    60: 'Sensor_AgNet_FeedC',
    61: 'Sensor_AgNet_AirS',
    62: 'Sensor_AgNet_AnimalScale',
    63: 'T4_Agriness_Virtual_v1',
    64: 'Sensor_AgNet_T2',
    65: 'Sensor_AgNet_T3',
    66: 'Sensor_AgNet_T4',
    67: 'Sensor_AgNet_T5',
    68: 'Sensor_Inobram_T_H2O',
    69: 'Collector_Inobram_Ambientte_v3',
    70: 'Sensor_Roboagro_Stock',
    71: 'Sensor_Roboagro_Consumption',
    72: 'Sensor_Roboagro_Animal_Counter',
    73: 'Sensor_Roboagro_Bay_Consumption',
    74: 'Sensor_Roboagro_Bay_Animal_Counter',
    75: 'Collector_Roboagro_v2',
    76: 'Collector_IonTec_v1',
    77: 'Sensor_IonTec_T',
    78: 'Sensor_IonTec_U',
    79: 'Sensor_IonTec_CO2',
    80: 'Sensor_IonTec_NH3',
    81: 'Sensor_IonTec_Feeder',
    82: 'Sensor_IonTec_ESF',
    83: 'Sensor_IonTec_Water_Level_Meter',
    84: 'Sensor_IonTec_Environment_Meter',
    85: 'Sensor_IonTec_Feed_Bin_Meter',
    86: 'Sensor_MSD_IDAL_Twin_v3'
}

DIMENSION_CODES = {
    'en-us': {
        0:  'Generic Dimension',
        1:  'Point Temperature',
        2:  'Average Temperature',
        3:  'Point Humidity',
        4:  'Average Humidity',
        5:  'Point Gas Concentration',
        6:  'Average Gas Concentration',
        7:  'Accumulated Water Flow',
        8:  'Point Water Flow',
        9:  'Point Water Temperature',
        10: 'Point Weight',
        11: 'Average Weight',
        12: 'Status',
        13: 'Point CO2 Concentration',
        14: 'Counter',
        15: 'Accumulated Time',
        16: 'Signal Strength',
        17: 'Free Memory',
        18: 'Free Storage',
        19: 'System Load',
        20: 'File Size',
        21: 'Point Time',
        22: 'Profile',
        23: 'Point Electric Voltage',
        24: 'Point Pressure',
        25: 'Average Pressure',
        26: 'Model',
        27: 'Lot Day',
        28: 'Average Electric Voltage',
        29: 'Point Light',
        30: 'Point Wind Speed',
        31: 'Point NH3 Concentration',
        32: 'Point Angulation',
        33: 'AccumulatedWeight'
    },
    'pt-br': {
        0:  'Dimensão Genérica',
        1:  'Temperatura Pontual',
        2:  'Temperatura Média',
        3:  'Umidade Pontual',
        4:  'Umidade Média',
        5:  'Concentração de Gases Pontual',
        6:  'Concentração de Gases Média',
        7:  'Fluxo de Água Acumulado',
        8:  'Fluxo de Água Pontual',
        9:  'Temperatura da Água Pontual',
        10: 'Peso Pontual',
        11: 'Peso Médio',
        12: 'Estado',
        13: 'Concentração de CO2 Pontual',
        14: 'Contador',
        15: 'Tempo Acumulado',
        16: 'Força de Sinal',
        17: 'Memória Livre',
        18: 'Armazenamento Livre',
        19: 'Carga do Sistema',
        20: 'Tamanho de Arquivo',
        21: 'Tempo Pontual',
        22: 'Perfil',
        23: 'Tensão Elétrica Pontual',
        24: 'Pressão Pontual',
        25: 'Pressão Média',
        26: 'Modelo',
        27: 'Dia do Lote',
        28: 'Tensão Elétrica Média',
        29: 'Luz Pontual',
        30: 'Velocidade do Vento Pontual',
        31: 'Concentração de NH3 Pontual',
        32: 'Angulação Pontual',
        33: 'PesoAcumulado'
    }
}

EVENT_CODES = {
    'en-us': {
        0:  'Generic Event',
        1:  'Communication State'
    },
    'pt-br': {
        0:  'Evento Genérico',
        1:  'Estado de Comunicação'
    }
}

UNITY_CODES = {
    'en-us': {
        0:  ' unit(s)',
        1:  '°C',
        2:  '%',
        3:  'ppm',
        4:  'L',
        5:  'g',
        6:  's',
        7:  'L/min',
        8:  'dBm',
        9:  'B',
        10: '',
        11: '',
        12: 'ms',
        13: 'V',
        14: 'Pa',
        15: 'kg',
        16: ' day(s)',
        17: 'mV',
        18: 'gal',
        19: '°F',
        20: 'mL',
        21: 'lx',
        22: 'm/s',
        23: 't',
        24: 'lb',
        25: 'min',
        26: '°'
    },
    'pt-br': {
        0:  ' unidade(s)',
        1:  '°C',
        2:  '%',
        3:  'ppm',
        4:  'L',
        5:  'g',
        6:  's',
        7:  'L/min',
        8:  'dBm',
        9:  'B',
        10: '',
        11: '',
        12: 'ms',
        13: 'V',
        14: 'Pa',
        15: 'kg',
        16: ' dia(s)',
        17: 'mV',
        18: 'gal',
        19: '°F',
        20: 'mL',
        21: 'lx',
        22: 'm/s',
        23: 't',
        24: 'lb',
        25: 'min',
        26: '°'
    }
}


def humanize_thing_code(thing_code: int) -> str:
    """Translates a thing code into a humanized version of it.
    
    Arguments:
        thing_code {int} -- thing code to be humanized
    
    Returns:
        str -- humanized thing code
    """
    translated_thing_code = THING_CODES.get(int(thing_code))

    if translated_thing_code is None:
        return 'Thing Code {}'.format(thing_code)
    else:
        return translated_thing_code

def humanize_dimension_code(
    dimension_code: int, locale: str='en-us', custom: list=None
) -> str:
    """Translates a dimension code into a humanized version of it.
    
    Arguments:
        dimension_code {int} -- dimension code to be humanized
    
    Keyword Arguments:
        locale {str} -- which language to use when humanizing
                        (default: {'en-us'})
        custom {list} -- custom list of dimension codes (default: {None})
    
    Returns:
        str -- humanized dimension code
    """
    try:
        if custom is None:
            translated_dimension_code = DIMENSION_CODES.get(locale) \
                .get(int(dimension_code))
        else:
            translated_dimension_code = custom.get(locale) \
                .get(int(dimension_code))
    except:
        return 'Dimension Code {}'.format(dimension_code)
    else:
        return translated_dimension_code

def humanize_event_code(
    event_code: int, locale: str='en-us', custom: list=None
) -> str:
    """Translates an event code into a humanized version of it.
    
    Arguments:
        event_code {int} -- event code to be humanized
    
    Keyword Arguments:
        locale {str} -- which language to use when humanizing
                        (default: {'en-us'})
        custom {list} -- custom list of event codes (default: {None})
    
    Returns:
        str -- humanized event code
    """
    try:
        if custom is None:
            translated_event_code = EVENT_CODES.get(locale) \
                .get(int(event_code))
        else:
            translated_event_code = custom.get(locale) \
                .get(int(event_code))
    except:
        return 'Event Code {}'.format(event_code)
    else:
        return translated_event_code

def humanize_unity_code(
    unity_code: int, locale: str='en-us', custom: list=None
) -> str:
    """Translates a unity code into a humanized version of it.
    
    Arguments:
        unity_code {int} -- unity code to be humanized
    
    Keyword Arguments:
        locale {str} -- which language to use when humanizing
                        (default: {'en-us'})
        custom {list} -- custom list of unity codes (default: {None})
    
    Returns:
        str -- humanized unity code
    """
    try:
        if custom is None:
            translated_unity_code = UNITY_CODES.get(locale) \
                .get(int(unity_code))
        else:
            translated_unity_code = custom.get(locale) \
                .get(int(unity_code))
    except:
        return 'Unity Code {}'.format(unity_code)
    else:
        return translated_unity_code

def humanize_dataframe(
    dataframe: 'pd.DataFrame',
    locale: str='en-us',
    custom_dimension: list=None,
    custom_event: list=None,
    custom_unity: list=None
) -> 'pd.DataFrame':
    """Humanizes a data frame's dimensions by translating its columns data to
    actual text.

    Arguments:
        dataframe {pd.DataFrame} -- data frame to be humanized
    
    Keyword Arguments:
        locale {str} -- which language to use when humanizing
                        (default {'en-us'})
        custom_dimension {dict} -- custom list of dimension codes
                                   (default {None})
        custom_event {dict} -- custom list of event codes (default {None})
        custom_unity {dict} -- custom list of unity codes (default {None})

    Returns:
        pd.DataFrame -- humanized data frame
    """
    if 'dimension_thing_code' in dataframe.columns:
        dataframe['dimension_thing'] = dataframe['dimension_thing_code'].map(
            lambda thing_code: humanize_thing_code(int(thing_code))
        )


    if 'dimension_unity_code' in dataframe.columns:
        dataframe['dimension_unity'] = dataframe['dimension_unity_code'].map(
            lambda unity_code: humanize_unity_code(
                unity_code=int(unity_code),
                locale=locale,
                custom=custom_unity
            )
        )

    if 'dimension_code' in dataframe.columns:
        dataframe['dimension'] = dataframe['dimension_code'].map(
            lambda dimension_code: humanize_dimension_code(
                dimension_code=int(dimension_code),
                locale=locale,
                custom=custom_dimension
            )
        )

    if 'event_code' in dataframe.columns:
        dataframe['event'] = dataframe['event_code'].map(
            lambda event_code: humanize_event_code(
                event_code=int(event_code),
                locale=locale,
                custom=custom_event
            )
        )

    return dataframe

def humanize_json(
    json_: dict,
    locale: str='en-us',
    custom_dimension: list=None,
    custom_unity: list=None
) -> dict:
    """Humanizes a json's dimensions by translating its columns data to actual
    text.

    Arguments:
        json_ {dict} -- json to be humanized
    
    Keyword Arguments:
        locale {str} -- which language to use when humanizing
                        (default {'en-us'})
        custom_dimension {dict} -- custom list of dimension codes
                                   (default {None})
        custom_unity {dict} -- custom list of unity codes (default {None})

    Returns:
        dict -- humanized dictionary
    """
    json_['channel'] = humanize_thing_code(json_['channel_code'])
    json_['thing'] = humanize_thing_code(json_['thing_code'])

    for port in json_.get('ports'):
        port['thing'] = humanize_thing_code(port['thing_code'])

        for sensor in port.get('sensors'):
            last_package = sensor.get('last_package')

            last_package['dimension'] = humanize_dimension_code(
                dimension_code=last_package.get('dimension_code'),
                locale=locale,
                custom=custom_dimension
            )

            last_package['dimension_unity'] = humanize_unity_code(
                unity_code=last_package.get('dimension_unity_code'),
                locale=locale,
                custom=custom_unity
            )

            last_package['dimension_thing'] = humanize_thing_code(
                last_package.get('dimension_thing_code')
            )

    return json_


def http_get_request(
    portia_config: dict,
    endpoint: str,
    params: dict=None,
    optional_headers: dict=None
) -> object:
    """Makes an HTTP GET request.
    
    Arguments:
        portia_config {dict} -- Portia's configuration arguments
        endpoint {str} -- endpoint to make the request to
    
    Keyword Arguments:
        params {dict} -- params to send to the service (default: {None})
        optional_headers {dict} -- dictionary with other headers
                                   (default: {None})

    Returns:
        object -- response object
    """
    headers = {
        'Authorization': 'Bearer {0}' \
        .format(portia_config.get('authorization'))
    }

    if optional_headers is not None:
        headers = {**headers, **optional_headers}

    start = time.time()
    response = requests.get(
        '{0}{1}'.format(portia_config.get('baseurl'), endpoint),
        headers=headers,
        params=params
    )
    end = time.time()

    if portia_config.get('debug') == True:
        print(
            '[portia-debug]: status: {0} | {1:.4f} sec. | {2}' \
            .format(response.status_code, end - start, response.url)
        )

    return response

def http_post_request(
    portia_config: dict,
    endpoint: str,
    payload: dict,
    params: dict=None,
    optional_headers: dict=None
) -> object:
    """Makes an HTTP POST request.
    
    Arguments:
        portia_config {dict} -- Portia's configuration arguments 
        endpoint {str} -- endpoint to make the request to
        payload {dict} -- payload to send to the service
    
    Keyword Arguments:
        params {dict} -- params to send to the service (default: {None})
        optional_headers {dict} -- dictionary with other headers
                                   (default: {None})

    Returns:
        object -- response object
    """
    headers = {
        'Authorization': 'Bearer {0}' \
        .format(portia_config.get('authorization'))
    }

    if optional_headers is not None:
        headers = {**headers, **optional_headers}

    start = time.time()
    response = requests.post(
        '{0}{1}'.format(portia_config.get('baseurl'), endpoint),
        headers=headers,
        params=params,
        json=payload
    )
    end = time.time()

    if portia_config.get('debug') == True:
        print(
            '[portia-debug]: status: {0} | {1:.4f} sec. | {2}' \
            .format(response.status_code, end - start, response.url)
        )

    return response

def http_put_request(
    portia_config: dict,
    endpoint: str,
    payload: dict,
    params: dict=None,
    optional_headers: dict=None
)  -> object:
    """Makes an HTTP PUT request.
    
    Arguments:
        portia_config {dict} -- Portia's configuration arguments 
        endpoint {str} -- endpoint to make the request to
        payload {dict} -- payload to send to the service
    
    Keyword Arguments:
        params {dict} -- params to send to the service (default: {None})
        optional_headers {dict} -- dictionary with other headers
                                   (default: {None})

    Returns:
        object -- response object
    """
    headers = {
        'Authorization': 'Bearer {0}' \
        .format(portia_config.get('authorization'))
    }

    if optional_headers is not None:
        headers = {**headers, **optional_headers}

    start = time.time()
    response = requests.put(
        '{0}{1}'.format(portia_config.get('baseurl'), endpoint),
        headers=headers,
        params=params,
        json=payload
    )
    end = time.time()

    if portia_config.get('debug') == True:
        print(
            '[portia-debug]: status: {0} | {1:.4f} sec. | {2}' \
            .format(response.status_code, end - start, response.url)
        )

    return response

def http_delete_request(
    portia_config: dict,
    endpoint: str,
    payload: dict=None,
    params: dict=None,
    optional_headers: dict=None
) -> object:
    """Makes an HTTP DELETE request.
    
    Arguments:
        portia_config {dict} -- Portia's configuration arguments 
        endpoint {str} -- endpoint to make the request to
    
    Keyword Arguments:
        payload {dict} -- payload to send to the service (default: {None})
        params {dict} -- params to send to the service (default: {None})
        optional_headers {dict} -- dictionary with other headers
                                   (default: {None})

    Returns:
        object -- response object
    """
    headers = {
        'Authorization': 'Bearer {0}' \
        .format(portia_config.get('authorization'))
    }

    if optional_headers is not None:
        headers = {**headers, **optional_headers}

    start = time.time()
    response = requests.delete(
        '{0}{1}'.format(portia_config.get('baseurl'), endpoint),
        headers=headers,
        params=params,
        json=payload
    )
    end = time.time()

    if portia_config.get('debug') == True:
        print(
            '[portia-debug]: status: {0} | {1:.4f} sec. | {2}' \
            .format(response.status_code, end - start, response.url.encode('utf8'))
        )

    return response


def convert_csv(portia_config: dict, response: object) -> 'pd.DataFrame':
    """Converts a CSV text file to a data frame.
    
    Arguments:
        portia_config {dict} -- Portia's configuration arguments 
        response {object} -- HTTP response object
    
    Returns:
        pd.DataFrame -- converted dataframe
    
    Raises:
        Exception -- when the conversion goes wrong
    """
    if response.status_code == 200:

        try:

            dataframe = pd.read_csv(StringIO(response.text), sep=';')

            if 'port' in dataframe.columns:
                dataframe['port'] = dataframe['port'].map(int)

            if 'sensor' in dataframe.columns:
                dataframe['sensor'] = dataframe['sensor'].map(int)

            if 'event_code' in dataframe.columns:
                dataframe['event_code'] = dataframe['event_code'].map(int)

            if 'dimension_code' in dataframe.columns:
                dataframe['dimension_code'] = dataframe['dimension_code'] \
                    .map(int)

            if 'dimension_thing_code' in dataframe.columns:
                dataframe['dimension_thing_code'] = dataframe \
                    ['dimension_thing_code'].map(int)

            if 'dimension_unity_code' in dataframe.columns:
                dataframe['dimension_unity_code'] = dataframe \
                    ['dimension_unity_code'].map(int)

            if portia_config.get('debug'):
                print('[portia-debug]: {0} rows'.format(len(dataframe.index)))

            return dataframe

        except Exception as err:
            raise Exception('couldn\'t create data frame: {0}'.format(err))

    else:
        raise Exception("couldn't retrieve data")

def convert_json(portia_config: dict, response: object) -> dict:
    """Converts a JSON text file to a data frame.
    
    Arguments:
        portia_config {dict} -- Portia's configuration arguments 
        response {object} -- HTTP response object
    
    Returns:
        dict -- converted dictionary
    
    Raises:
        Exception -- when the conversion goes wrong
    """
    if response.status_code == 200:

        json_ = json.loads(response.text)
        if portia_config['debug']:
            print('[portia-debug]: {0}'.format(json_))

        return json_

    else:
        err = json.loads(response.text)
        raise Exception(
            "couldn't retrieve data: {0}".format(err.get('message'))
        )

def convert(type_: str, portia_config: dict, response: object) -> object:
    """Converts an HTTP response.
    
    Arguments:
        type_ {str} -- type of response
        portia_config {dict} -- Portia's configuration arguments 
        response {object} -- HTTP response object
    
    Returns:
        object -- converted response
    """
    if type_ == 'text/csv':
        return convert_csv(portia_config, response)
    elif type_ == 'application/json':
        return convert_json(portia_config, response)


def plot_selection_from_dataframes(
    dataframes: list, timezone: str='Etc/GMT-3'
):
    """Uses Plotly to plot a chart from a set of dataframes.
    
    Arguments:
        dataframes {list} -- list of dataframes
    
    Keyword Arguments:
        timezone {str} -- timezone to convert the timestamp to
                          (default: {'Etc/GMT-3'})
    """
    lines = []

    for i, dataframe in enumerate(dataframes):

        dataframe['header_timestamp'] = pd.to_datetime(
            dataframe['header_timestamp'],
            unit='ms'
        ).dt.tz_localize(timezone)

        lines.append(plotlygo.Scatter(
            y=dataframe.dimension_value,
            x=dataframe.header_timestamp,
            mode='lines+markers',
            name="Sensor {0}".format(i)
        ))

    data = plotlygo.Data(lines)
    layout = plotlygo.Layout(width=1100, height=650)
    plotly.iplot(plotlygo.Figure(data=data, layout=layout))

def plot_summary_from_dataframes(
    dataframes: list, timezone: str='Etc/GMT-3'
):
    """Uses Plotly to plot a chart from a set of dataframes.
    
    Arguments:
        dataframes {list} -- list of dataframes
    
    Keyword Arguments:
        timezone {str} -- timezone to convert the timestamp to
                          (default: {'Etc/GMT-3'})
    """
    lines = []

    for dataframe in dataframes:
        dataframe['header_timestamp'] = pd.to_datetime(
            dataframe['header_timestamp'],
            unit='ms'
        ).dt.tz_localize(timezone)

        lines.append(plotlygo.Bar(
            y=dataframe['number_of_packages'],
            x=dataframe.header_timestamp,
            name="Packages",
            opacity=0.1
        ))

        if 'max' in dataframe.columns:
            lines.append(plotlygo.Scatter(
                y=dataframe['max'],
                x=dataframe.header_timestamp,
                mode='lines+markers',
                name="Max",
                yaxis='y2'
            ))

        if 'avg' in dataframe.columns:
            lines.append(plotlygo.Scatter(
                y=dataframe['avg'],
                x=dataframe.header_timestamp,
                mode='lines+markers',
                name="Avg",
                yaxis='y2'
            ))

        if 'min' in dataframe.columns:
            lines.append(plotlygo.Scatter(
                y=dataframe['min'],
                x=dataframe.header_timestamp,
                mode='lines+markers',
                name="Min",
                yaxis='y2'
            ))

        if 'median' in dataframe.columns:
            lines.append(plotlygo.Scatter(
                y=dataframe['median'],
                x=dataframe.header_timestamp,
                mode='lines+markers',
                name="Median",
                yaxis='y2'
            ))

        if 'mode' in dataframe.columns:
            lines.append(plotlygo.Scatter(
                y=dataframe['mode'],
                x=dataframe.header_timestamp,
                mode='lines+markers',
                name="Mode",
                yaxis='y2'
            ))

        if 'sum' in dataframe.columns:
            lines.append(plotlygo.Scatter(
                y=dataframe['sum'],
                x=dataframe.header_timestamp,
                mode='lines+markers',
                name="Sum",
                yaxis='y2',
                visible='legendonly'
            ))

        if 'stddev' in dataframe.columns:
            lines.append(plotlygo.Scatter(
                y=dataframe['stddev'],
                x=dataframe.header_timestamp,
                mode='lines+markers',
                name="Stddev",
                yaxis='y2',
                visible='legendonly'
            ))

        if 'spread' in dataframe.columns:
            lines.append(plotlygo.Scatter(
                y=dataframe['spread'],
                x=dataframe.header_timestamp,
                mode='lines+markers',
                name="Spread",
                yaxis='y2',
                visible='legendonly'
            ))

    data = plotlygo.Data(lines)
    layout = plotlygo.Layout(
        width=1100,
        height=650,
        yaxis=dict(title='Number of Packages', side='right'),
        yaxis2=dict(title='Dimension Value',
        overlaying='y',
        side='left'
    ))
    plotly.iplot(plotlygo.Figure(data=data, layout=layout))


def map_device_port_to_dropdown_widget(edge_id: str) -> dict:
    """Maps set of device port to a dropdown.
    
    Arguments:
        edge_id {str} -- Edge ID that identifies the device
    
    Returns:
        dict -- configuration for the dropdown
    
    Raises:
        Exception -- when something goes wrong with the request
    """
    portMapping = {}

    response = http_get_request(
        '/describe/device/{0}/ports/last?precision=ms'.format(edge_id)
    )

    if response.status_code == 200:
        d = json.loads(response.text)

        for port in d['ports']:
            label = '{0:3} | {1:25} ({2})'.format(
                port['port'],
                humanize_thing_code(port["dimension_thing_code"]),
                arrow.get(
                    port["header_timestamp"] / 1000,
                    tzinfo=tz.gettz('America/Sao_Paulo')
                ).humanize()
            )

            portMapping[label] = port['port']

        return portMapping

    else:
        raise Exception('Couldn\'t retrieve data')

def map_device_port_sensors_to_dropdown_widget(edge_id: str, port: int) -> dict:
    """Maps set of device port sensors to a dropdown.
    
    Arguments:
        edge_id {str} -- Edge ID that identifies the device
        port {int} -- port to fetch
    
    Returns:
        dict -- configuration for the dropdown
    
    Raises:
        Exception -- when something goes wrong with the request
    """
    sensorMapping = {}

    response = http_get_request(
        '/describe/device/{0}/port/{1}/sensors/last?precision=ms' \
        .format(edge_id, port)
    )

    if response.status_code == 200:
        d = json.loads(response.text)

        for sensor in d['sensors']:
            label = '{0:3} | {1:25} | {2:6}{3:15} ({4})'.format(
                sensor['sensor'],
                humanize_dimension_code(sensor["dimension_code"]),
                sensor["dimension_value"],
                humanize_unity_code(sensor["dimension_unity_code"]),
                arrow.get(
                    sensor["header_timestamp"] / 1000,
                    tzinfo=tz.gettz('America/Sao_Paulo')
                ).humanize()
            )

            sensorMapping[label] = sensor['sensor']

        return sensorMapping

    else:
        raise Exception('Couldn\'t retrieve data')

def map_device_port_sensor_dimensions_to_dropdown_widget(
    edge_id: str, port: int, sensor: int
):
    """Maps set of device port sensor dimensions to a dropdown.
    
    Arguments:
        edge_id {str} -- Edge ID that identifies the device
        port {int} -- port to fetch
        sensor {int} -- sensor to fetch
    
    Returns:
        dict -- configuration for the dropdown
    
    Raises:
        Exception -- when something goes wrong with the request
    """
    dimensionMapping = {}

    response = http_get_request(
        '/describe/device/{0}/port/{1}/sensor/{2}/dimensions/last'
        '?precision=ms'.format(edge_id, port, sensor)
    )

    if response.status_code == 200:
        d = json.loads(response.text)

        for dimension in d['dimensions']:
            label = '{0:3} | {1:25} | {2:6}{3:15} ({4})'.format(
                dimension['dimension_code'],
                humanize_dimension_code(dimension["dimension_code"]),
                dimension["dimension_value"],
                humanize_unity_code(dimension["dimension_unity_code"]),
                arrow.get(
                    dimension["header_timestamp"] / 1000,
                    tzinfo=tz.gettz('America/Sao_Paulo')
                ).humanize()
            )

            dimensionMapping[label] = dimension['dimension_code']

        return dimensionMapping

    else:
        raise Exception('Couldn\'t retrieve data')


# Maintaining compatibility with old versions
translateThingCode = humanize_thing_code
translateUnityCode = humanize_unity_code
translateDimensionCode = humanize_dimension_code
