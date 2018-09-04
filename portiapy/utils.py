#####################################
#              Commons              #
#####################################

# Libraries
from datetime import date, datetime, timedelta, timezone    # Basic date and time types
import copy                                                 # Shallow and deep copy operations
import json                                                 # JSON encoder and decoder
import time                                                 # Time access and conversions

# Functions
def about():
    print('portiapy.utils - an Agriness Edge project')

#####################################
#        REST API Management        #
#####################################

import requests     # Simple HTTP library
    
def httpGetRequest(portiaConfig, endpoint, headers=None):

    h = { 'Authorization': 'Bearer {0}'.format(portiaConfig['authorization']) }
    if headers is not None:
        h = { **h, **headers }  # Takes the arguments and turn them into a dictionary

    url = '{0}{1}'.format(portiaConfig['baseurl'], endpoint)

    start = time.time()
    response = requests.get(url, headers=h)
    end = time.time()
    elapsed = end - start

    if portiaConfig['debug'] == True:
        print('[portia-debug]: status: {0} | {1:.4f} sec. | {2}'.format(response.status_code, elapsed, url))

    return response

def httpPostRequest(portiaConfig, endpoint, payload, headers=None):

    h = { 'Authorization': 'Bearer {0}'.format(portiaConfig['authorization']) }
    if headers is not None:
        h = { **h, **headers }  # Takes the arguments and turn them into a dictionary

    url = '{0}{1}'.format(portiaConfig['baseurl'], endpoint)

    start = time.time()
    response = requests.post(url, headers=h, json=payload)
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

            # Padronizing values
            if value == True:
                value = 'true'
            elif value == False:
                value = 'false'

            getParams += '{0}={1}'.format(key, value)

    return getParams

#####################################
#            Plotting               #
#####################################

from dateutil import tz                                         # Powerful extensions to datetime
import pandas                                                   # Data analysis tools for Python
import plotly.graph_objs as plotlygo                            # Modern visualization for the data era
import plotly.offline as plotly
import pytz                                                     # World timezone definitions for Python

def plotSummaryfromDataFrame(dataFrame, timezone='Etc/GMT-3'):     

    plotly.offline.init_notebook_mode(connected=False)

    tz = pytz.timezone(timezone)
    lines =[]
    timeAxis = []

    dataFrame['header_timestamp'] = pandas.to_datetime(dataFrame['header_timestamp'], unit='ms').dt.tz_localize('Etc/GMT-3')
    
    for i, line in enumerate( dataFrame['header_timestamp'] ):
        timeAxis.append( dataFrame['header_timestamp'][i] )

    lines.append(plotlygo.Bar( y=dataFrame['number_of_packages'], x=timeAxis, name="Packages", opacity=0.1 ))

    if 'min' in dataFrame.columns:
        lines.append( plotlygo.Scatter( y=dataFrame['min'],    x=timeAxis, mode='lines+markers', name="Min",    yaxis='y2' ) )
    if 'max' in dataFrame.columns:
        lines.append( plotlygo.Scatter( y=dataFrame['max'],    x=timeAxis, mode='lines+markers', name="Max",    yaxis='y2' ) )
    if 'sum' in dataFrame.columns:
        lines.append( plotlygo.Scatter( y=dataFrame['sum'],    x=timeAxis, mode='lines+markers', name="Sum",    yaxis='y2', visible='legendonly' ) )
    if 'avg' in dataFrame.columns:
        lines.append( plotlygo.Scatter( y=dataFrame['avg'],    x=timeAxis, mode='lines+markers', name="Avg",    yaxis='y2' ) )
    
    if 'median' in dataFrame.columns:
        lines.append( plotlygo.Scatter( y=dataFrame['median'], x=timeAxis, mode='lines+markers', name="Median", yaxis='y2' ) )
    if 'mode' in dataFrame.columns:
        lines.append( plotlygo.Scatter( y=dataFrame['mode'],   x=timeAxis, mode='lines+markers', name="Mode",   yaxis='y2' ) )
    if 'stddev' in dataFrame.columns:
        lines.append( plotlygo.Scatter( y=dataFrame['stddev'], x=timeAxis, mode='lines+markers', name="Stddev", yaxis='y2', visible='legendonly' ) )
    if 'spread' in dataFrame.columns:
        lines.append( plotlygo.Scatter( y=dataFrame['spread'], x=timeAxis, mode='lines+markers', name="Spread", yaxis='y2', visible='legendonly' ) )

    data = plotlygo.Data(lines)
    layout = plotlygo.Layout( width=1000, height=650, yaxis=dict(title='Number of Packages', side='right'), yaxis2=dict(title='Dimension Value', overlaying='y',side='left') )
    plotly.iplot( plotlygo.Figure(data=data, layout=layout) )    

