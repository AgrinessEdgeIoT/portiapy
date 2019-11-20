#####################################    
#              Portia               #
#####################################

# Libraries
import pandas                     # Data analysis tools for Python
import types					  # Names for built-in types
import builtins

import portiapy.phases as phases
import portiapy.axioms as axioms
import portiapy.specs as specs

import portiapy.describe as describe
import portiapy.profile as profile
import portiapy.select as select
import portiapy.summary as summary

import portiapy.utils as utils

# Functions
def about():
    print("portiapy.device - an Agriness Edge project")

class CustomDict(dict):
	def humanize(self, datetime=False, locale='en-us', custom_unity_codes=None,
                 custom_dimension_codes=None):
		return utils.humanizeJson(self, datetime, locale, custom_unity_codes,
                 				  custom_dimension_codes)

def addHumanizeFunction(obj):
	if isinstance(obj, pandas.DataFrame):
		obj.humanize = types.MethodType( utils.humanize, obj )
	elif isinstance(obj, dict):
		obj = CustomDict(obj)
	return obj

# Classes

########################################
# PortiaApi
# A factory for devices that use our Portia API
class PortiaApi:

	########################################
	# __init__
	# - Constructor for PortiaApi
	def __init__(self, portiaConfig):
		self.portiaConfig = portiaConfig

	########################################
	# pipeline
	# - Instantiates a new EdgePipeline
	def pipeline(self):
		return EdgePipeline(self.portiaConfig)

	########################################
	# device
	# - Instantiates a new EdgeDevice
	def device(self, edgeId):
		return EdgeDevice(edgeId, self.portiaConfig)

# class PortiaApi

########################################
# EdgePipeline
# /pipeline...
class EdgePipeline:

	########################################
	# __init__
	# - Constructor for EdgePipeline
	def __init__(self, portiaConfig):
		self.portiaConfig = portiaConfig

	########################################
	# phase
	# - Instantiates a new EdgePipelinePhase
	def phase(self):
		return EdgePipelinePhase(self.portiaConfig)

	########################################
	# axiom
	# - Instantiates a new EdgePipelineAxiom
	def axiom(self):
		return EdgePipelineAxiom(self.portiaConfig)

	########################################
	# specification
	# - Instantiates a new EdgePipelineSpecification
	def specification(self):
		return EdgePipelineSpecification(self.portiaConfig)

# class EdgePipeline

########################################
# EdgePipelinePhase
# /pipeline/phases/...
class EdgePipelinePhase:

	########################################
	# __init__
	# - Constructor for EdgePipelinePhase
	def __init__(self, portiaConfig):
		self.portiaConfig = portiaConfig

	############################# CRUD #############################
	def list(self):
		return phases.index(self.portiaConfig)

	def create(self, payload):
		return phases.store(self.portiaConfig, payload)

	def display(self, phaseName):
		return phases.show(self.portiaConfig, phaseName)

	def update(self, phaseName, payload):
		return phases.update(self.portiaConfig, phaseName, payload)

# class EdgePipelinePhase

########################################
# EdgePipelineAxiom
# /pipeline/axioms/...
class EdgePipelineAxiom:

	########################################
	# __init__
	# - Constructor for EdgePipelineAxiom
	def __init__(self, portiaConfig):
		self.portiaConfig = portiaConfig

	############################# CRUD #############################
	def list(self):
		return axioms.index(self.portiaConfig)

	def create(self, payload):
		return axioms.store(self.portiaConfig, payload)

	def display(self, axiomName, showParams=False):
		return axioms.show(self.portiaConfig, axiomName, showParams)

	def update(self, axiomName, payload):
		return axioms.update(self.portiaConfig, axiomName, payload)

	def delete(self, axiomName):
		return axioms.destroy(self.portiaConfig, axiomName)

# class EdgePipelineAxiom

