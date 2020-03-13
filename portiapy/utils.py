#####################################
#              Commons              #
#####################################

# Libraries
from datetime import date, datetime, timedelta, timezone  # Basic date and time types
import copy  # Shallow and deep copy operations
import json  # JSON encoder and decoder
import time  # Time access and conversions


# Functions
def about():
    print('portiapy.utils - an Agriness Edge project')


#####################################
#        REST API Management        #
#####################################

import requests  # Simple HTTP library


def httpGetRequest(portiaConfig, endpoint, headers=None):
    h = {'Authorization': 'Bearer {0}'.format(portiaConfig['authorization'])}
    if headers is not None:
        h = {**h, **headers}  # Takes the arguments and turn them into a dictionary

    url = '{0}{1}'.format(portiaConfig['baseurl'], endpoint)

    start = time.time()
    response = requests.get(url, headers=h)
    end = time.time()
    elapsed = end - start

    if portiaConfig['debug'] == True:
        print('[portia-debug]: status: {0} | {1:.4f} sec. | {2}'.format(response.status_code, elapsed, url))

    return response


def httpPostRequest(portiaConfig, endpoint, payload, headers=None):
    h = {'Authorization': 'Bearer {0}'.format(portiaConfig['authorization'])}
    if headers is not None:
        h = {**h, **headers}  # Takes the arguments and turn them into a dictionary

    url = '{0}{1}'.format(portiaConfig['baseurl'], endpoint)

    start = time.time()
    response = requests.post(url, headers=h, json=payload)
    end = time.time()
    elapsed = end - start

    if portiaConfig['debug'] == True:
        print('[portia-debug]: status: {0} | {1:.4f} sec. | {2}'.format(response.status_code, elapsed, url))

    return response


def httpPutRequest(portiaConfig, endpoint, payload, headers=None):
    h = {'Authorization': 'Bearer {0}'.format(portiaConfig['authorization'])}
    if headers is not None:
        h = {**h, **headers}  # Takes the arguments and turn them into a dictionary

    url = '{0}{1}'.format(portiaConfig['baseurl'], endpoint)

    start = time.time()
    response = requests.put(url, headers=h, json=payload)
    end = time.time()
    elapsed = end - start

    if portiaConfig['debug'] == True:
        print('[portia-debug]: status: {0} | {1:.4f} sec. | {2}'.format(response.status_code, elapsed, url))

    return response


def httpDeleteRequest(portiaConfig, endpoint, headers=None):
    h = {'Authorization': 'Bearer {0}'.format(portiaConfig['authorization'])}
    if headers is not None:
        h = {**h, **headers}  # Takes the arguments and turn them into a dictionary

    url = '{0}{1}'.format(portiaConfig['baseurl'], endpoint)

    start = time.time()
    response = requests.delete(url, headers=h)
    end = time.time()
    elapsed = end - start

    if portiaConfig['debug'] == True:
        print('[portia-debug]: status: {0} | {1:.4f} sec. | {2}'.format(response.status_code, elapsed, url))

    return response


def buildGetParams(params):
    getParams = ''
    hasParams = False

    for key, value in params.items():
        if value is not None:
            if hasParams == True:
                getParams += '&'
            else:
                getParams += '?'
                hasParams = True

            # Standardizing values
            if isinstance(value, bool) and value == True:
                value = 'true'
            elif isinstance(value, bool) and value == False:
                value = 'false'

            getParams += '{0}={1}'.format(key, value)

    return getParams


#####################################
#            Plotting               #
#####################################

from dateutil import tz  # Powerful extensions to datetime
import pandas  # Data analysis tools for Python
import plotly.graph_objs as plotlygo  # Modern visualization for the data era
import plotly.offline as plotly
import pytz  # World timezone definitions for Python


def plotSelectionsFromDataframes(dataFrames, timezone='Etc/GMT-3'):
    lines = []

    for i, dataFrame in enumerate(dataFrames):
        dataFrame['header_timestamp'] = pandas.to_datetime(dataFrame['header_timestamp'], unit='ms').dt.tz_localize(timezone)
        lines.append(plotlygo.Scatter(y=dataFrame.dimension_value, x=dataFrame.header_timestamp, mode='lines+markers',
                                      name="Sensor {0}".format(i)))

    data = plotlygo.Data(lines)
    layout = plotlygo.Layout(width=1100, height=650)
    plotly.iplot(plotlygo.Figure(data=data, layout=layout))