#####################################
#            Widget Utils           #
#####################################

import arrow    # Better dates and times for Python

def mapDevicePortsToDropdownWidget(edgeid):
    portMapping = {}
    
    response = httpGetRequest( '/describe/device/{0}/ports/last?precision=ms'.format(edgeid) )

    if response.status_code == 200:
        d = json.loads(response.text)
        for port in d['ports']:

            label = "{0:3} | {1:25} ({2})".format(
                port['port'],
                translateThingCode(port["dimension_thing_code"]),
                arrow.get( port["header_timestamp"]/1000, tzinfo=tz.gettz('America/Sao_Paulo') ).humanize()
            )

            portMapping[label] = port['port']
        return portMapping
        
    else:
        raise Exception('Couldn\'t retrieve data')

def mapDevicePortSensorsToDropdownWidget(edgeid, port):
    sensorMapping = {}
    
    response = httpGetRequest( '/describe/device/{0}/port/{1}/sensors/last?precision=ms'.format(edgeid, port) )

    if response.status_code == 200:
        d = json.loads(response.text)
        for sensor in d['sensors']:

            label = "{0:3} | {1:25} | {2:6}{3:15} ({4})".format(
                sensor['sensor'],
                translateDimensionCode(sensor["dimension_code"]),
                sensor["dimension_value"],
                translateUnityCode(sensor["dimension_unity_code"]),
                arrow.get( sensor["header_timestamp"]/1000, tzinfo=tz.gettz('America/Sao_Paulo') ).humanize()
            )

            sensorMapping[label] = sensor['sensor']
        return sensorMapping
        
    else:
        raise Exception('Couldn\'t retrieve data')
        
def mapDevicePortSensorDimensionsToDropdownWidget(edgeid, port, sensor):
    dimensionMapping = {}
    
    response = httpGetRequest( '/describe/device/{0}/port/{1}/sensor/{2}/dimensions/last?precision=ms'.format(edgeid, port, sensor) )

    if response.status_code == 200:
        d = json.loads(response.text)
        for dimension in d['dimensions']:

            label = "{0:3} | {1:25} | {2:6}{3:15} ({4})".format(
                dimension['dimension_code'],
                translateDimensionCode(dimension["dimension_code"]),
                dimension["dimension_value"],
                translateUnityCode(dimension["dimension_unity_code"]),
                arrow.get( dimension["header_timestamp"]/1000, tzinfo=tz.gettz('America/Sao_Paulo') ).humanize()
            )
            
            dimensionMapping[label] = dimension['dimension_code']
        return dimensionMapping
        
    else:
        raise Exception('Couldn\'t retrieve data')
        
#####################################
#         Portia Labeling           #
#####################################

def translateUnityCode(unityCode):
    if unityCode == 0:
        return ' unidades'
    elif unityCode == 1:
        return 'ºC'
    elif unityCode == 2:
        return '%'
    elif unityCode == 3:
        return 'ppm'
    elif unityCode == 4:
        return 'L'
    elif unityCode == 5:
        return 'g'
    elif unityCode == 6:
        return 's'
    elif unityCode == 7:
        return 'L/min'
    elif unityCode == 8:
        return 'dBm'
    elif unityCode == 9:
        return 'B'
    elif unityCode == 10:
        return ''
    elif unityCode == 11:
        return ''
    elif unityCode == 12:
        return 'ms'
    elif unityCode == 13:
        return 'V'
    elif unityCode == 14:
        return 'Pa'
    elif unityCode == 15:
        return 'Kg'
    else:
        return ''

