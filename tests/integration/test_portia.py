"""Integration testing for the application's portia module.
"""

import os
import unittest

from portiapy import portia


from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


class TestEdgeDevice(unittest.TestCase):
	"""Set of integration tests for all functions concerning the EdgeDevice
	instance.
	"""
	@classmethod
	def setUpClass(cls):
		"""Creates a Portia configuration to test the instance.
		"""

		# Settings for test
		base_url = os.getenv('PORTIA_URL', 'https://api-portia.agriness.io/v3')
		token = os.getenv('PORTIA_TOKEN')

		# Creating Portia API instance
		cls.portia_api = portia.PortiaApi({
			'baseurl': base_url,
			'authorization': token,
			'debug': False,
			'Accept': 'text/csv'
		})

	def test_ports(self):
		ports = self.portia_api.device('2DPEQ572HEXP').ports(params={
	        'from': None,
	        'to': None,
	        'sort': True,
	        'precision': 'ms',
	        'timezone': 'Etc/UTC'
		})
		self.assertListEqual(ports, [0, 1, 2, 4, 5, 8, 9, 10, 11, 12, 13])

	def test_ports_last(self):
		ports = self.portia_api.device('2DPEQ572HEXP').ports(
			last=True,
			params={
		        'from': None,
		        'to': None,
		        'sort': True,
		        'precision': 'ms',
		        'timezone': 'Etc/UTC'
			}
		)

		self.assertListEqual(
			ports['port'].tolist(), [0, 1, 2, 4, 5, 8, 9, 10, 11, 12, 13]
		)

		self.assertListEqual(
			ports['dimension_thing_code'].tolist(),
			[69, 15, 15, 16, 16, 22, 22, 22, 23, 68, 68]
		)

	def test_profile(self):
		device = self.portia_api.device('2DPEQ572HEXP').profile(params={
			'sort': True,
			'precision': 'ms',
			'timezone': 'Etc/UTC'
		})

		self.assertEqual(device.get('device'), '2DPEQ572HEXP')
		self.assertEqual(device.get('channel_id'), '1BTU7542G5EY')
		self.assertEqual(device.get('channel_code'), 14)
		self.assertEqual(device.get('thing_code'), 69)
		self.assertEqual(len(device.get('ports')), 9)


class TestEdgeDevicePort(unittest.TestCase):
	"""Set of integration tests for all functions concerning the EdgeDevicePort
	instance.
	"""
	@classmethod
	def setUpClass(cls):
		"""Creates a Portia configuration to test the instance.
		"""

		# Settings for test
		base_url = os.getenv('PORTIA_URL', 'https://api-portia.agriness.io/v3')
		token = os.getenv('PORTIA_TOKEN')

		# Creating Portia API instance
		cls.portia_api = portia.PortiaApi({
			'baseurl': base_url,
			'authorization': token,
			'debug': False,
			'Accept': 'text/csv'
		})

	def test_sensors(self):
		sensors = self.portia_api.device('2DPEQ572HEXP').port(1).sensors(
			params={
		        'from': None,
		        'to': None,
		        'sort': True,
		        'precision': 'ms',
		        'timezone': 'Etc/UTC'
			}
		)
		self.assertListEqual(sensors, [1])

	def test_sensors_last(self):
		sensors = self.portia_api.device('2DPEQ572HEXP').port(1).sensors(
			last=True,
			params={
		        'from': None,
		        'to': None,
		        'sort': True,
		        'precision': 'ms',
		        'timezone': 'Etc/UTC'
			}
		)

		self.assertEqual(sensors.iloc[0]['sensor'], 1)
		self.assertEqual(sensors.iloc[0]['dimension_code'], 1)
		self.assertEqual(sensors.iloc[0]['dimension_unity_code'], 1)
		self.assertEqual(sensors.iloc[0]['dimension_thing_code'], 15)

		humanized_sensors = sensors.humanize()
		self.assertEqual(humanized_sensors.iloc[0]['sensor'], 1)
		self.assertEqual(
			humanized_sensors.iloc[0]['dimension_code'], 1
		)
		self.assertEqual(
			humanized_sensors.iloc[0]['dimension'], 'Point Temperature'
		)
		self.assertEqual(
			humanized_sensors.iloc[0]['dimension_unity_code'], 1
		)
		self.assertEqual(
			humanized_sensors.iloc[0]['dimension_unity'], '°C'
		)
		self.assertEqual(
			humanized_sensors.iloc[0]['dimension_thing_code'], 15
		)
		self.assertEqual(
			humanized_sensors.iloc[0]['dimension_thing'], 'Sensor_Inobram_T'
		)

	def test_dimensions(self):
		dimensions = self.portia_api.device('2DPEQ572HEXP').port(1).dimensions(
			params={
		        'from': None,
		        'to': None,
		        'sort': True,
		        'precision': 'ms',
		        'timezone': 'Etc/UTC'
			}
		)
		self.assertListEqual(dimensions, [1, 9])

	def test_dimensions_last(self):
		dimensions = self.portia_api.device('2DPEQ572HEXP').port(1).dimensions(
			last=True,
			params={
		        'from': None,
		        'to': None,
		        'sort': True,
		        'precision': 'ms',
		        'timezone': 'Etc/UTC'
			}
		)

		self.assertEqual(dimensions.iloc[0]['sensor'], 1)
		self.assertEqual(dimensions.iloc[0]['dimension_code'], 1)
		self.assertEqual(dimensions.iloc[0]['dimension_thing_code'], 15)

		self.assertEqual(dimensions.iloc[1]['sensor'], 1)
		self.assertEqual(dimensions.iloc[1]['dimension_code'], 9)
		self.assertEqual(dimensions.iloc[1]['dimension_thing_code'], 15)

		humanized_dimensions = dimensions.humanize()
		self.assertEqual(humanized_dimensions.iloc[0]['sensor'], 1)
		self.assertEqual(
			humanized_dimensions.iloc[0]['dimension_code'], 1
		)
		self.assertEqual(
			humanized_dimensions.iloc[0]['dimension'], 'Point Temperature'
		)
		self.assertEqual(
			humanized_dimensions.iloc[0]['dimension_thing_code'], 15
		)
		self.assertEqual(
			humanized_dimensions.iloc[0]['dimension_thing'], 'Sensor_Inobram_T'
		)

		self.assertEqual(humanized_dimensions.iloc[1]['sensor'], 1)
		self.assertEqual(
			humanized_dimensions.iloc[1]['dimension_code'], 9
		)
		self.assertEqual(
			humanized_dimensions.iloc[1]['dimension'],
			'Point Water Temperature'
		)
		self.assertEqual(
			humanized_dimensions.iloc[1]['dimension_thing_code'], 15
		)
		self.assertEqual(
			humanized_dimensions.iloc[1]['dimension_thing'], 'Sensor_Inobram_T'
		)

	def test_profile(self):
		port = self.portia_api.device('2DPEQ572HEXP').port(4).profile(params={
			'sort': True,
			'precision': 'ms',
			'timezone': 'Etc/UTC'
		})

		self.assertEqual(port.get('device'), '2DPEQ572HEXP')
		self.assertEqual(port.get('channel_id'), '1BTU7542G5EY')
		self.assertEqual(port.get('channel_code'), 14)
		self.assertEqual(port.get('thing_code'), 69)
		self.assertEqual(len(port.get('ports')), 1)
		self.assertEqual(len(port.get('ports')[0].get('sensors')), 2)