def plotSummariesFromDataframes(dataFrames, timezone='Etc/GMT-3'):
    lines = []

    for dataFrame in dataFrames:
        dataFrame['header_timestamp'] = pandas.to_datetime(dataFrame['header_timestamp'], unit='ms').dt.tz_localize(
            timezone)

        #         timeAxis = []
        #         for i, line in enumerate(dataFrame['header_timestamp']):
        #             timeAxis.append( dataFrame['header_timestamp'][i] )

        lines.append(plotlygo.Bar(y=dataFrame['number_of_packages'], x=dataFrame.header_timestamp, name="Packages", opacity=0.1))

        if 'max' in dataFrame.columns:
            lines.append(plotlygo.Scatter(y=dataFrame['max'], x=dataFrame.header_timestamp, mode='lines+markers', name="Max", yaxis='y2'))

        if 'avg' in dataFrame.columns:
            lines.append(plotlygo.Scatter(y=dataFrame['avg'], x=dataFrame.header_timestamp, mode='lines+markers', name="Avg", yaxis='y2'))

        if 'min' in dataFrame.columns:
            lines.append(plotlygo.Scatter(y=dataFrame['min'], x=dataFrame.header_timestamp, mode='lines+markers', name="Min", yaxis='y2'))

        if 'median' in dataFrame.columns:
            lines.append(plotlygo.Scatter(y=dataFrame['median'], x=dataFrame.header_timestamp, mode='lines+markers', name="Median", yaxis='y2'))

        if 'mode' in dataFrame.columns:
            lines.append(plotlygo.Scatter(y=dataFrame['mode'], x=dataFrame.header_timestamp, mode='lines+markers', name="Mode", yaxis='y2'))

        if 'sum' in dataFrame.columns:
            lines.append(plotlygo.Scatter(y=dataFrame['sum'], x=dataFrame.header_timestamp, mode='lines+markers', name="Sum", yaxis='y2',
                                          visible='legendonly'))

        if 'stddev' in dataFrame.columns:
            lines.append(plotlygo.Scatter(y=dataFrame['stddev'], x=dataFrame.header_timestamp, mode='lines+markers', name="Stddev", yaxis='y2',
                                          visible='legendonly'))

        if 'spread' in dataFrame.columns:
            lines.append(plotlygo.Scatter(y=dataFrame['spread'], x=dataFrame.header_timestamp, mode='lines+markers', name="Spread", yaxis='y2',
                                          visible='legendonly'))

    data = plotlygo.Data(lines)
    layout = plotlygo.Layout(width=1100, height=650, yaxis=dict(title='Number of Packages', side='right'),
                             yaxis2=dict(title='Dimension Value', overlaying='y', side='left'))
    plotly.iplot(plotlygo.Figure(data=data, layout=layout))


#####################################
#            Widget Utils           #
#####################################

import arrow  # Better dates and times for Python


def mapDevicePortsToDropdownWidget(edgeid):
    portMapping = {}

    response = httpGetRequest('/describe/device/{0}/ports/last?precision=ms'.format(edgeid))

    if response.status_code == 200:
        d = json.loads(response.text)
        for port in d['ports']:
            label = "{0:3} | {1:25} ({2})".format(
                port['port'],
                translateThingCode(port["dimension_thing_code"]),
                arrow.get(port["header_timestamp"] / 1000, tzinfo=tz.gettz('America/Sao_Paulo')).humanize()
            )

            portMapping[label] = port['port']
        return portMapping

    else:
        raise Exception('Couldn\'t retrieve data')


def mapDevicePortSensorsToDropdownWidget(edgeid, port):
    sensorMapping = {}

    response = httpGetRequest('/describe/device/{0}/port/{1}/sensors/last?precision=ms'.format(edgeid, port))

    if response.status_code == 200:
        d = json.loads(response.text)
        for sensor in d['sensors']:
            label = "{0:3} | {1:25} | {2:6}{3:15} ({4})".format(
                sensor['sensor'],
                translateDimensionCode(sensor["dimension_code"]),
                sensor["dimension_value"],
                translateUnityCode(sensor["dimension_unity_code"]),
                arrow.get(sensor["header_timestamp"] / 1000, tzinfo=tz.gettz('America/Sao_Paulo')).humanize()
            )

            sensorMapping[label] = sensor['sensor']
        return sensorMapping

    else:
        raise Exception('Couldn\'t retrieve data')


