#####################################
#               Phases              #
#####################################

# Libraries
import json                       # JSON encoder and decoder
import portiapy.utils as utils

# Functions
def about():
    print("portiapy.describe - an Agriness Edge project")

########################################
# index
########################################
# /pipeline/phases
########################################
def index(portiaConfig):

	endpoint = '/pipeline/phases'
	response = utils.httpGetRequest(portiaConfig, endpoint)

	if response.status_code == 200:

		d = json.loads(response.text)
		if portiaConfig['debug']:
			print( '[portia-debug]: {0}'.format(d) )

		return d

	else:

		d = json.loads(response.text)
		raise Exception( 'couldn\'t retrieve data: {0}'.format(d['message']) )

########################################
# store
########################################
# /pipeline/phases
########################################
def store(portiaConfig, payload):

	endpoint = '/pipeline/phases'
	response = utils.httpPostRequest(portiaConfig, endpoint, payload)

	if response.status_code == 200:

		d = json.loads(response.text)
		if portiaConfig['debug']:
			print( '[portia-debug]: {0}'.format(d) )

		return d

	else:

		d = json.loads(response.text)
		raise Exception( 'couldn\'t retrieve data: {0}'.format(d['message']) )

########################################
# show
########################################
# /pipeline/phases/:phase
########################################
def show(portiaConfig, phaseName):

	endpoint = '/pipeline/phases/{0}'.format(phaseName)
	response = utils.httpGetRequest(portiaConfig, endpoint)

	if response.status_code == 200:

		d = json.loads(response.text)
		if portiaConfig['debug']:
			print( '[portia-debug]: {0}'.format(d) )

		return d

	else:

		d = json.loads(response.text)
		raise Exception( 'couldn\'t retrieve data: {0}'.format(d['message']) )

########################################
# update
########################################
# /pipeline/phases/:phase
########################################
def update(portiaConfig, phaseName, payload):

	endpoint = '/pipeline/phases/{0}'.format(phaseName)
	response = utils.httpPutRequest(portiaConfig, endpoint, payload)

	if response.status_code == 200:

		d = json.loads(response.text)
		if portiaConfig['debug']:
			print( '[portia-debug]: {0}'.format(d) )

		return d

	else:

		d = json.loads(response.text)
		raise Exception( 'couldn\'t retrieve data: {0}'.format(d['message']) )
