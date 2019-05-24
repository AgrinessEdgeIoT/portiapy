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


def translateUnityCode(unity_code, locale='en-us', custom_unity_codes=None):
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
    if thing_code == 0:
        return 'NotSpecified'
    elif thing_code == 1:
        return 'ProbeTU_v1'
    elif thing_code == 2:
        return 'ProbeAirQ_v1'
    elif thing_code == 3:
        return 'HubHydro_v1'
    elif thing_code == 4:
        return 'ProbeLoadCell_v1'
    elif thing_code == 5:
        return 'HubCycleCounter_v1'
    elif thing_code == 6:
        return 'HubSmaai5'
    elif thing_code == 7:
        return 'ProbeHydroEDN15-100'
    elif thing_code == 8:
        return 'ProbeHydroQMS_v1'
    elif thing_code == 9:
        return 'ProbeHydroTemp_v1'
    elif thing_code == 10:
        return 'Gateway_v0'
    elif thing_code == 11:
        return 'HubUniversal_v1'
    elif thing_code == 12:
        return 'HubSmaai3'
    elif thing_code == 13:
        return 'HubSmaai4'
    elif thing_code == 14:
        return 'Gateway_v1'
    elif thing_code == 15:
        return 'ProbeSmaaiT'
    elif thing_code == 16:
        return 'ProbeSmaaiTU'
    elif thing_code == 17:
        return 'SmaaiExhaustor'
    elif thing_code == 18:
        return 'SmaaiNebulizer'
    elif thing_code == 19:
        return 'SmaaiHeater'
    elif thing_code == 20:
        return 'SmaaiDimmer'
    elif thing_code == 21:
        return 'ProbeSmaaiPE'
    elif thing_code == 22:
        return 'ProbeSmaaiH2O'
    elif thing_code == 23:
        return 'ProbeSmaaiCO2'
    elif thing_code == 24:
        return 'ProbeSmaaiU'
    elif thing_code == 25:
        return 'SmaaiSmartScale'
    elif thing_code == 26:
        return 'SmaaiSiloWeight'
    elif thing_code == 27:
        return 'VirtualGateway_v0'
    elif thing_code == 28:
        return 'HubAmbientte'
    elif thing_code == 29:
        return 'HubBluetooth_v1'
    elif thing_code == 30:
        return 'ProbeTruTestS2'
    else:
        return 'Thing Code {}'.format(thing_code)


def translateDimensionCode(dimension_code, locale='en-us',
                           custom_dimension_codes=None):
    dimension_code = int(dimension_code)

    default_dimension_codes = {
        'en-us': {
            0:  'Unamed Dimension',
            1:  'Punctual Temperature',
            2:  'Average Temperature',
            3:  'Punctual Umidity',
            4:  'Average Umidity',
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