class TestEdgeDeviceSensor(unittest.TestCase):
	"""Set of integration tests for all functions concerning the
	EdgeDeviceSensor instance.
	"""
	@classmethod
	def setUpClass(cls):
		"""Creates a Portia configuration to test the instance.
		"""

		# Settings for test
		base_url = os.getenv('PORTIA_URL', 'https://api-portia.agriness.io/v3')
		token = os.getenv('PORTIA_TOKEN')

		# Creating Portia API instance
		cls.portia_api = portia.PortiaApi({
			'baseurl': base_url,
			'authorization': token,
			'debug': False,
			'Accept': 'text/csv'
		})

	def test_dimensions(self):
		dimensions = self.portia_api.device('2DPEQ572HEXP').port(1).sensor(1) \
			.dimensions(
				params={
			        'from': None,
			        'to': None,
			        'sort': True,
			        'precision': 'ms',
			        'timezone': 'Etc/UTC'
				}
			)
		self.assertListEqual(dimensions, [1, 9])

	def test_dimensions_last(self):
		dimensions = self.portia_api.device('2DPEQ572HEXP').port(1).sensor(1) \
			.dimensions(
				last=True,
				params={
			        'from': None,
			        'to': None,
			        'sort': True,
			        'precision': 'ms',
			        'timezone': 'Etc/UTC'
				}
			)

		self.assertEqual(dimensions.iloc[0]['dimension_code'], 1)
		self.assertEqual(dimensions.iloc[0]['dimension_unity_code'], 1)
		self.assertEqual(dimensions.iloc[0]['dimension_thing_code'], 15)

		self.assertEqual(dimensions.iloc[1]['dimension_code'], 9)
		self.assertEqual(dimensions.iloc[1]['dimension_unity_code'], 1)
		self.assertEqual(dimensions.iloc[1]['dimension_thing_code'], 15)

		humanized_dimensions = dimensions.humanize()
		self.assertEqual(
			humanized_dimensions.iloc[0]['dimension_code'], 1
		)
		self.assertEqual(
			humanized_dimensions.iloc[0]['dimension'], 'Point Temperature'
		)
		self.assertEqual(
			humanized_dimensions.iloc[0]['dimension_unity_code'], 1
		)
		self.assertEqual(
			humanized_dimensions.iloc[0]['dimension_unity'], '°C'
		)
		self.assertEqual(
			humanized_dimensions.iloc[0]['dimension_thing_code'], 15
		)
		self.assertEqual(
			humanized_dimensions.iloc[0]['dimension_thing'], 'Sensor_Inobram_T'
		)

		self.assertEqual(
			humanized_dimensions.iloc[1]['dimension_code'], 9
		)
		self.assertEqual(
			humanized_dimensions.iloc[1]['dimension'],
			'Point Water Temperature'
		)
		self.assertEqual(
			humanized_dimensions.iloc[1]['dimension_unity_code'], 1
		)
		self.assertEqual(
			humanized_dimensions.iloc[1]['dimension_unity'], '°C'
		)
		self.assertEqual(
			humanized_dimensions.iloc[1]['dimension_thing_code'], 15
		)
		self.assertEqual(
			humanized_dimensions.iloc[1]['dimension_thing'], 'Sensor_Inobram_T'
		)

	def test_profile(self):
		sensor = self.portia_api.device('2DPEQ572HEXP').port(4).sensor(1). \
			profile(params={
				'sort': True,
				'precision': 'ms',
				'timezone': 'Etc/UTC'
			})

		self.assertEqual(sensor.get('device'), '2DPEQ572HEXP')
		self.assertEqual(sensor.get('channel_id'), '1BTU7542G5EY')
		self.assertEqual(sensor.get('channel_code'), 14)
		self.assertEqual(sensor.get('thing_code'), 69)
		self.assertEqual(len(sensor.get('ports')), 1)
		self.assertEqual(len(sensor.get('ports')[0].get('sensors')), 1)

	def test_select(self):
		dimensions = self.portia_api.device('2DPEQ572HEXP').port(4) \
			.sensor(1).select(params={
		        'from': 1609470000000,
		        'to': 1609729199000,
		        'lower_bound': None,
		        'upper_bound': None,
		        'order': None,
		        'limit': None,
		        'precision': 'ms',
		        'timezone': 'Etc/UTC'
		    })

		for i, row in dimensions.iterrows():
			self.assertEqual(row.dimension_thing_code, 16)
			self.assertEqual(row.dimension_unity_code, 1)
			self.assertEqual(row.dimension_code, 1)

		for i, row in dimensions.humanize().iterrows():
			self.assertEqual(row.dimension_thing_code, 16)
			self.assertEqual(row.dimension_thing, 'Sensor_Inobram_TU')
			self.assertEqual(row.dimension_unity_code, 1)
			self.assertEqual(row.dimension_unity, '°C')
			self.assertEqual(row.dimension_code, 1)
			self.assertEqual(row.dimension, 'Point Temperature')

	def test_select_last(self):
		dimensions = self.portia_api.device('2DPEQ572HEXP').port(4) \
			.sensor(1).select(
				last=True,
				params={
			        'from': 1609470000000,
			        'to': 1609729199000,
			        'lower_bound': None,
			        'upper_bound': None,
			        'order': None,
			        'limit': None,
			        'precision': 'ms',
			        'timezone': 'Etc/UTC'
			    }
			)

		self.assertEqual(dimensions.iloc[0].dimension_thing_code, 16)
		self.assertEqual(dimensions.iloc[0].dimension_unity_code, 1)
		self.assertEqual(dimensions.iloc[0].dimension_code, 1)

		humanized_dimensions = dimensions.humanize()
		self.assertEqual(
			humanized_dimensions.iloc[0].dimension_thing_code, 16
		)
		self.assertEqual(
			humanized_dimensions.iloc[0].dimension_thing, 'Sensor_Inobram_TU'
		)
		self.assertEqual(
			humanized_dimensions.iloc[0].dimension_unity_code, 1
		)
		self.assertEqual(
			humanized_dimensions.iloc[0].dimension_unity, '°C'
		)
		self.assertEqual(
			humanized_dimensions.iloc[0].dimension_code, 1
		)
		self.assertEqual(
			humanized_dimensions.iloc[0].dimension, 'Point Temperature'
		)

	def test_summary(self):
		summarized_dimensions = self.portia_api.device('2DPEQ572HEXP') \
			.port(4).sensor(1).summary(params={
		        'from': 1609470000000,
		        'to': 1609729199000,
		        'lower_bound': None,
		        'upper_bound': None,
		        'offset': 0,
		        'fill': None,
		        'order': None,
		        'limit': None,
		        'avg': True,
		        'min': True,
		        'max': True,
		        'sum': False,
		        'median': False,
		        'mode': False,
		        'stddev': False,
		        'spread': False,
		        'last_timestamp': False,
		        'precision': 'ms',
		        'timezone': 'Etc/UTC'
		    })

		for i, row in summarized_dimensions.iterrows():
			self.assertEqual(row.dimension_unity_code, 1)

		for i, row in summarized_dimensions.humanize().iterrows():
			self.assertEqual(row.dimension_unity_code, 1)
			self.assertEqual(row.dimension_unity, '°C')

	def test_events(self):
		events = self.portia_api.device('2DPEQ572HEXP').port(4) \
			.sensor(1).events(params={
		        'from': 1609470000000,
		        'to': 1609729199000,
		        'order': None,
		        'limit': None,
		        'precision': 'ms',
		        'timezone': 'Etc/UTC'
		    })

		for i, row in events.iterrows():
			self.assertEqual(row.dimension_thing_code, 16)
			self.assertEqual(row.dimension_unity_code, 1)
			self.assertEqual(row.dimension_code, 1)
			self.assertEqual(row.event_code, 1)

		for i, row in events.humanize().iterrows():
			self.assertEqual(row.dimension_thing_code, 16)
			self.assertEqual(row.dimension_thing, 'Sensor_Inobram_TU')
			self.assertEqual(row.dimension_unity_code, 1)
			self.assertEqual(row.dimension_unity, '°C')
			self.assertEqual(row.dimension_code, 1)
			self.assertEqual(row.dimension, 'Point Temperature')
			self.assertEqual(row.event_code, 1)
			self.assertEqual(row.event, 'Communication State')

	def test_events_last(self):
		events = self.portia_api.device('2DPEQ572HEXP').port(4) \
			.sensor(1).events(
				last=True,
				params={
			        'from': 1609470000000,
			        'to': 1609729199000,
			        'order': None,
			        'limit': None,
			        'precision': 'ms',
			        'timezone': 'Etc/UTC'
			    }
			)

		self.assertEqual(events.iloc[0].dimension_thing_code, 16)
		self.assertEqual(events.iloc[0].dimension_unity_code, 1)
		self.assertEqual(events.iloc[0].dimension_code, 1)
		self.assertEqual(events.iloc[0].event_code, 1)

		humanized_events = events.humanize()
		self.assertEqual(
			humanized_events.iloc[0].dimension_thing_code, 16
		)
		self.assertEqual(
			humanized_events.iloc[0].dimension_thing, 'Sensor_Inobram_TU'
		)
		self.assertEqual(
			humanized_events.iloc[0].dimension_unity_code, 1
		)
		self.assertEqual(
			humanized_events.iloc[0].dimension_unity, '°C'
		)
		self.assertEqual(
			humanized_events.iloc[0].dimension_code, 1
		)
		self.assertEqual(
			humanized_events.iloc[0].dimension, 'Point Temperature'
		)
		self.assertEqual(
			humanized_events.iloc[0].event_code, 1
		)
		self.assertEqual(
			humanized_events.iloc[0].event, 'Communication State'
		)