########################################
# EdgePipelineSpecification
# /pipeline/axioms/...
class EdgePipelineSpecification:

	########################################
	# __init__
	# - Constructor for EdgePipelineSpecification
	def __init__(self, portiaConfig):
		self.portiaConfig = portiaConfig

	############################# CRUD #############################
	def list(self):
		return specs.index(self.portiaConfig)

	def create(self, payload):
		return specs.store(self.portiaConfig, payload)

	def display(self, specName):
		return specs.show(self.portiaConfig, specName)

	def update(self, specName, payload):
		return specs.update(self.portiaConfig, specName, payload)

	def delete(self, specName):
		return specs.destroy(self.portiaConfig, specName)

# class EdgePipelineSpecification

########################################
# EdgeDevice
# /device/:device/...
class EdgeDevice:

	########################################
	# __init__
	# - Constructor for EdgeDevice
	def __init__(self, edgeId, portiaConfig):
		self.edgeId = edgeId
		self.portiaConfig = portiaConfig

	########################################
	# port
	# - Instantiates a new EdgeDevicePort
	def port(self, port):
		return EdgeDevicePort(self, port, self.portiaConfig)

	########################### Describe ###########################
	def ports(self, last=False, params=None):
		if params is None:
			return addHumanizeFunction( describe.devicePorts(self.portiaConfig, self.edgeId, last) )
		else:
			return addHumanizeFunction( describe.devicePorts(self.portiaConfig, self.edgeId, last, params) )

	########################### Profile ############################
	def profile(self, strategy=profile.ProfileStrategies.BY_ZERO_PORT, interval=30, params=None):
		if params is None:
			return addHumanizeFunction( profile.deviceProfile(self.portiaConfig, self.edgeId, strategy, interval) )
		else:
			return addHumanizeFunction( profile.deviceProfile(self.portiaConfig, self.edgeId, strategy, interval, params) )

# class EdgeDevice

########################################
# EdgeDevicePort
# /device/:device/port/:port/...
class EdgeDevicePort:

	########################################
	# __init__
	# - Constructor for EdgeDevicePort
	def __init__(self, edgeDevice, port, portiaConfig):
		self.edgeId = edgeDevice.edgeId
		self.port = port
		self.portiaConfig = portiaConfig

	########################################
	# sensor
	# - Instantiates a new EdgeDeviceSensor
	def sensor(self, sensor):
		return EdgeDeviceSensor(self, sensor, self.portiaConfig)

	########################################
	# dimension
	# - Instantiates a new EdgeDeviceDimension
	def dimension(self, dimension):
		return EdgeDeviceDimensionFromPort(self, dimension, self.portiaConfig)

	########################### Describe ###########################
	def sensors(self, last=False, params=None):
		if params is None:
			return addHumanizeFunction( describe.devicePortSensors(self.portiaConfig, self.edgeId, self.port, last) )
		else:
			return addHumanizeFunction( describe.devicePortSensors(self.portiaConfig, self.edgeId, self.port, last, params) )

	def dimensions(self, last=False, params=None):
		if params is None:
			return addHumanizeFunction( describe.devicePortDimensions(self.portiaConfig, self.edgeId, self.port, last) )
		else:
			return addHumanizeFunction( describe.devicePortDimensions(self.portiaConfig, self.edgeId, self.port, last, params) )

	########################### Profile ############################
	def profile(self, strategy=profile.ProfileStrategies.BY_ZERO_PORT, interval=30, params=None):
		if params is None:
			return addHumanizeFunction( profile.portProfile(self.portiaConfig, self.edgeId, self.port, strategy, interval) )
		else:
			return addHumanizeFunction( profile.portProfile(self.portiaConfig, self.edgeId, self.port, strategy, interval, params) )

# class EdgeDevicePort