def translateThingCode(thingCode):
    if thingCode == 0:
        return 'Sem especificação'
    elif thingCode == 1:
        return 'SondaTU_v1'
    elif thingCode == 2:
        return 'SondaAirQ_v1'
    elif thingCode == 3:
        return 'HubHydro_v1'
    elif thingCode == 4:
        return 'SondaLoadCell_v1'
    elif thingCode == 5:
        return 'HubCycleCounter_v1'
    elif thingCode == 6:
        return 'VirtualHubSmaai5'
    elif thingCode == 7:
        return 'SondaHydroEDN15-100'
    elif thingCode == 8:
        return 'SondaHydroQMS_v1'
    elif thingCode == 9:
        return 'SondaHydroTemp_v1'
    elif thingCode == 10:
        return 'FarmBrain_v1'
    elif thingCode == 11:
        return 'HubUniversal_v1'
    elif thingCode == 12:
        return 'VirtualHubSmaai3'
    elif thingCode == 13:
        return 'VirtualHubSmaai4'
    elif thingCode == 14:
        return 'MiniFarmBrain_v1'
    elif thingCode == 15:
        return 'SondaSmaaiT'
    elif thingCode == 16:
        return 'SondaSmaaiTU'
    elif thingCode == 17:
        return 'SmaaiExhaustor'
    elif thingCode == 18:
        return 'SmaaiNebulizer'
    elif thingCode == 19:
        return 'SmaaiHeater'
    elif thingCode == 20:
        return 'SmaaiDimmer'
    elif thingCode == 21:
        return 'SondaSmaaiPE'
    elif thingCode == 22:
        return 'SondaSmaaiH2O'
    elif thingCode == 23:
        return 'SondaSmaaiCO2'
    elif thingCode == 28:
        return 'Ambientte'    
    else:
        return 'Desconhecido'

def translateDimensionCode(dimensionCode):
    dimensionCode = int(dimensionCode)
    if dimensionCode == 0:
        return ''
    elif dimensionCode == 1:
        return 'Temperatura Pontual'
    elif dimensionCode == 2:
        return 'Temperatura Média'
    elif dimensionCode == 3:
        return 'Umidade Pontual'
    elif dimensionCode == 4:
        return 'Umidade Média'
    elif dimensionCode == 5:
        return 'Concentração Pontual'
    elif dimensionCode == 6:
        return 'Concentração Média'
    elif dimensionCode == 7:
        return 'Fluxo Acumulado'
    elif dimensionCode == 8:
        return 'Fluxo Pontual'
    elif dimensionCode == 9:
        return 'Temperatura da Água Pontual'
    elif dimensionCode == 10:
        return 'Peso Pontual'
    elif dimensionCode == 11:
        return 'Peso Médio'
    elif dimensionCode == 12:
        return 'Estado do Dispositivo'
    elif dimensionCode == 13:
        return 'Concentração de CO2 Pontual'
    elif dimensionCode == 14:
        return 'Número de Ciclos'
    elif dimensionCode == 15:
        return 'Uptime'
    elif dimensionCode == 16:
        return 'RSSI'
    elif dimensionCode == 17:
        return 'Memória Livre'
    elif dimensionCode == 18:
        return 'Disco Livre'
    elif dimensionCode == 19:
        return 'Carga do Sistema'
    elif dimensionCode == 20:
        return 'Tamanho de Arquivo'
    elif dimensionCode == 21:
        return 'Tempo Momentâneo'
    elif dimensionCode == 22:
        return 'Perfil'
    elif dimensionCode == 23:
        return 'Alimentação do Dispositivo'
    elif dimensionCode == 24:
        return 'Pressão Pontual'
    elif dimensionCode == 25:
        return 'Pressão Média'
    elif dimensionCode == 26:
        return 'Modelo'
    else:
        return 'Desconhecido'