class TestEdgeDeviceDimensionFromDevice(unittest.TestCase):
	"""Set of integration tests for all functions concerning the
	EdgeDeviceDimensionFromDevice instance.
	"""
	@classmethod
	def setUpClass(cls):
		"""Creates a Portia configuration to test the instance.
		"""

		# Settings for test
		base_url = os.getenv('PORTIA_URL', 'https://api-portia.agriness.io/v3')
		token = os.getenv('PORTIA_TOKEN')

		# Creating Portia API instance
		cls.portia_api = portia.PortiaApi({
			'baseurl': base_url,
			'authorization': token,
			'debug': False,
			'Accept': 'text/csv'
		})

	def test_summary(self):
		summarized_dimensions = self.portia_api.device('2DPEQ572HEXP') \
			.dimension(1).summary(None, params={
		        'from': 1609470000000,
		        'to': 1609729199000,
		        'lower_bound': None,
		        'upper_bound': None,
		        'offset': 0,
		        'fill': None,
		        'order': None,
		        'limit': None,
		        'avg': True,
		        'min': True,
		        'max': True,
		        'sum': False,
		        'median': False,
		        'mode': False,
		        'stddev': False,
		        'spread': False,
		        'last_timestamp': False,
		        'precision': 'ms',
		        'timezone': 'Etc/UTC'
		    })

		for i, row in summarized_dimensions.iterrows():
			self.assertEqual(row.dimension_unity_code, 1)

		for i, row in summarized_dimensions.humanize().iterrows():
			self.assertEqual(row.dimension_unity_code, 1)
			self.assertEqual(row.dimension_unity, '°C')



