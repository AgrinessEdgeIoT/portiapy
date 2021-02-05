"""Integration testing for the application's profile module.
"""

import os
import unittest

from portiapy import profile


from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


class TestProfile(unittest.TestCase):
	"""Set of integration tests for all functions concerning the profile
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

	def test_profile_strategies(self):
		by_zero_port = profile.ProfileStrategies.BY_ZERO_PORT
		by_ports = profile.ProfileStrategies.BY_PORTS
		
		self.assertEqual(by_zero_port.endpoint, 'byzeroport')
		self.assertEqual(by_ports.endpoint, 'byports')

	def test_device_profile(self):
		device = profile.device_profile(self.portia_config, '2DPEQ572HEXP')

		self.assertEqual(device.get('device'), '2DPEQ572HEXP')
		self.assertEqual(device.get('channel_id'), '1BTU7542G5EY')
		self.assertEqual(device.get('channel_code'), 14)
		self.assertEqual(device.get('thing_code'), 69)
		self.assertEqual(len(device.get('ports')), 9)

	def test_port_profile(self):
		port = profile.port_profile(self.portia_config, '2DPEQ572HEXP', 4)

		self.assertEqual(port.get('device'), '2DPEQ572HEXP')
		self.assertEqual(port.get('channel_id'), '1BTU7542G5EY')
		self.assertEqual(port.get('channel_code'), 14)
		self.assertEqual(port.get('thing_code'), 69)
		self.assertEqual(len(port.get('ports')), 1)
		self.assertEqual(len(port.get('ports')[0].get('sensors')), 2)

	def test_sensor_profile(self):
		sensor = profile.sensor_profile(
			self.portia_config, '2DPEQ572HEXP', 4, 1
		)

		self.assertEqual(sensor.get('device'), '2DPEQ572HEXP')
		self.assertEqual(sensor.get('channel_id'), '1BTU7542G5EY')
		self.assertEqual(sensor.get('channel_code'), 14)
		self.assertEqual(sensor.get('thing_code'), 69)
		self.assertEqual(len(sensor.get('ports')), 1)
		self.assertEqual(len(sensor.get('ports')[0].get('sensors')), 1)


if __name__ == '__main__':
	unittest.main()
