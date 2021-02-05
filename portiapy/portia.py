"""A class to abstract the usage of all endpoints.
"""

import types
import builtins

import pandas as pd

import portiapy.specs as specs
import portiapy.utils as utils
import portiapy.axioms as axioms
import portiapy.events as events
import portiapy.phases as phases
import portiapy.select as select
import portiapy.profile as profile
import portiapy.summary as summary
import portiapy.describe as describe


class CustomDict(dict):
	"""Custom dictionary with an humanization method.
	
	Extends:
		dict
	"""
	def humanize(
		self,
		locale='en-us',
		custom_dimension: dict=None,
		custom_event: dict=None,
		custom_unity: dict=None
	) -> dict:
		"""Humanizes dictionary.
		
		Keyword Arguments:
	        locale {str} -- which language to use when humanizing
	                        (default {'en-us'})
	        custom_dimension {dict} -- custom list of dimension codes
	                                   (default {None})
	        custom_event {dict} -- custom list of event codes (default {None})
	        custom_unity {dict} -- custom list of unity codes (default {None})
		
		Returns:
			dict -- humanized dictionary
		"""
		return utils.humanize_json(
			self, locale, custom_dimension, custom_unity
		)


def add_humanize_method(obj: object) -> object:
	"""Adds humanize method to an object's instance.
	
	Arguments:
		obj {object} -- object to have the method added
	
	Returns:
		object -- object with the humanize method
	"""
	if isinstance(obj, pd.DataFrame):
		obj.humanize = types.MethodType(utils.humanize_dataframe, obj)
	elif isinstance(obj, dict):
		obj = CustomDict(obj)

	return obj


class PortiaApi(object):
	"""A factory for devices that use our Portia API.
	"""
	def __init__(self, portia_config: dict):
		"""PortiaApi's constructor.
		
		Arguments:
			portia_config {dict} -- Portia's configuration arguments
		"""
		self.portia_config = portia_config

	def pipeline(self) -> 'EdgePipeline':
		"""Builds a new EdgePipeline instance.
		
		Returns:
			EdgePipeline -- EdgePipeline instance
		"""
		return EdgePipeline(self.portia_config)

	def device(self, edge_id: str) -> 'EdgeDevice':
		"""Builds a new EdgeDevice instance.
		
		Arguments:
			edge_id {str} -- Edge ID that identifies the device

		Returns:
			EdgeDevice -- EdgeDevice instance
		"""
		return EdgeDevice(edge_id, self.portia_config)


class EdgePipeline(object):
	"""Abstracts usage of pipeline endpoints.
	"""
	def __init__(self, portia_config: dict):
		"""EdgePipeline's constructor.
		
		Arguments:
			portia_config {dict} -- Portia's configuration arguments
		"""
		self.portia_config = portia_config

	def phase(self) -> 'EdgePipelinePhase':
		"""Builds a new EdgePipelinePhase instance.
		
		Returns:
			EdgePipelinePhase -- EdgePipelinePhase instance
		"""
		return EdgePipelinePhase(self.portia_config)

	def axiom(self) -> 'EdgePipelineAxiom':
		"""Builds a new EdgePipelineAxiom instance.
		
		Returns:
			EdgePipelineAxiom -- EdgePipelineAxiom instance
		"""
		return EdgePipelineAxiom(self.portia_config)

	def specification(self) -> 'EdgePipelineSpecification':
		"""Builds a new EdgePipelineSpecification instance.
		
		Returns:
			EdgePipelineSpecification -- EdgePipelineSpecification instance
		"""
		return EdgePipelineSpecification(self.portia_config)


class EdgePipelinePhase(object):
	"""Abstracts usage of pipeline phase endpoints.
	"""
	def __init__(self, portia_config: dict):
		"""EdgePipelinePhase's constructor.
		
		Arguments:
			portia_config {dict} -- Portia's configuration arguments
		"""
		self.portia_config = portia_config

	def list(self) -> list:
		return phases.index(self.portia_config)

	def create(self, payload):
		return phases.store(self.portia_config, payload)

	def display(self, phase_name):
		return phases.show(self.portia_config, phase_name)

	def update(self, phase_name, payload):
		return phases.update(self.portia_config, phase_name, payload)


