"""Integration testing for the application's select module.
"""

import os
import unittest

from portiapy import events


from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


class TestEvents(unittest.TestCase):
	"""Set of integration tests for all functions concerning the events
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

	def test_query_by_port_sensor(self):
		device_events = events.query_by_port_sensor(
			self.portia_config, '2DPEQ572HEXP', 4, 1
		)

		for i, row in device_events.iterrows():
			self.assertEqual(row.dimension_thing_code, 16)
			self.assertEqual(row.dimension_unity_code, 1)
			self.assertEqual(row.dimension_code, 1)
			self.assertEqual(row.event_code, 1)

	def test_query_by_port_sensor_last(self):
		device_events = events.query_by_port_sensor(
			self.portia_config, '2DPEQ572HEXP', 4, 1, last=True
		)

		self.assertEqual(device_events.iloc[0].dimension_thing_code, 16)
		self.assertEqual(device_events.iloc[0].dimension_unity_code, 1)
		self.assertEqual(device_events.iloc[0].dimension_code, 1)
		self.assertEqual(device_events.iloc[0].event_code, 1)

	def test_query_by_port_dimension(self):
		device_events = events.query_by_port_dimension(
			self.portia_config, '2DPEQ572HEXP', 4, 1
		)

		for i, row in device_events.iterrows():
			self.assertEqual(row.dimension_thing_code, 16)
			self.assertEqual(row.dimension_unity_code, 1)
			self.assertEqual(row.dimension_code, 1)
			self.assertEqual(row.event_code, 1)

	def test_query_by_port_dimension_last(self):
		device_events = events.query_by_port_dimension(
			self.portia_config, '2DPEQ572HEXP', 4, 1, last=True
		)

		self.assertEqual(device_events.iloc[0].dimension_thing_code, 16)
		self.assertEqual(device_events.iloc[0].dimension_unity_code, 1)
		self.assertEqual(device_events.iloc[0].dimension_code, 1)
		self.assertEqual(device_events.iloc[0].event_code, 1)

	def test_query_by_port_sensor_dimension(self):
		device_events = events.query_by_port_sensor_dimension(
			self.portia_config, '2DPEQ572HEXP', 4, 1, 1
		)

		for i, row in device_events.iterrows():
			self.assertEqual(row.dimension_thing_code, 16)
			self.assertEqual(row.dimension_unity_code, 1)
			self.assertEqual(row.dimension_code, 1)
			self.assertEqual(row.event_code, 1)

	def test_query_by_port_sensor_dimension_last(self):
		device_events = events.query_by_port_sensor_dimension(
			self.portia_config, '2DPEQ572HEXP', 4, 1, 1, last=True
		)

		self.assertEqual(device_events.iloc[0].dimension_thing_code, 16)
		self.assertEqual(device_events.iloc[0].dimension_unity_code, 1)
		self.assertEqual(device_events.iloc[0].dimension_code, 1)
		self.assertEqual(device_events.iloc[0].event_code, 1)

	def test_query_by_port_sensor_event(self):
		device_events = events.query_by_port_sensor_event(
			self.portia_config, '2DPEQ572HEXP', 4, 1, 1
		)

		for i, row in device_events.iterrows():
			self.assertEqual(row.dimension_thing_code, 16)
			self.assertEqual(row.dimension_unity_code, 1)
			self.assertEqual(row.dimension_code, 1)
			self.assertEqual(row.event_code, 1)

	def test_query_by_port_sensor_event_last(self):
		device_events = events.query_by_port_sensor_event(
			self.portia_config, '2DPEQ572HEXP', 4, 1, 1, last=True
		)

		self.assertEqual(device_events.iloc[0].dimension_thing_code, 16)
		self.assertEqual(device_events.iloc[0].dimension_unity_code, 1)
		self.assertEqual(device_events.iloc[0].dimension_code, 1)
		self.assertEqual(device_events.iloc[0].event_code, 1)

	def test_query_by_port_dimension_event(self):
		device_events = events.query_by_port_dimension_event(
			self.portia_config, '2DPEQ572HEXP', 4, 1, 1
		)

		for i, row in device_events.iterrows():
			self.assertEqual(row.dimension_thing_code, 16)
			self.assertEqual(row.dimension_unity_code, 1)
			self.assertEqual(row.dimension_code, 1)
			self.assertEqual(row.event_code, 1)

	def test_query_by_port_dimension_event_last(self):
		device_events = events.query_by_port_dimension_event(
			self.portia_config, '2DPEQ572HEXP', 4, 1, 1, last=True
		)

		self.assertEqual(device_events.iloc[0].dimension_thing_code, 16)
		self.assertEqual(device_events.iloc[0].dimension_unity_code, 1)
		self.assertEqual(device_events.iloc[0].dimension_code, 1)
		self.assertEqual(device_events.iloc[0].event_code, 1)

	def test_query_by_port_sensor_dimension_event(self):
		device_events = events.query_by_port_sensor_dimension_event(
			self.portia_config, '2DPEQ572HEXP', 4, 1, 1, 1
		)

		for i, row in device_events.iterrows():
			self.assertEqual(row.dimension_thing_code, 16)
			self.assertEqual(row.dimension_unity_code, 1)
			self.assertEqual(row.dimension_code, 1)
			self.assertEqual(row.event_code, 1)

	def test_query_by_port_sensor_dimension_event_last(self):
		device_events = events.query_by_port_sensor_dimension_event(
			self.portia_config, '2DPEQ572HEXP', 4, 1, 1, 1, last=True
		)

		self.assertEqual(device_events.iloc[0].dimension_thing_code, 16)
		self.assertEqual(device_events.iloc[0].dimension_unity_code, 1)
		self.assertEqual(device_events.iloc[0].dimension_code, 1)
		self.assertEqual(device_events.iloc[0].event_code, 1)


if __name__ == '__main__':
	unittest.main()
