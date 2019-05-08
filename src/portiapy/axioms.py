#####################################
#               Axioms              #
#####################################

# Libraries
import json                       # JSON encoder and decoder
import portiapy.utils as utils

# Functions
def about():
    print("portiapy.axioms - an Agriness Edge project")

########################################
# index
########################################
# /pipeline/axioms
########################################
def index(portiaConfig):

	endpoint = '/pipeline/axioms'
	response = utils.httpGetRequest(portiaConfig, endpoint)

	if response.status_code == 200:

		d = json.loads(response.text)
		if portiaConfig['debug']:
			print( '[portia-debug]: {0}'.format(d) )

		return d

	else:

		d = json.loads(response.text)
		raise Exception( 'couldn\'t list axioms: {0}'.format(d['message']) )

########################################
# store
########################################
# /pipeline/axioms
########################################
def store(portiaConfig, payload):

	endpoint = '/pipeline/axioms'
	response = utils.httpPostRequest(portiaConfig, endpoint, payload)

	if response.status_code == 200:

		d = json.loads(response.text)
		if portiaConfig['debug']:
			print( '[portia-debug]: {0}'.format(d) )

		return d

	else:

		d = json.loads(response.text)
		raise Exception( 'couldn\'t create axiom: {0}'.format(d['message']) )

########################################
# show
########################################
# /pipeline/axioms/:axiom
########################################
def show(portiaConfig, axiomName, params=False):

	if params == False:
		endpoint = '/pipeline/axioms/{0}'.format(axiomName)
	else:
		endpoint = '/pipeline/axioms/{0}/params'.format(axiomName)

	response = utils.httpGetRequest(portiaConfig, endpoint)

	if response.status_code == 200:

		d = json.loads(response.text)
		if portiaConfig['debug']:
			print( '[portia-debug]: {0}'.format(d) )

		return d

	else:

		d = json.loads(response.text)
		raise Exception( 'couldn\'t show axiom: {0}'.format(d['message']) )

########################################
# update
########################################
# /pipeline/axioms/:axiom
########################################
def update(portiaConfig, axiomName, payload):

	endpoint = '/pipeline/axioms/{0}'.format(axiomName)
	response = utils.httpPutRequest(portiaConfig, endpoint, payload)

	if response.status_code == 200:

		d = json.loads(response.text)
		if portiaConfig['debug']:
			print( '[portia-debug]: {0}'.format(d) )

		return d

	else:

		d = json.loads(response.text)
		raise Exception( 'couldn\'t update axiom: {0}'.format(d['message']) )

########################################
# destroy
########################################
# /pipeline/axioms/:axiom
########################################
def destroy(portiaConfig, axiomName):

	endpoint = '/pipeline/axioms/{0}'.format(axiomName)
	response = utils.httpDeleteRequest(portiaConfig, endpoint)

	if response.status_code == 200:

		d = json.loads(response.text)
		if portiaConfig['debug']:
			print( '[portia-debug]: {0}'.format(d) )

		return d

	else:

		d = json.loads(response.text)
		raise Exception( 'couldn\'t destroy axiom: {0}'.format(d['message']) )