class TestEdgeDeviceDimensionFromPort(unittest.TestCase):
	"""Set of integration tests for all functions concerning the
	EdgeDeviceDimensionFromPort instance.
	"""
	@classmethod
	def setUpClass(cls):
		"""Creates a Portia configuration to test the instance.
		"""

		# Settings for test
		base_url = os.getenv('PORTIA_URL', 'https://api-portia.agriness.io/v3')
		token = os.getenv('PORTIA_TOKEN')

		# Creating Portia API instance
		cls.portia_api = portia.PortiaApi({
			'baseurl': base_url,
			'authorization': token,
			'debug': False,
			'Accept': 'text/csv'
		})

	def test_select(self):
		dimensions = self.portia_api.device('2DPEQ572HEXP').port(4) \
			.dimension(1).select(params={
		        'from': 1609470000000,
		        'to': 1609729199000,
		        'lower_bound': None,
		        'upper_bound': None,
		        'order': None,
		        'limit': None,
		        'precision': 'ms',
		        'timezone': 'Etc/UTC'
		    })

		for i, row in dimensions.iterrows():
			self.assertEqual(row.dimension_thing_code, 16)
			self.assertEqual(row.dimension_unity_code, 1)
			self.assertEqual(row.dimension_code, 1)

		for i, row in dimensions.humanize().iterrows():
			self.assertEqual(row.dimension_thing_code, 16)
			self.assertEqual(row.dimension_thing, 'Sensor_Inobram_TU')
			self.assertEqual(row.dimension_unity_code, 1)
			self.assertEqual(row.dimension_unity, '°C')
			self.assertEqual(row.dimension_code, 1)
			self.assertEqual(row.dimension, 'Point Temperature')

	def test_select_last(self):
		dimensions = self.portia_api.device('2DPEQ572HEXP').port(4) \
			.dimension(1).select(
				last=True,
				params={
			        'from': 1609470000000,
			        'to': 1609729199000,
			        'lower_bound': None,
			        'upper_bound': None,
			        'order': None,
			        'limit': None,
			        'precision': 'ms',
			        'timezone': 'Etc/UTC'
			    }
			)

		self.assertEqual(dimensions.iloc[0].dimension_thing_code, 16)
		self.assertEqual(dimensions.iloc[0].dimension_unity_code, 1)
		self.assertEqual(dimensions.iloc[0].dimension_code, 1)

		humanized_dimensions = dimensions.humanize()
		self.assertEqual(
			humanized_dimensions.iloc[0].dimension_thing_code, 16
		)
		self.assertEqual(
			humanized_dimensions.iloc[0].dimension_thing, 'Sensor_Inobram_TU'
		)
		self.assertEqual(
			humanized_dimensions.iloc[0].dimension_unity_code, 1
		)
		self.assertEqual(
			humanized_dimensions.iloc[0].dimension_unity, '°C'
		)
		self.assertEqual(
			humanized_dimensions.iloc[0].dimension_code, 1
		)
		self.assertEqual(
			humanized_dimensions.iloc[0].dimension, 'Point Temperature'
		)

	def test_events(self):
		events = self.portia_api.device('2DPEQ572HEXP').port(4) \
			.dimension(1).events(params={
		        'from': 1609470000000,
		        'to': 1609729199000,
		        'order': None,
		        'limit': None,
		        'precision': 'ms',
		        'timezone': 'Etc/UTC'
		    })

		for i, row in events.iterrows():
			self.assertEqual(row.dimension_thing_code, 16)
			self.assertEqual(row.dimension_unity_code, 1)
			self.assertEqual(row.dimension_code, 1)
			self.assertEqual(row.event_code, 1)

		for i, row in events.humanize().iterrows():
			self.assertEqual(row.dimension_thing_code, 16)
			self.assertEqual(row.dimension_thing, 'Sensor_Inobram_TU')
			self.assertEqual(row.dimension_unity_code, 1)
			self.assertEqual(row.dimension_unity, '°C')
			self.assertEqual(row.dimension_code, 1)
			self.assertEqual(row.dimension, 'Point Temperature')
			self.assertEqual(row.event_code, 1)
			self.assertEqual(row.event, 'Communication State')

	def test_events_last(self):
		events = self.portia_api.device('2DPEQ572HEXP').port(4) \
			.dimension(1).events(
				last=True,
				params={
			        'from': 1609470000000,
			        'to': 1609729199000,
			        'order': None,
			        'limit': None,
			        'precision': 'ms',
			        'timezone': 'Etc/UTC'
			    }
			)

		self.assertEqual(events.iloc[0].dimension_thing_code, 16)
		self.assertEqual(events.iloc[0].dimension_unity_code, 1)
		self.assertEqual(events.iloc[0].dimension_code, 1)
		self.assertEqual(events.iloc[0].event_code, 1)

		humanized_events = events.humanize()
		self.assertEqual(
			humanized_events.iloc[0].dimension_thing_code, 16
		)
		self.assertEqual(
			humanized_events.iloc[0].dimension_thing, 'Sensor_Inobram_TU'
		)
		self.assertEqual(
			humanized_events.iloc[0].dimension_unity_code, 1
		)
		self.assertEqual(
			humanized_events.iloc[0].dimension_unity, '°C'
		)
		self.assertEqual(
			humanized_events.iloc[0].dimension_code, 1
		)
		self.assertEqual(
			humanized_events.iloc[0].dimension, 'Point Temperature'
		)
		self.assertEqual(
			humanized_events.iloc[0].event_code, 1
		)
		self.assertEqual(
			humanized_events.iloc[0].event, 'Communication State'
		)