def mapDevicePortSensorDimensionsToDropdownWidget(edgeid, port, sensor):
    dimensionMapping = {}

    response = httpGetRequest(
        '/describe/device/{0}/port/{1}/sensor/{2}/dimensions/last?precision=ms'.format(edgeid, port, sensor))

    if response.status_code == 200:
        d = json.loads(response.text)
        for dimension in d['dimensions']:
            label = "{0:3} | {1:25} | {2:6}{3:15} ({4})".format(
                dimension['dimension_code'],
                translateDimensionCode(dimension["dimension_code"]),
                dimension["dimension_value"],
                translateUnityCode(dimension["dimension_unity_code"]),
                arrow.get(dimension["header_timestamp"] / 1000, tzinfo=tz.gettz('America/Sao_Paulo')).humanize()
            )

            dimensionMapping[label] = dimension['dimension_code']
        return dimensionMapping

    else:
        raise Exception('Couldn\'t retrieve data')


#####################################
#         Portia Labeling           #
#####################################

from enum import Enum


default_unity_codes = {
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


default_thing_codes = {
    0: 'NotSpecified',
    1: 'Sensor_Agriness_TU',
    2: 'Sensor_Agriness_AirQ',
    3: 'Collector_Agriness_Hydro_v1',
    4: 'Sensor_Agriness_AnimalScale',
    5: 'Collector_Agriness_CycleCounter_v1',
    6: 'Collector_Inobram_Smaai_v5',
    7: 'Sensor_Agriness_HydroEDN15-100',
    8: 'Sensor_Agriness_HydroQMS',
    9: 'Sensor_Agriness_HydroTemp',
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
    69: 'Collector_Inobram_Ambientte_v3'
}


default_dimension_codes = {
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
        32: 'Point Angulation'
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
        32: 'Angulação Pontual'
    }
}


def humanize(df, datetime=False, locale='en-us', custom_unity_codes=None,
             custom_dimension_codes=None):
    """Humanizes a data frame's content by translating its columns data to
    actual text.

    Parameters
    ----------
    df -- the data frame to be humanized
    datetime -- if the header_timestamp column should be humanized too
    (default False)
    locale -- which language to use when humanizing (default 'en-us')
    custom_unity_codes -- a dictionary with custom unity codes to use when
    translating (default None)
    custom_dimension_codes -- a dictionary with custom dimension codes to use
    when translating (default None)
    """

    for index, row in df.iterrows():

        if datetime == True:
            datetime_locale = locale.replace('-', '_')
            if datetime_locale == 'pt-br':
                datetime_locale = 'pt'

            df['header_timestamp'] = df['header_timestamp'].astype(str)

            df.at[index, 'header_timestamp'] = arrow.get(
                int(row['header_timestamp']) / 1000,
                tzinfo=tz.gettz('America/Sao_Paulo')
            ).humanize(locale=datetime_locale)

        if 'dimension_code' in df.columns:
            df['dimension_code'] = df['dimension_code'].astype(str)
            df.at[index, 'dimension_code'] = translateDimensionCode(
                row['dimension_code'], locale, custom_dimension_codes)

        if 'dimension_unity_code' in df.columns:
            df['dimension_unity_code'] = df['dimension_unity_code'].astype(str)
            df.at[index, 'dimension_unity_code'] = translateUnityCode(
                row['dimension_unity_code'], locale, custom_unity_codes)

        if 'dimension_thing_code' in df.columns:
            df['dimension_thing_code'] = df['dimension_thing_code'].astype(str)
            df.at[index, 'dimension_thing_code'] = translateThingCode(
                row['dimension_thing_code'])

    if datetime == True:
        df.rename(columns={'header_timestamp': 'header_datetime'},
                  inplace=True)
    if 'dimension_code' in df.columns:
        df.rename(columns={'dimension_code': 'dimension'},
                  inplace=True)
    if 'dimension_unity_code' in df.columns:
        df.rename(columns={'dimension_unity_code': 'dimension_unity'},
                  inplace=True)
    if 'dimension_thing_code' in df.columns:
        df.rename(columns={'dimension_thing_code': 'dimension_thing'},
                  inplace=True)

    return df