########################################
# EdgeDeviceSensor
# /device/:device/port/:port/sensor/:sensor/...
class EdgeDeviceSensor:

	########################################
	# __init__
	# - Constructor for EdgeDeviceSensor
	def __init__(self, edgeDevicePort, sensor, portiaConfig):
		self.edgeId = edgeDevicePort.edgeId
		self.port = edgeDevicePort.port
		self.sensor = sensor
		self.portiaConfig = portiaConfig

	########################################
	# dimension
	# - Instantiates a new EdgeDeviceDimension
	def dimension(self, dimension):
		return EdgeDeviceDimensionFromSensor(self, dimension, self.portiaConfig)

	########################### Describe ###########################
	def dimensions(self, last=False, params=None):
		if params is None:
			return addHumanizeFunction( describe.devicePortSensorDimensions(self.portiaConfig, self.edgeId, self.port, self.sensor, last) )
		else:
			return addHumanizeFunction( describe.devicePortSensorDimensions(self.portiaConfig, self.edgeId, self.port, self.sensor, last, params) )

	########################### Profile ############################
	def profile(self, strategy=profile.ProfileStrategies.BY_ZERO_PORT, interval=30, params=None):
		if params is None:
			return addHumanizeFunction( profile.sensorProfile(self.portiaConfig, self.edgeId, self.port, self.sensor, strategy, interval) )
		else:
			return addHumanizeFunction( profile.sensorProfile(self.portiaConfig, self.edgeId, self.port, self.sensor, strategy, interval, params) )

	############################ Select ############################
	def select(self, last=False, params=None):
		if params is None:
			return addHumanizeFunction( select.queryByPortSensor(self.portiaConfig, self.edgeId, self.port, self.sensor, last) )
		else:
			return addHumanizeFunction( select.queryByPortSensor(self.portiaConfig, self.edgeId, self.port, self.sensor, last, params) )

	########################### Summary ############################
	def summary(self, strategy=summary.SummaryStrategies.PER_HOUR, interval=1, params=None):
		if params is None:
			return summary.queryByPortSensor(self.portiaConfig, self.edgeId, self.port, self.sensor, strategy, interval)
		else:
			return summary.queryByPortSensor(self.portiaConfig, self.edgeId, self.port, self.sensor, strategy, interval, params)

# class EdgeDeviceSensor

########################################
# EdgeDeviceDimensionFromPort
# /device/:device/port/:port/dimension/:dimension/...
class EdgeDeviceDimensionFromPort:

	########################################
	# __init__
	# - Constructor for EdgeDeviceDimensionFromPort
	def __init__(self, edgeDevicePort, dimension, portiaConfig):
		self.edgeId = edgeDevicePort.edgeId
		self.port = edgeDevicePort.port
		self.dimension = dimension
		self.portiaConfig = portiaConfig

	############################ Select ############################
	def select(self, last=False, params=None):
		if params is None:
			return addHumanizeFunction( select.queryByPortDimension(self.portiaConfig, self.edgeId, self.port, self.dimension, last) )
		else:
			return addHumanizeFunction( select.queryByPortDimension(self.portiaConfig, self.edgeId, self.port, self.dimension, last, params) )

# class EdgeDeviceDimensionFromPort

########################################
# EdgeDeviceDimensionFromSensor
# /device/:device/port/:port/sensor/:sensor/dimension/:dimension/...
class EdgeDeviceDimensionFromSensor:

	########################################
	# __init__
	# - Constructor for EdgeDeviceDimensionFromSensor
	def __init__(self, edgeDeviceSensor, dimension, portiaConfig):
		self.edgeId = edgeDeviceSensor.edgeId
		self.port = edgeDeviceSensor.port
		self.sensor = edgeDeviceSensor.sensor
		self.dimension = dimension
		self.portiaConfig = portiaConfig

	############################ Select ############################
	def select(self, last=False, params=None):
		if params is None:
			return addHumanizeFunction( select.queryByPortSensorDimension(self.portiaConfig, self.edgeId, self.port, self.sensor, self.dimension, last) )
		else:
			return addHumanizeFunction( select.queryByPortSensorDimension(self.portiaConfig, self.edgeId, self.port, self.sensor, self.dimension, last, params) )

	########################### Summary ############################
	def summary(self, strategy=summary.SummaryStrategies.PER_HOUR, interval=1, params=None):
		if params is None:
			return summary.queryByPortSensorDimension(self.portiaConfig, self.edgeId, self.port, self.sensor, self.dimension, strategy, interval)
		else:
			return summary.queryByPortSensorDimension(self.portiaConfig, self.edgeId, self.port, self.sensor, self.dimension, strategy, interval, params)

# class EdgeDeviceDimensionFromSensor