class TestEdgeDeviceDimensionFromSensor(unittest.TestCase):
	"""Set of integration tests for all functions concerning the
	EdgeDeviceDimensionFromSensor instance.
	"""
	@classmethod
	def setUpClass(cls):
		"""Creates a Portia configuration to test the instance.
		"""

		# Settings for test
		base_url = os.getenv('PORTIA_URL', 'https://api-portia.agriness.io/v3')
		token = os.getenv('PORTIA_TOKEN')

		# Creating Portia API instance
		cls.portia_api = portia.PortiaApi({
			'baseurl': base_url,
			'authorization': token,
			'debug': False,
			'Accept': 'text/csv'
		})

	def test_select(self):
		dimensions = self.portia_api.device('2DPEQ572HEXP').port(4).sensor(1) \
			.dimension(1).select(params={
		        'from': 1609470000000,
		        'to': 1609729199000,
		        'lower_bound': None,
		        'upper_bound': None,
		        'order': None,
		        'limit': None,
		        'precision': 'ms',
		        'timezone': 'Etc/UTC'
		    })

		for i, row in dimensions.iterrows():
			self.assertEqual(row.dimension_thing_code, 16)
			self.assertEqual(row.dimension_unity_code, 1)
			self.assertEqual(row.dimension_code, 1)

		for i, row in dimensions.humanize().iterrows():
			self.assertEqual(row.dimension_thing_code, 16)
			self.assertEqual(row.dimension_thing, 'Sensor_Inobram_TU')
			self.assertEqual(row.dimension_unity_code, 1)
			self.assertEqual(row.dimension_unity, '°C')
			self.assertEqual(row.dimension_code, 1)
			self.assertEqual(row.dimension, 'Point Temperature')

	def test_select_last(self):
		dimensions = self.portia_api.device('2DPEQ572HEXP').port(4).sensor(1) \
			.dimension(1).select(
				last=True,
				params={
			        'from': 1609470000000,
			        'to': 1609729199000,
			        'lower_bound': None,
			        'upper_bound': None,
			        'order': None,
			        'limit': None,
			        'precision': 'ms',
			        'timezone': 'Etc/UTC'
			    }
			)

		self.assertEqual(dimensions.iloc[0].dimension_thing_code, 16)
		self.assertEqual(dimensions.iloc[0].dimension_unity_code, 1)
		self.assertEqual(dimensions.iloc[0].dimension_code, 1)

		humanized_dimensions = dimensions.humanize()
		self.assertEqual(
			humanized_dimensions.iloc[0].dimension_thing_code, 16
		)
		self.assertEqual(
			humanized_dimensions.iloc[0].dimension_thing, 'Sensor_Inobram_TU'
		)
		self.assertEqual(
			humanized_dimensions.iloc[0].dimension_unity_code, 1
		)
		self.assertEqual(
			humanized_dimensions.iloc[0].dimension_unity, '°C'
		)
		self.assertEqual(
			humanized_dimensions.iloc[0].dimension_code, 1
		)
		self.assertEqual(
			humanized_dimensions.iloc[0].dimension, 'Point Temperature'
		)

	def test_summary(self):
		summarized_dimensions = self.portia_api.device('2DPEQ572HEXP') \
			.port(4).sensor(1).dimension(1).summary(params={
		        'from': 1609470000000,
		        'to': 1609729199000,
		        'lower_bound': None,
		        'upper_bound': None,
		        'offset': 0,
		        'fill': None,
		        'order': None,
		        'limit': None,
		        'avg': True,
		        'min': True,
		        'max': True,
		        'sum': False,
		        'median': False,
		        'mode': False,
		        'stddev': False,
		        'spread': False,
		        'last_timestamp': False,
		        'precision': 'ms',
		        'timezone': 'Etc/UTC'
		    })

		for i, row in summarized_dimensions.iterrows():
			self.assertEqual(row.dimension_unity_code, 1)

		for i, row in summarized_dimensions.humanize().iterrows():
			self.assertEqual(row.dimension_unity_code, 1)
			self.assertEqual(row.dimension_unity, '°C')

	def test_events(self):
		events = self.portia_api.device('2DPEQ572HEXP').port(4).sensor(1) \
			.dimension(1).events(params={
		        'from': 1609470000000,
		        'to': 1609729199000,
		        'order': None,
		        'limit': None,
		        'precision': 'ms',
		        'timezone': 'Etc/UTC'
		    })

		for i, row in events.iterrows():
			self.assertEqual(row.dimension_thing_code, 16)
			self.assertEqual(row.dimension_unity_code, 1)
			self.assertEqual(row.dimension_code, 1)
			self.assertEqual(row.event_code, 1)

		for i, row in events.humanize().iterrows():
			self.assertEqual(row.dimension_thing_code, 16)
			self.assertEqual(row.dimension_thing, 'Sensor_Inobram_TU')
			self.assertEqual(row.dimension_unity_code, 1)
			self.assertEqual(row.dimension_unity, '°C')
			self.assertEqual(row.dimension_code, 1)
			self.assertEqual(row.dimension, 'Point Temperature')
			self.assertEqual(row.event_code, 1)
			self.assertEqual(row.event, 'Communication State')

	def test_events_last(self):
		events = self.portia_api.device('2DPEQ572HEXP').port(4).sensor(1) \
			.dimension(1).events(
				last=True,
				params={
			        'from': 1609470000000,
			        'to': 1609729199000,
			        'order': None,
			        'limit': None,
			        'precision': 'ms',
			        'timezone': 'Etc/UTC'
			    }
			)

		self.assertEqual(events.iloc[0].dimension_thing_code, 16)
		self.assertEqual(events.iloc[0].dimension_unity_code, 1)
		self.assertEqual(events.iloc[0].dimension_code, 1)
		self.assertEqual(events.iloc[0].event_code, 1)

		humanized_events = events.humanize()
		self.assertEqual(
			humanized_events.iloc[0].dimension_thing_code, 16
		)
		self.assertEqual(
			humanized_events.iloc[0].dimension_thing, 'Sensor_Inobram_TU'
		)
		self.assertEqual(
			humanized_events.iloc[0].dimension_unity_code, 1
		)
		self.assertEqual(
			humanized_events.iloc[0].dimension_unity, '°C'
		)
		self.assertEqual(
			humanized_events.iloc[0].dimension_code, 1
		)
		self.assertEqual(
			humanized_events.iloc[0].dimension, 'Point Temperature'
		)
		self.assertEqual(
			humanized_events.iloc[0].event_code, 1
		)
		self.assertEqual(
			humanized_events.iloc[0].event, 'Communication State'
		)