def humanizeJson(json_, datetime=False, locale='en-us',
                 custom_unity_codes=None, custom_dimension_codes=None):
    """Humanizes a JSON object's content by translating its data to actual
    text.

    Parameters
    ----------
    json_ -- the JSON object to be humanized
    datetime -- if the header_timestamp column should be humanized too
    (default False)
    locale -- which language to use when humanizing (default 'en-us')
    custom_unity_codes -- a dictionary with custom unity codes to use when
    translating (default None)
    custom_dimension_codes -- a dictionary with custom dimension codes to use
    when translating (default None)
    """
    
    json_['thing_code'] = translateThingCode(json_['thing_code'])

    for port in json_['ports']:
        port['thing_code'] = translateThingCode(port['thing_code'])

        for sensor in port['sensors']:

            if datetime == True:
                datetime_locale = locale.replace('-', '_')
                if datetime_locale == 'pt-br':
                    datetime_locale = 'pt'

                sensor['last_package']['header_datetime'] = arrow.get(
                    sensor['last_package']['header_timestamp'] / 1000,
                    tzinfo=tz.gettz('America/Sao_Paulo')
                ).humanize(locale=datetime_locale)
                del sensor['last_package']['header_timestamp']

            sensor['last_package']['dimension'] = translateDimensionCode(
                sensor['last_package']['dimension_code'], locale,
                custom_dimension_codes)
            sensor['last_package']['dimension_unity'] = translateUnityCode(
                sensor['last_package']['dimension_unity_code'], locale,
                custom_unity_codes)
            sensor['last_package']['dimension_thing'] = translateThingCode(
                sensor['last_package']['dimension_thing_code'])

            del sensor['last_package']['dimension_code']
            del sensor['last_package']['dimension_unity_code']
            del sensor['last_package']['dimension_thing_code']

    return json_


def translateUnityCode(unity_code, locale='en-us', custom_unity_codes=None):

    if custom_unity_codes is None:
        if default_unity_codes.get(locale) is None or \
           default_unity_codes.get(locale).get(unity_code) is None:
            return 'Unity Code {}'.format(unity_code)
        else:
            return default_unity_codes.get(locale).get(unity_code)
    else:
        if not isinstance(custom_unity_codes, dict) or \
           custom_unity_codes.get(locale) is None or \
           not isinstance(custom_unity_codes.get(locale), dict) or \
           custom_unity_codes.get(locale).get(unity_code) is None:
            return 'Unity Code {}'.format(unity_code)
        else:
            return custom_unity_codes.get(locale).get(unity_code)


def translateThingCode(thing_code):

    if default_thing_codes.get(thing_code) is None:
        return 'Thing Code {}'.format(thing_code)
    else:
        return default_thing_codes.get(thing_code)


def translateDimensionCode(dimension_code, locale='en-us',
                           custom_dimension_codes=None):

    dimension_code = int(dimension_code)

    if custom_dimension_codes is None:
        if default_dimension_codes.get(locale) is None or \
           default_dimension_codes.get(locale).get(dimension_code) is None:
            return 'Dimension Code {}'.format(dimension_code)
        else:
            return default_dimension_codes.get(locale).get(dimension_code)
    else:
        if not isinstance(custom_dimension_codes, dict) or \
           custom_dimension_codes.get(locale) is None or \
           not isinstance(custom_dimension_codes.get(locale), dict) or \
           custom_dimension_codes.get(locale).get(dimension_code) is None:
            return 'Dimension Code {}'.format(dimension_code)
        else:
            return custom_dimension_codes.get(locale).get(dimension_code)


#####################################
#         Converter Types           #
#####################################

from io import StringIO  # Read and write strings as files
import pandas  # Data analysis tools for Python
import json


def convert_csv(response, portiaConfig):
    if response.status_code == 200:
        try:
            dimensionSeries = pandas.read_csv(StringIO(response.text), sep=';')
            if portiaConfig['debug']:
                print('[portia-debug]: {0} rows'.format(len(dimensionSeries.index)))

            return dimensionSeries
        except Exception as err:
            raise Exception('couldn\'t create pandas data frame: {0}'.format(err))
    else:
        raise Exception('couldn\'t retrieve data')


def convert_json(response, portiaConfig):
    if response.status_code == 200:
        dimensionSeries = json.loads(response.text)
        if portiaConfig['debug']:
            print('[portia-debug]: {0}'.format(dimensionSeries))

        return dimensionSeries
    else:
        err = json.loads(response.text)
        raise Exception('couldn\'t retrieve data: {0}'.format(err['message']))


response_convert = {
    'text/csv': convert_csv,
    'application/json': convert_json
}
