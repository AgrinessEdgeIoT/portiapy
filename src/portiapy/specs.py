#####################################
#           Specifications          #
#####################################

# Libraries
import json                       # JSON encoder and decoder
import portiapy.utils as utils

# Functions
def about():
    print("portiapy.specs - an Agriness Edge project")

########################################
# index
########################################
# /pipeline/specs
########################################
def index(portiaConfig):

	endpoint = '/pipeline/specs'
	response = utils.httpGetRequest(portiaConfig, endpoint)

	if response.status_code == 200:

		d = json.loads(response.text)
		if portiaConfig['debug']:
			print( '[portia-debug]: {0}'.format(d) )

		return d

	else:

		d = json.loads(response.text)
		raise Exception( 'couldn\'t list specifications: {0}'.format(d['message']) )

########################################
# store
########################################
# /pipeline/specs
########################################
def store(portiaConfig, payload):

	endpoint = '/pipeline/specs'
	response = utils.httpPostRequest(portiaConfig, endpoint, payload)

	if response.status_code == 200:

		d = json.loads(response.text)
		if portiaConfig['debug']:
			print( '[portia-debug]: {0}'.format(d) )

		return d

	else:

		d = json.loads(response.text)
		raise Exception( 'couldn\'t create specification: {0}'.format(d['message']) )

########################################
# show
########################################
# /pipeline/specs/:spec
########################################
def show(portiaConfig, specName):

	endpoint = '/pipeline/specs/{0}'.format(specName)
	response = utils.httpGetRequest(portiaConfig, endpoint)

	if response.status_code == 200:

		d = json.loads(response.text)
		if portiaConfig['debug']:
			print( '[portia-debug]: {0}'.format(d) )

		return d

	else:

		d = json.loads(response.text)
		raise Exception( 'couldn\'t show specification: {0}'.format(d['message']) )

########################################
# update
########################################
# /pipeline/specs/:spec
########################################
def update(portiaConfig, specName, payload):

	endpoint = '/pipeline/specs/{0}'.format(specName)
	response = utils.httpPutRequest(portiaConfig, endpoint, payload)

	if response.status_code == 200:

		d = json.loads(response.text)
		if portiaConfig['debug']:
			print( '[portia-debug]: {0}'.format(d) )

		return d

	else:

		d = json.loads(response.text)
		raise Exception( 'couldn\'t update specification: {0}'.format(d['message']) )

########################################
# destroy
########################################
# /pipeline/specs/:spec
########################################
def destroy(portiaConfig, specName):

	endpoint = '/pipeline/specs/{0}'.format(specName)
	response = utils.httpDeleteRequest(portiaConfig, endpoint)

	if response.status_code == 200:

		d = json.loads(response.text)
		if portiaConfig['debug']:
			print( '[portia-debug]: {0}'.format(d) )

		return d

	else:

		d = json.loads(response.text)
		raise Exception( 'couldn\'t destroy specification: {0}'.format(d['message']) )