class TestEdgeDeviceEventFromSensor(unittest.TestCase):
	"""Set of integration tests for all functions concerning the
	EdgeDeviceEventFromSensor instance.
	"""
	@classmethod
	def setUpClass(cls):
		"""Creates a Portia configuration to test the instance.
		"""

		# Settings for test
		base_url = os.getenv('PORTIA_URL', 'https://api-portia.agriness.io/v3')
		token = os.getenv('PORTIA_TOKEN')

		# Creating Portia API instance
		cls.portia_api = portia.PortiaApi({
			'baseurl': base_url,
			'authorization': token,
			'debug': False,
			'Accept': 'text/csv'
		})

	def test_events(self):
		events = self.portia_api.device('2DPEQ572HEXP').port(4).sensor(1) \
			.event(1).events(params={
		        'from': 1609470000000,
		        'to': 1609729199000,
		        'order': None,
		        'limit': None,
		        'precision': 'ms',
		        'timezone': 'Etc/UTC'
		    })

		for i, row in events.iterrows():
			self.assertEqual(row.dimension_thing_code, 16)
			self.assertEqual(row.dimension_unity_code, 1)
			self.assertEqual(row.dimension_code, 1)
			self.assertEqual(row.event_code, 1)

		for i, row in events.humanize().iterrows():
			self.assertEqual(row.dimension_thing_code, 16)
			self.assertEqual(row.dimension_thing, 'Sensor_Inobram_TU')
			self.assertEqual(row.dimension_unity_code, 1)
			self.assertEqual(row.dimension_unity, '°C')
			self.assertEqual(row.dimension_code, 1)
			self.assertEqual(row.dimension, 'Point Temperature')
			self.assertEqual(row.event_code, 1)
			self.assertEqual(row.event, 'Communication State')

	def test_events_last(self):
		events = self.portia_api.device('2DPEQ572HEXP').port(4).sensor(1) \
			.event(1).events(
				last=True,
				params={
			        'from': 1609470000000,
			        'to': 1609729199000,
			        'order': None,
			        'limit': None,
			        'precision': 'ms',
			        'timezone': 'Etc/UTC'
			    }
			)

		self.assertEqual(events.iloc[0].dimension_thing_code, 16)
		self.assertEqual(events.iloc[0].dimension_unity_code, 1)
		self.assertEqual(events.iloc[0].dimension_code, 1)
		self.assertEqual(events.iloc[0].event_code, 1)

		humanized_events = events.humanize()
		self.assertEqual(
			humanized_events.iloc[0].dimension_thing_code, 16
		)
		self.assertEqual(
			humanized_events.iloc[0].dimension_thing, 'Sensor_Inobram_TU'
		)
		self.assertEqual(
			humanized_events.iloc[0].dimension_unity_code, 1
		)
		self.assertEqual(
			humanized_events.iloc[0].dimension_unity, '°C'
		)
		self.assertEqual(
			humanized_events.iloc[0].dimension_code, 1
		)
		self.assertEqual(
			humanized_events.iloc[0].dimension, 'Point Temperature'
		)
		self.assertEqual(
			humanized_events.iloc[0].event_code, 1
		)
		self.assertEqual(
			humanized_events.iloc[0].event, 'Communication State'
		)