class EdgePipelineAxiom(object):
	"""Abstracts usage of pipeline axiom endpoints.
	"""
	def __init__(self, portia_config: dict):
		"""EdgePipelineAxiom's constructor.
		
		Arguments:
			portia_config {dict} -- Portia's configuration arguments
		"""
		self.portia_config = portia_config

	def list(self):
		return axioms.index(self.portia_config)

	def create(self, payload):
		return axioms.store(self.portia_config, payload)

	def display(self, axiom_name, show_params=False):
		return axioms.show(self.portia_config, axiom_name, show_params)

	def update(self, axiom_name, payload):
		return axioms.update(self.portia_config, axiom_name, payload)

	def delete(self, axiom_name):
		return axioms.destroy(self.portia_config, axiom_name)


class EdgePipelineSpecification(object):
	"""Abstracts usage of pipeline specification endpoints.
	"""
	def __init__(self, portia_config: dict):
		"""EdgePipelineSpecification's constructor.
		
		Arguments:
			portia_config {dict} -- Portia's configuration arguments
		"""
		self.portia_config = portia_config

	def list(self):
		return specs.index(self.portia_config)

	def create(self, payload):
		return specs.store(self.portia_config, payload)

	def display(self, specName):
		return specs.show(self.portia_config, specName)

	def update(self, specName, payload):
		return specs.update(self.portia_config, specName, payload)

	def delete(self, specName):
		return specs.destroy(self.portia_config, specName)


class EdgeDevice(object):
	"""Abstracts usage of all Portia endpoints concerning data that only need
	an Edge ID.
	"""
	def __init__(self, edge_id: str, portia_config: dict):
		"""EdgeDevice's constructor.
		
		Arguments:
			edge_id {str} -- Edge ID that identifies the device
			portia_config {dict} -- Portia's configuration arguments
		"""
		self.edge_id = edge_id
		self.portia_config = portia_config

	def port(self, port: int) -> 'EdgeDevicePort':
		"""Builds a new EdgeDevicePort instance.
		
		Arguments:
			port {int} -- port of the device

		Returns:
			EdgeDevicePort -- EdgeDevicePort instance
		"""
		return EdgeDevicePort(self, port, self.portia_config)

	def dimension(self, dimension: int) -> 'EdgeDeviceDimensionFromDevice':
		"""Builds a new EdgeDeviceDimensionFromDevice instance.
		
		Arguments:
			dimension {int} -- dimension of the device

		Returns:
			EdgeDeviceDimensionFromDevice -- EdgeDeviceDimensionFromDevice
											 instance
		"""
		return EdgeDeviceDimensionFromDevice(
			self, dimension, self.portia_config
		)

	def ports(self, last: bool=False, params: dict=None) -> object:
		"""Lists a device's ports.
		
	    Keyword Arguments:
	        last {bool} -- if the last package of each port should be returned
	        			   or not (default: {False})
	        params {dict} -- params to send to the service (default: {None})

	    Returns:
	        object -- object with the list of ports
		"""
		return add_humanize_method(describe.device_ports(
			self.portia_config, self.edge_id, last, params
		))

	def profile(
		self,
		strategy: 'ProfileStrategies'=profile.ProfileStrategies.BY_ZERO_PORT,
		interval: int=30,
		params: dict=None
	) -> dict:
		"""Retrieves a device's profile.

	    Keyword Arguments:
	        strategy {ProfileStrategies} -- strategy to use when building the
	                                        profile (default: 
	                                        {ProfileStrategies.BY_ZERO_PORT})
	        interval {int} -- interval of time in minutes to build the profile
	                          (default: {30})
	        params {dict} -- params to send to the service (default: {None})
		
	    Returns:
	        dict -- dictionary with the device's profile
		"""
		return add_humanize_method(profile.device_profile(
			self.portia_config, self.edge_id, strategy, interval, params
		))


