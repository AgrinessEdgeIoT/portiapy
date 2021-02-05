"""Integration testing for the application's select module.
"""

import os
import unittest

from portiapy import select


from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


class TestSelect(unittest.TestCase):
	"""Set of integration tests for all functions concerning the select
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
		dimensions = select.query_by_port_sensor(
			self.portia_config, '2DPEQ572HEXP', 4, 1
		)

		for i, row in dimensions.iterrows():
			self.assertEqual(row.dimension_thing_code, 16)
			self.assertEqual(row.dimension_unity_code, 1)
			self.assertEqual(row.dimension_code, 1)

	def test_query_by_port_sensor_last(self):
		dimensions = select.query_by_port_sensor(
			self.portia_config, '2DPEQ572HEXP', 4, 1, last=True
		)

		self.assertEqual(dimensions.iloc[0].dimension_thing_code, 16)
		self.assertEqual(dimensions.iloc[0].dimension_unity_code, 1)
		self.assertEqual(dimensions.iloc[0].dimension_code, 1)

	def test_query_by_port_dimension(self):
		dimensions = select.query_by_port_dimension(
			self.portia_config, '2DPEQ572HEXP', 4, 1
		)

		for i, row in dimensions.iterrows():
			self.assertEqual(row.dimension_thing_code, 16)
			self.assertEqual(row.dimension_unity_code, 1)
			self.assertEqual(row.dimension_code, 1)

	def test_query_by_port_dimension_last(self):
		dimensions = select.query_by_port_dimension(
			self.portia_config, '2DPEQ572HEXP', 4, 1, last=True
		)

		self.assertEqual(dimensions.iloc[0].dimension_thing_code, 16)
		self.assertEqual(dimensions.iloc[0].dimension_unity_code, 1)
		self.assertEqual(dimensions.iloc[0].dimension_code, 1)

	def test_query_by_port_sensor_dimension(self):
		dimensions = select.query_by_port_sensor_dimension(
			self.portia_config, '2DPEQ572HEXP', 4, 1, 1
		)

		for i, row in dimensions.iterrows():
			self.assertEqual(row.dimension_thing_code, 16)
			self.assertEqual(row.dimension_unity_code, 1)
			self.assertEqual(row.dimension_code, 1)

	def test_query_by_port_sensor_dimension_last(self):
		dimensions = select.query_by_port_sensor_dimension(
			self.portia_config, '2DPEQ572HEXP', 4, 1, 1, last=True
		)

		self.assertEqual(dimensions.iloc[0].dimension_thing_code, 16)
		self.assertEqual(dimensions.iloc[0].dimension_unity_code, 1)
		self.assertEqual(dimensions.iloc[0].dimension_code, 1)


if __name__ == '__main__':
	unittest.main()
