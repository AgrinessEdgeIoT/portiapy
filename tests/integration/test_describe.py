"""Integration testing for the application's describe module.
"""

import os
import unittest

import pandas as pd

from portiapy import describe


from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


class TestDescribe(unittest.TestCase):
	"""Set of integration tests for all functions concerning the describe
	module.
	"""
	@classmethod
	def setUpClass(cls):
		"""Creates a Portia configuration to test the adapter.
		"""

		# Settings for test
		base_url = os.getenv('PORTIA_URL', 'https://api-portia.agriness.io/v3')
		token = os.getenv('PORTIA_TOKEN')

		# Creating portia configuration
		cls.portia_config = {
			'baseurl': base_url,
			'authorization': token,
			'debug': False,
			'Accept': 'text/csv'
		}

	def test_device_ports(self):
		ports = describe.device_ports(self.portia_config, '2DPEQ572HEXP')
		self.assertListEqual(ports, [0, 1, 2, 4, 5, 8, 9, 10, 11, 12, 13])

	def test_device_ports_last(self):
		ports = describe.device_ports(
			self.portia_config, '2DPEQ572HEXP', last=True
		)

		self.assertListEqual(
			ports['port'].tolist(), [0, 1, 2, 4, 5, 8, 9, 10, 11, 12, 13]
		)

		self.assertListEqual(
			ports['dimension_thing_code'].tolist(),
			[69, 15, 15, 16, 16, 22, 22, 22, 23, 68, 68]
		)

	def test_device_port_sensors(self):
		sensors = describe.device_port_sensors(
			self.portia_config, '2DPEQ572HEXP', 1
		)

		self.assertListEqual(sensors, [1])

	def test_device_port_sensors_last(self):
		sensors = describe.device_port_sensors(
			self.portia_config, '2DPEQ572HEXP', 1, last=True
		)

		self.assertEqual(sensors.iloc[0]['sensor'], 1)
		self.assertEqual(sensors.iloc[0]['dimension_code'], 1)
		self.assertEqual(sensors.iloc[0]['dimension_unity_code'], 1)
		self.assertEqual(sensors.iloc[0]['dimension_thing_code'], 15)

	def test_device_port_dimensions(self):
		dimensions = describe.device_port_dimensions(
			self.portia_config, '2DPEQ572HEXP', 1
		)

		self.assertListEqual(dimensions, [1, 9])

	def test_device_port_dimensions_last(self):
		dimensions = describe.device_port_dimensions(
			self.portia_config, '2DPEQ572HEXP', 1, last=True
		)

		self.assertEqual(dimensions.iloc[0]['sensor'], 1)
		self.assertEqual(dimensions.iloc[0]['dimension_code'], 1)
		self.assertEqual(dimensions.iloc[0]['dimension_thing_code'], 15)

		self.assertEqual(dimensions.iloc[1]['sensor'], 1)
		self.assertEqual(dimensions.iloc[1]['dimension_code'], 9)
		self.assertEqual(dimensions.iloc[1]['dimension_thing_code'], 15)

	def test_device_port_sensor_dimensions(self):
		dimensions = describe.device_port_sensor_dimensions(
			self.portia_config, '2DPEQ572HEXP', 1, 1
		)

		self.assertListEqual(dimensions, [1, 9])

	def test_device_port_sensor_dimensions_last(self):
		dimensions = describe.device_port_sensor_dimensions(
			self.portia_config, '2DPEQ572HEXP', 1, 1, last=True
		)

		self.assertEqual(dimensions.iloc[0]['dimension_code'], 1)
		self.assertEqual(dimensions.iloc[0]['dimension_unity_code'], 1)
		self.assertEqual(dimensions.iloc[0]['dimension_thing_code'], 15)

		self.assertEqual(dimensions.iloc[1]['dimension_code'], 9)
		self.assertEqual(dimensions.iloc[1]['dimension_unity_code'], 1)
		self.assertEqual(dimensions.iloc[1]['dimension_thing_code'], 15)


if __name__ == '__main__':
	unittest.main()