class EdgeDevicePort(object):
	"""Abstracts usage of all Portia endpoints concerning data that only need
	an Edge ID and a port.
	"""
	def __init__(
		self, edge_device: EdgeDevice, port: int, portia_config: dict
	):
		"""EdgeDevicePort's constructor.
		
		Arguments:
			edge_device {EdgeDevice} -- instance of an Edge device
			port {int} -- port of the device
			portia_config {dict} -- Portia's configuration arguments
		"""
		self.edge_id = edge_device.edge_id
		self.port = port
		self.portia_config = portia_config

	def sensor(self, sensor: int) -> 'EdgeDeviceSensor':
		"""Builds a new EdgeDeviceSensor instance.
		
		Arguments:
			sensor {int} -- sensor of the device

		Returns:
			EdgeDeviceSensor -- EdgeDeviceSensor instance
		"""
		return EdgeDeviceSensor(self, sensor, self.portia_config)

	def dimension(self, dimension: int) -> 'EdgeDeviceDimensionFromPort':
		"""Builds a new EdgeDeviceDimensionFromPort instance.
		
		Arguments:
			dimension {int} -- dimension code of the device

		Returns:
			EdgeDeviceDimensionFromPort -- EdgeDeviceDimensionFromPort instance
		"""
		return EdgeDeviceDimensionFromPort(self, dimension, self.portia_config)

	def sensors(self, last: bool=False, params: dict=None) -> object:
		"""Lists a device's sensors.
		
	    Keyword Arguments:
	        last {bool} -- if the last package of each sensor should be
	        			   returned or not (default: {False})
	        params {dict} -- params to send to the service (default: {None})

	    Returns:
	        object -- object with the list of sensors
		"""
		return add_humanize_method(describe.device_port_sensors(
			self.portia_config, self.edge_id, self.port, last, params
		))

	def dimensions(self, last: bool=False, params: dict=None) -> object:
		"""Lists a device's dimensions.
		
	    Keyword Arguments:
	        last {bool} -- if the last package of each dimension should be
	        			   returned or not (default: {False})
	        params {dict} -- params to send to the service (default: {None})

	    Returns:
	        object -- object with the list of dimensions
		"""
		return add_humanize_method(describe.device_port_dimensions(
			self.portia_config, self.edge_id, self.port, last, params
		))

	def profile(
		self,
		strategy: 'ProfileStrategies'=profile.ProfileStrategies.BY_ZERO_PORT,
		interval: int=30,
		params: dict=None
	) -> dict:
		"""Retrieves a port's profile.

	    Keyword Arguments:
	        strategy {ProfileStrategies} -- strategy to use when building the
	                                        profile (default: 
	                                        {ProfileStrategies.BY_ZERO_PORT})
	        interval {int} -- interval of time in minutes to build the profile
	                          (default: {30})
	        params {dict} -- params to send to the service (default: {None})
		
	    Returns:
	        dict -- dictionary with the port's profile
		"""
		return add_humanize_method(profile.port_profile(
			self.portia_config,
			self.edge_id,
			self.port,
			strategy,
			interval,
			params
		))