class TestEdgeDeviceEventFromDimension(unittest.TestCase):
	"""Set of integration tests for all functions concerning the
	EdgeDeviceEventFromDimension instance.
	"""
	@classmethod
	def setUpClass(cls):
		"""Creates a Portia configuration to test the instance.
		"""

		# Settings for test
		base_url = os.getenv('PORTIA_URL', 'https://api-portia.agriness.io/v3')
		token = os.getenv('PORTIA_TOKEN')

		# Creating Portia API instance
		cls.portia_api = portia.PortiaApi({
			'baseurl': base_url,
			'authorization': token,
			'debug': False,
			'Accept': 'text/csv'
		})

	def test_events(self):
		events = self.portia_api.device('2DPEQ572HEXP').port(4).dimension(1) \
			.event(1).events(params={
		        'from': 1609470000000,
		        'to': 1609729199000,
		        'order': None,
		        'limit': None,
		        'precision': 'ms',
		        'timezone': 'Etc/UTC'
		    })

		for i, row in events.iterrows():
			self.assertEqual(row.dimension_thing_code, 16)
			self.assertEqual(row.dimension_unity_code, 1)
			self.assertEqual(row.dimension_code, 1)
			self.assertEqual(row.event_code, 1)

		for i, row in events.humanize().iterrows():
			self.assertEqual(row.dimension_thing_code, 16)
			self.assertEqual(row.dimension_thing, 'Sensor_Inobram_TU')
			self.assertEqual(row.dimension_unity_code, 1)
			self.assertEqual(row.dimension_unity, '°C')
			self.assertEqual(row.dimension_code, 1)
			self.assertEqual(row.dimension, 'Point Temperature')
			self.assertEqual(row.event_code, 1)
			self.assertEqual(row.event, 'Communication State')

	def test_events_last(self):
		events = self.portia_api.device('2DPEQ572HEXP').port(4).dimension(1) \
			.event(1).events(
				last=True,
				params={
			        'from': 1609470000000,
			        'to': 1609729199000,
			        'order': None,
			        'limit': None,
			        'precision': 'ms',
			        'timezone': 'Etc/UTC'
			    }
			)

		self.assertEqual(events.iloc[0].dimension_thing_code, 16)
		self.assertEqual(events.iloc[0].dimension_unity_code, 1)
		self.assertEqual(events.iloc[0].dimension_code, 1)
		self.assertEqual(events.iloc[0].event_code, 1)

		humanized_events = events.humanize()
		self.assertEqual(
			humanized_events.iloc[0].dimension_thing_code, 16
		)
		self.assertEqual(
			humanized_events.iloc[0].dimension_thing, 'Sensor_Inobram_TU'
		)
		self.assertEqual(
			humanized_events.iloc[0].dimension_unity_code, 1
		)
		self.assertEqual(
			humanized_events.iloc[0].dimension_unity, '°C'
		)
		self.assertEqual(
			humanized_events.iloc[0].dimension_code, 1
		)
		self.assertEqual(
			humanized_events.iloc[0].dimension, 'Point Temperature'
		)
		self.assertEqual(
			humanized_events.iloc[0].event_code, 1
		)
		self.assertEqual(
			humanized_events.iloc[0].event, 'Communication State'
		)


