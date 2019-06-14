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
        15: 'Kg',
        16: ' day(s)'
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
        15: 'Kg',
        16: ' dia(s)'
    }
}


default_thing_codes = {
    0: 'NotSpecified',
    1: 'ProbeTU_v1',
    2: 'ProbeAirQ_v1',
    3: 'HubHydro_v1',
    4: 'ProbeLoadCell_v1',
    5: 'HubCycleCounter_v1',
    6: 'HubSmaai5',
    7: 'ProbeHydroEDN15-100',
    8: 'ProbeHydroQMS_v1',
    9: 'ProbeHydroTemp_v1',
    10: 'Gateway_v0',
    11: 'HubUniversal_v1',
    12: 'HubSmaai3',
    13: 'HubSmaai4',
    14: 'Gateway_v1',
    15: 'ProbeSmaaiT',
    16: 'ProbeSmaaiTU',
    17: 'SmaaiExhaustor',
    18: 'SmaaiNebulizer',
    19: 'SmaaiHeater',
    20: 'SmaaiDimmer',
    21: 'ProbeSmaaiPE',
    22: 'ProbeSmaaiH2O',
    23: 'ProbeSmaaiCO2',
    24: 'ProbeSmaaiU',
    25: 'SmaaiSmartScale',
    26: 'SmaaiSiloWeight',
    27: 'VirtualGateway_v0',
    28: 'HubAmbientte',
    29: 'HubBluetooth_v1',
    30: 'ProbeTruTestS2'
}


default_dimension_codes = {
    'en-us': {
        0:  'Unamed Dimension',
        1:  'Punctual Temperature',
        2:  'Average Temperature',
        3:  'Punctual Humidity',
        4:  'Average Humidity',
        5:  'Punctual Concentration',
        6:  'Average Concentration',
        7:  'Cumulative Flow',
        8:  'Punctual Flow',
        9:  'Punctual Water Temperature',
        10: 'Punctual Weight',
        11: 'Average Weight',
        12: 'Status',
        13: 'Punctual CO2 Concentration',
        14: 'Number of Cycles',
        15: 'Cumulative Time',
        16: 'RSSI',
        17: 'Free Memory',
        18: 'Free Storage',
        19: 'System Load',
        20: 'File Size',
        21: 'Punctual Time',
        22: 'Profile',
        23: 'Punctual Voltage',
        24: 'Punctual Pressure',
        25: 'Average Pressure',
        26: 'Model',
        27: 'Lot Day',
        28: 'Average Voltage'
    },
    'pt-br': {
        0:  'Dimensão Anônima',
        1:  'Temperatura Pontual',
        2:  'Temperatura Média',
        3:  'Umidade Pontual',
        4:  'Umidade Média',
        5:  'Concentração Pontual',
        6:  'Concentração Média',
        7:  'Fluxo Acumulado',
        8:  'Fluxo Pontual',
        9:  'Temperatura da Água Pontual',
        10: 'Peso Pontual',
        11: 'Peso Médio',
        12: 'Estado',
        13: 'Concentração de CO2 Pontual',
        14: 'Número de Ciclos',
        15: 'Tempo Acumulado',
        16: 'RSSI',
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
        28: 'Tensão Elétrica Média'
    }
}


def humanize(df, datetime=False, locale='en-us', custom_unity_codes=None, custom_dimension_codes=None):

    for index, row in df.iterrows():

        if datetime == True:
            df['header_timestamp'] = df['header_timestamp'].astype(str)
            df.at[index, 'header_timestamp'] = arrow.get(int(row['header_timestamp']) / 1000,
                                                         tzinfo=tz.gettz('America/Sao_Paulo')).humanize()

        if 'dimension_code' in df.columns:
            df['dimension_code'] = df['dimension_code'].astype(str)
            df.at[index, 'dimension_code'] = translateDimensionCode(row['dimension_code'], locale, custom_dimension_codes)
        if 'dimension_unity_code' in df.columns:
            df['dimension_unity_code'] = df['dimension_unity_code'].astype(str)
            df.at[index, 'dimension_unity_code'] = translateUnityCode(row['dimension_unity_code'], locale, custom_unity_codes)
        if 'dimension_thing_code' in df.columns:
            df['dimension_thing_code'] = df['dimension_thing_code'].astype(str)
            df.at[index, 'dimension_thing_code'] = translateThingCode(row['dimension_thing_code'])

    if datetime == True:
        df.rename(columns={'header_timestamp': 'header_datetime'}, inplace=True)
    if 'dimension_code' in df.columns:
        df.rename(columns={'dimension_code': 'dimension'}, inplace=True)
    if 'dimension_unity_code' in df.columns:
        df.rename(columns={'dimension_unity_code': 'dimension_unity'}, inplace=True)
    if 'dimension_thing_code' in df.columns:
        df.rename(columns={'dimension_thing_code': 'dimension_thing'}, inplace=True)

    return df


def humanizeJson(json_, datetime=False, locale='en-us', custom_unity_codes=None,
                 custom_dimension_codes=None):
    
    json_['thing_code'] = translateThingCode(json_['thing_code'])

    for port in json_['ports']:
        port['thing_code'] = translateThingCode(port['thing_code'])

        for sensor in port['sensors']:

            if datetime == True:

                sensor['last_package']['header_datetime'] = arrow.get(
                    sensor['last_package']['header_timestamp'] / 1000,
                    tzinfo=tz.gettz('America/Sao_Paulo')
                ).humanize()
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