class EdgeDeviceSensor(object):
	"""Abstracts usage of all Portia endpoints concerning data that only need
	an Edge ID, a port and a sensor.
	"""
	def __init__(
		self,
		edge_device_port: EdgeDevicePort,
		sensor: int,
		portia_config: dict
	):
		"""EdgeDeviceSensor's constructor.
		
		Arguments:
			edge_device_port {EdgeDevicePort} -- instance of an Edge device
												 port
			sensor {int} -- sensor of the device
			portia_config {dict} -- Portia's configuration arguments
		"""
		self.edge_id = edge_device_port.edge_id
		self.port = edge_device_port.port
		self.sensor = sensor
		self.portia_config = portia_config

	def dimension(self, dimension: int) -> 'EdgeDeviceDimensionFromSensor':
		"""Builds a new EdgeDeviceDimensionFromSensor instance.
		
		Arguments:
			dimension {int} -- dimension code of the device

		Returns:
			EdgeDeviceDimensionFromSensor -- EdgeDeviceDimensionFromSensor
											 instance
		"""
		return EdgeDeviceDimensionFromSensor(
			self, dimension, self.portia_config
		)

	def event(self, event: int) -> 'EdgeDeviceEventFromSensor':
		"""Builds a new EdgeDeviceEventFromSensor instance.
		
		Arguments:
			event {int} -- event code of the device

		Returns:
			EdgeDeviceEventFromSensor -- EdgeDeviceEventFromSensor instance
		"""
		return EdgeDeviceEventFromSensor(self, event, self.portia_config)

	def dimensions(self, last: bool=False, params: dict=None) -> object:
		"""Lists a device's dimensions.
		
	    Keyword Arguments:
	        last {bool} -- if the last package of each dimension should be
	        			   returned or not (default: {False})
	        params {dict} -- params to send to the service (default: {None})

	    Returns:
	        object -- object with the list of dimensions
		"""
		return add_humanize_method(describe.device_port_sensor_dimensions(
			self.portia_config,
			self.edge_id,
			self.port,
			self.sensor,
			last,
			params
		))

	def profile(
		self,
		strategy: 'ProfileStrategies'=profile.ProfileStrategies.BY_ZERO_PORT,
		interval: int=30,
		params: dict=None
	) -> dict:
		"""Retrieves a sensor's profile.

	    Keyword Arguments:
	        strategy {ProfileStrategies} -- strategy to use when building the
	                                        profile (default: 
	                                        {ProfileStrategies.BY_ZERO_PORT})
	        interval {int} -- interval of time in minutes to build the profile
	                          (default: {30})
	        params {dict} -- params to send to the service (default: {None})
		
	    Returns:
	        dict -- dictionary with the sensor's profile
		"""
		return add_humanize_method(profile.sensor_profile(
			self.portia_config,
			self.edge_id,
			self.port,
			self.sensor,
			strategy,
			interval,
			params
		))

	def select(self, last: bool=False, params: dict=None) -> object:
		"""Retrieves a device's series by its port and sensor.

		Keyword Arguments:
			last {bool} -- if the last package should be returned or not
						   (default: {False})
			params {dict} -- params to send to the service (default: {None})

		Returns:
			object -- object with the device's dimensions
		"""
		return add_humanize_method(select.query_by_port_sensor(
			self.portia_config,
			self.edge_id,
			self.port,
			self.sensor,
			last,
			params
		))

	def summary(
		self,
		strategy: 'SummaryStrategies'=summary.SummaryStrategies.PER_HOUR,
		interval=1,
		params=None
	) -> object:
		"""Summarizes a device by port and sensor.

		Keyword Arguments:
			strategy {SummaryStrategies} -- strategy to use when summarizing
											(default:
											{SummaryStrategies.PER_HOUR})
			interval {int} -- interval of time to summarize (default: {1})
			params {dict} -- params to send to the service (default: {None})

		Returns:
			object -- object with the device's summarized dimensions
		"""
		return add_humanize_method(summary.query_by_port_sensor(
			self.portia_config,
			self.edge_id,
			self.port,
			self.sensor,
			strategy,
			interval,
			params
		))

	def events(self, last: bool=False, params: dict=None) -> object:
		"""Retrieves a device's events by its port and sensor.

		Keyword Arguments:
			last {bool} -- if the last event should be returned or not
						   (default: {False})
			params {dict} -- params to send to the service (default: {None})

		Returns:
			object -- object with the device's events
		"""
		return add_humanize_method(events.query_by_port_sensor(
			self.portia_config,
			self.edge_id,
			self.port,
			self.sensor,
			last,
			params
		))


class EdgeDeviceDimensionFromDevice(object):
	"""Abstracts usage of all Portia endpoints concerning data that only need
	an Edge ID and a dimension code.
	"""
	def __init__(
		self,
		edge_device: EdgeDevice,
		dimension: int,
		portia_config: dict
	):
		"""EdgeDeviceDimensionFromDevice's constructor.
		
		Arguments:
			edge_device {EdgeDevice} -- instance of an Edge device
			dimension {int} -- dimension code of the device
			portia_config {dict} -- Portia's configuration arguments
		"""
		self.edge_id = edge_device.edge_id
		self.dimension = dimension
		self.portia_config = portia_config

	def summary(
		self,
		series: list=None,
		strategy: 'SummaryStrategies'=summary.SummaryStrategies.PER_HOUR,
		interval=1,
		params=None
	) -> object:
		"""Summarizes a device by dimension code.

		Keyword Arguments:
			series {list} -- list of series to summarize (default: {None})
			strategy {SummaryStrategies} -- strategy to use when summarizing
											(default:
											{SummaryStrategies.PER_HOUR})
			interval {int} -- interval of time to summarize (default: {1})
			params {dict} -- params to send to the service (default: {None})

		Returns:
			object -- object with the device's summarized dimensions
		"""
		return add_humanize_method(summary.query_device_by_dimension(
			self.portia_config,
			self.edge_id,
			self.dimension,
			series,
			strategy,
			interval,
			params
		))