class TestEdgeDeviceEventFromSensorDimension(unittest.TestCase):
	"""Set of integration tests for all functions concerning the
	EdgeDeviceEventFromSensorDimension instance.
	"""
	@classmethod
	def setUpClass(cls):
		"""Creates a Portia configuration to test the instance.
		"""

		# Settings for test
		base_url = os.getenv('PORTIA_URL', 'https://api-portia.agriness.io/v3')
		token = os.getenv('PORTIA_TOKEN')

		# Creating Portia API instance
		cls.portia_api = portia.PortiaApi({
			'baseurl': base_url,
			'authorization': token,
			'debug': False,
			'Accept': 'text/csv'
		})

	def test_events(self):
		events = self.portia_api.device('2DPEQ572HEXP').port(4).sensor(1) \
			.dimension(1).event(1).events(params={
		        'from': 1609470000000,
		        'to': 1609729199000,
		        'order': None,
		        'limit': None,
		        'precision': 'ms',
		        'timezone': 'Etc/UTC'
		    })

		for i, row in events.iterrows():
			self.assertEqual(row.dimension_thing_code, 16)
			self.assertEqual(row.dimension_unity_code, 1)
			self.assertEqual(row.dimension_code, 1)
			self.assertEqual(row.event_code, 1)

		for i, row in events.humanize().iterrows():
			self.assertEqual(row.dimension_thing_code, 16)
			self.assertEqual(row.dimension_thing, 'Sensor_Inobram_TU')
			self.assertEqual(row.dimension_unity_code, 1)
			self.assertEqual(row.dimension_unity, '°C')
			self.assertEqual(row.dimension_code, 1)
			self.assertEqual(row.dimension, 'Point Temperature')
			self.assertEqual(row.event_code, 1)
			self.assertEqual(row.event, 'Communication State')

	def test_events_last(self):
		events = self.portia_api.device('2DPEQ572HEXP').port(4).sensor(1) \
			.dimension(1).event(1).events(
				last=True,
				params={
			        'from': 1609470000000,
			        'to': 1609729199000,
			        'order': None,
			        'limit': None,
			        'precision': 'ms',
			        'timezone': 'Etc/UTC'
			    }
			)

		self.assertEqual(events.iloc[0].dimension_thing_code, 16)
		self.assertEqual(events.iloc[0].dimension_unity_code, 1)
		self.assertEqual(events.iloc[0].dimension_code, 1)
		self.assertEqual(events.iloc[0].event_code, 1)

		humanized_events = events.humanize()
		self.assertEqual(
			humanized_events.iloc[0].dimension_thing_code, 16
		)
		self.assertEqual(
			humanized_events.iloc[0].dimension_thing, 'Sensor_Inobram_TU'
		)
		self.assertEqual(
			humanized_events.iloc[0].dimension_unity_code, 1
		)
		self.assertEqual(
			humanized_events.iloc[0].dimension_unity, '°C'
		)
		self.assertEqual(
			humanized_events.iloc[0].dimension_code, 1
		)
		self.assertEqual(
			humanized_events.iloc[0].dimension, 'Point Temperature'
		)
		self.assertEqual(
			humanized_events.iloc[0].event_code, 1
		)
		self.assertEqual(
			humanized_events.iloc[0].event, 'Communication State'
		)


if __name__ == '__main__':
	unittest.main()
