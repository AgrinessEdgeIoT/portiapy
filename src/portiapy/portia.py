#####################################    
#              Device               #
#####################################

# Libraries
import pandas                     # Data analysis tools for Python
import types					  # Names for built-in types

import portiapy.describe as describe
import portiapy.profile as profile
import portiapy.select as select
import portiapy.summary as summary
import portiapy.utils as utils

# Functions
def about():
    print("portiapy.device - an Agriness Edge project")

def addHumanizeFunction(obj):
	if isinstance(obj, pandas.DataFrame):
		obj.humanize = types.MethodType( utils.humanize, obj )
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
	# device
	# - Instantiates a new EdgeDevice
	def device(self, edgeId):
		return EdgeDevice(edgeId, self.portiaConfig)

# class PortiaApi

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
			return profile.deviceProfile(self.portiaConfig, self.edgeId, strategy, interval)
		else:
			return profile.deviceProfile(self.portiaConfig, self.edgeId, strategy, interval, params)

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
			return profile.portProfile(self.portiaConfig, self.edgeId, self.port, strategy, interval)
		else:
			return profile.portProfile(self.portiaConfig, self.edgeId, self.port, strategy, interval, params)

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
			return profile.sensorProfile(self.portiaConfig, self.edgeId, self.port, self.sensor, strategy, interval)
		else:
			return profile.sensorProfile(self.portiaConfig, self.edgeId, self.port, self.sensor, strategy, interval, params)

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

# class EdgeDeviceDimension

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

# class EdgeDeviceDimension2