class EdgeDeviceDimensionFromPort(object):
	"""Abstracts usage of all Portia endpoints concerning data that only need
	an Edge ID, a port and a dimension code.
	"""
	def __init__(
		self,
		edge_device_port: EdgeDevicePort,
		dimension: int,
		portia_config: dict
	):
		"""EdgeDeviceDimensionFromPort's constructor.
		
		Arguments:
			edge_device_port {EdgeDevicePort} -- instance of an Edge device
												 port
			dimension {int} -- dimension code of the device
			portia_config {dict} -- Portia's configuration arguments
		"""
		self.edge_id = edge_device_port.edge_id
		self.port = edge_device_port.port
		self.dimension = dimension
		self.portia_config = portia_config

	def event(self, event: int) -> 'EdgeDeviceEventFromDimension':
		"""Builds a new EdgeDeviceEventFromDimension instance.
		
		Arguments:
			event {int} -- event code of the device

		Returns:
			EdgeDeviceEventFromDimension -- EdgeDeviceEventFromDimension
											instance
		"""
		return EdgeDeviceEventFromDimension(self, event, self.portia_config)

	def select(self, last: bool=False, params: dict=None) -> object:
		"""Retrieves a device's series by its port and dimension code.

		Keyword Arguments:
			last {bool} -- if the last package should be returned or not
						   (default: {False})
			params {dict} -- params to send to the service (default: {None})

		Returns:
			object -- object with the device's dimensions
		"""
		return add_humanize_method(select.query_by_port_dimension(
			self.portia_config,
			self.edge_id,
			self.port,
			self.dimension,
			last,
			params
		))

	def events(self, last: bool=False, params: dict=None) -> object:
		"""Retrieves a device's events by its port and dimension code.

		Keyword Arguments:
			last {bool} -- if the last event should be returned or not
						   (default: {False})
			params {dict} -- params to send to the service (default: {None})

		Returns:
			object -- object with the device's events
		"""
		return add_humanize_method(events.query_by_port_dimension(
			self.portia_config,
			self.edge_id,
			self.port,
			self.dimension,
			last,
			params
		))


class EdgeDeviceDimensionFromSensor(object):
	"""Abstracts usage of all Portia endpoints concerning data that only need
	an Edge ID, a port, a sensor and a dimension code.
	"""
	def __init__(
		self,
		edge_device_sensor: EdgeDeviceSensor,
		dimension: int,
		portia_config: dict
	):
		"""EdgeDeviceDimensionFromSensor's constructor.
		
		Arguments:
			edge_device_sensor {EdgeDeviceSensor} -- instance of an Edge device
					 								 sensor
			dimension {int} -- dimension code of the device
			portia_config {dict} -- Portia's configuration arguments
		"""
		self.edge_id = edge_device_sensor.edge_id
		self.port = edge_device_sensor.port
		self.sensor = edge_device_sensor.sensor
		self.dimension = dimension
		self.portia_config = portia_config

	def event(self, event: int) -> 'EdgeDeviceEventFromSensorDimension':
		"""Builds a new EdgeDeviceEventFromSensorDimension instance.
		
		Arguments:
			event {int} -- event code of the device

		Returns:
			EdgeDeviceEventFromSensorDimension -- 
				EdgeDeviceEventFromSensorDimension instance
		"""
		return EdgeDeviceEventFromSensorDimension(
			self, event, self.portia_config
		)

	def select(self, last: bool=False, params: dict=None) -> object:
		"""Retrieves a device's series by its port, sensor and dimension code.

		Keyword Arguments:
			last {bool} -- if the last package should be returned or not
						   (default: {False})
			params {dict} -- params to send to the service (default: {None})

		Returns:
			object -- object with the device's dimensions
		"""
		return add_humanize_method(select.query_by_port_sensor_dimension(
			self.portia_config,
			self.edge_id,
			self.port,
			self.sensor,
			self.dimension,
			last,
			params
		))

	def summary(
		self,
		strategy: 'SummaryStrategies'=summary.SummaryStrategies.PER_HOUR,
		interval=1,
		params=None
	) -> object:
		"""Summarizes a device by port, sensor and dimension code.

		Keyword Arguments:
			strategy {SummaryStrategies} -- strategy to use when summarizing
											(default:
											{SummaryStrategies.PER_HOUR})
			interval {int} -- interval of time to summarize (default: {1})
			params {dict} -- params to send to the service (default: {None})

		Returns:
			object -- object with the device's summarized dimensions
		"""
		return add_humanize_method(summary.query_by_port_sensor_dimension(
			self.portia_config,
			self.edge_id,
			self.port,
			self.sensor,
			self.dimension,
			strategy,
			interval,
			params
		))

	def events(self, last: bool=False, params: dict=None) -> object:
		"""Retrieves a device's events by its port, sensor and dimension code.

		Keyword Arguments:
			last {bool} -- if the last event should be returned or not
						   (default: {False})
			params {dict} -- params to send to the service (default: {None})

		Returns:
			object -- object with the device's events
		"""
		return add_humanize_method(events.query_by_port_sensor_dimension(
			self.portia_config,
			self.edge_id,
			self.port,
			self.sensor,
			self.dimension,
			last,
			params
		))


class EdgeDeviceEventFromSensor(object):
	"""Abstracts usage of all Portia endpoints concerning data that only need
	an Edge ID, a port a sensor and an event code.
	"""
	def __init__(
		self,
		edge_device_sensor: EdgeDeviceSensor,
		event: int,
		portia_config: dict
	):
		"""EdgeDeviceEventFromSensor's constructor.
		
		Arguments:
			edge_device_sensor {EdgeDeviceSensor} -- instance of an Edge device
												 	 sensor
			event {int} -- event code of the device
			portia_config {dict} -- Portia's configuration arguments
		"""
		self.edge_id = edge_device_sensor.edge_id
		self.port = edge_device_sensor.port
		self.sensor = edge_device_sensor.sensor
		self.event = event
		self.portia_config = portia_config

	def events(self, last: bool=False, params: dict=None) -> object:
		"""Retrieves a device's events by its port, sensor and event code.

		Keyword Arguments:
			last {bool} -- if the last event should be returned or not
						   (default: {False})
			params {dict} -- params to send to the service (default: {None})

		Returns:
			object -- object with the device's events
		"""
		return add_humanize_method(events.query_by_port_sensor_event(
			self.portia_config,
			self.edge_id,
			self.port,
			self.sensor,
			self.event,
			last,
			params
		))


class EdgeDeviceEventFromDimension(object):
	"""Abstracts usage of all Portia endpoints concerning data that only need
	an Edge ID, a port a dimension code and an event code.
	"""
	def __init__(
		self,
		edge_device_dimension_from_port: EdgeDeviceDimensionFromPort,
		event: int,
		portia_config: dict
	):
		"""EdgeDeviceEventFromDimension's constructor.
		
		Arguments:
			edge_device_dimension_from_port {EdgeDeviceDimensionFromPort} -- 
				instance of an Edge device dimension from port
			event {int} -- event code of the device
			portia_config {dict} -- Portia's configuration arguments
		"""
		self.edge_id = edge_device_dimension_from_port.edge_id
		self.port = edge_device_dimension_from_port.port
		self.dimension = edge_device_dimension_from_port.dimension
		self.event = event
		self.portia_config = portia_config

	def events(self, last: bool=False, params: dict=None) -> object:
		"""Retrieves a device's events by its port, dimension code and event
		code.

		Keyword Arguments:
			last {bool} -- if the last event should be returned or not
						   (default: {False})
			params {dict} -- params to send to the service (default: {None})

		Returns:
			object -- object with the device's events
		"""
		return add_humanize_method(events.query_by_port_dimension_event(
			self.portia_config,
			self.edge_id,
			self.port,
			self.dimension,
			self.event,
			last,
			params
		))


class EdgeDeviceEventFromSensorDimension(object):
	"""Abstracts usage of all Portia endpoints concerning data that only need
	an Edge ID, a port, sensor, dimension code and an event code.
	"""
	def __init__(
		self,
		edge_device_dimension_from_sensor: EdgeDeviceDimensionFromSensor,
		event: int,
		portia_config: dict
	):
		"""EdgeDeviceEventFromDimension's constructor.
		
		Arguments:
			edge_device_dimension_from_sensor {EdgeDeviceDimensionFromSensor}
				-- instance of an Edge device dimension from sensor
			event {int} -- event code of the device
			portia_config {dict} -- Portia's configuration arguments
		"""
		self.edge_id = edge_device_dimension_from_sensor.edge_id
		self.port = edge_device_dimension_from_sensor.port
		self.sensor = edge_device_dimension_from_sensor.sensor
		self.dimension = edge_device_dimension_from_sensor.dimension
		self.event = event
		self.portia_config = portia_config

	def events(self, last: bool=False, params: dict=None) -> object:
		"""Retrieves a device's events by its port, sensor, dimension code and
		event code.

		Keyword Arguments:
			last {bool} -- if the last event should be returned or not
						   (default: {False})
			params {dict} -- params to send to the service (default: {None})

		Returns:
			object -- object with the device's events
		"""
		return add_humanize_method(events.query_by_port_sensor_dimension_event(
			self.portia_config,
			self.edge_id,
			self.port,
			self.sensor,
			self.dimension,
			self.event,
			last,
			params
		))
