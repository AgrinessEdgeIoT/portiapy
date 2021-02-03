"""Unit testing of PortiaPy's utils module.
"""

import unittest

import pandas as pd

from portiapy import utils


class TestHumanization(unittest.TestCase):
	"""Set of unit tests for all functions concerning humanization of data.
	"""
	def test_humanize_thing_code(self):
		h_thing_code = utils.humanize_thing_code(1)
		self.assertEqual(h_thing_code, 'Sensor_Agriness_TU')

	def test_humanize_dimension_code(self):
		h_dimension_code = utils.humanize_dimension_code(1)
		self.assertEqual(h_dimension_code, 'Point Temperature')

		h_dimension_code = utils.humanize_dimension_code(1, 'pt-br')
		self.assertEqual(h_dimension_code, 'Temperatura Pontual')

		h_dimension_code = utils.humanize_dimension_code(1, custom={
			'en-us': { 1: 'Temperatura Pontual de Teste' }
		})
		self.assertEqual(h_dimension_code, 'Temperatura Pontual de Teste')

	def test_humanize_event_code(self):
		h_dimension_code = utils.humanize_event_code(1)
		self.assertEqual(h_dimension_code, 'Communication State')

		h_dimension_code = utils.humanize_event_code(1, 'pt-br')
		self.assertEqual(h_dimension_code, 'Estado de Comunicação')

		h_dimension_code = utils.humanize_event_code(1, custom={
			'en-us': { 1: 'Status de Comunicação' }
		})
		self.assertEqual(h_dimension_code, 'Status de Comunicação')

	def test_humanize_unity_code(self):
		h_dimension_code = utils.humanize_unity_code(1)
		self.assertEqual(h_dimension_code, '°C')

		h_dimension_code = utils.humanize_unity_code(1, 'pt-br')
		self.assertEqual(h_dimension_code, '°C')

		h_dimension_code = utils.humanize_unity_code(1, custom={
			'en-us': { 1: 'Celsius' }
		})
		self.assertEqual(h_dimension_code, 'Celsius')

	def test_humanize_dimensions_dataframe(self):
		dataframe = pd.DataFrame(data=[{
			'header_timestamp': 1565634220016,
			'dimension_value': 60,
			'dimension_code': 1,
			'dimension_unity_code': 1,
			'dimension_thing_code': 15
		}, {
			'header_timestamp': 1565634165295,
			'dimension_value': 60,
			'dimension_code': 3,
			'dimension_unity_code': 2,
			'dimension_thing_code': 16
		}])

		h_dataframe = utils.humanize_dimensions_dataframe(dataframe)
		self.assertIn('header_timestamp', h_dataframe.columns)
		self.assertIn('dimension_value', h_dataframe.columns)
		self.assertIn('dimension_code', h_dataframe.columns)
		self.assertIn('dimension_unity_code', h_dataframe.columns)
		self.assertIn('dimension_thing_code', h_dataframe.columns)
		self.assertIn('dimension_thing', h_dataframe.columns)
		self.assertIn('dimension', h_dataframe.columns)
		self.assertIn('dimension_unity', h_dataframe.columns)

		self.assertEqual(
			h_dataframe.iloc[0].get('dimension_thing'), 'Sensor_Inobram_T'
		)
		self.assertEqual(
			h_dataframe.iloc[0].get('dimension'), 'Point Temperature'
		)
		self.assertEqual(h_dataframe.iloc[0].get('dimension_unity'), '°C')

		self.assertEqual(
			h_dataframe.iloc[1].get('dimension_thing'), 'Sensor_Inobram_TU'
		)
		self.assertEqual(
			h_dataframe.iloc[1].get('dimension'), 'Point Humidity'
		)
		self.assertEqual(h_dataframe.iloc[1].get('dimension_unity'), '%')

	def test_humanize_events_dataframe(self):
		dataframe = pd.DataFrame(data=[{
			'header_timestamp': 1565634220016,
			'event_value': 'ON',
			'dimension_code': 1,
			'event_code': 1,
			'dimension_unity_code': 1,
			'dimension_thing_code': 15
		}, {
			'header_timestamp': 1565634165295,
			'event_value': 'OFF',
			'dimension_code': 3,
			'event_code': 1,
			'dimension_unity_code': 2,
			'dimension_thing_code': 16
		}])

		h_dataframe = utils.humanize_events_dataframe(dataframe)
		self.assertIn('header_timestamp', h_dataframe.columns)
		self.assertIn('event_value', h_dataframe.columns)
		self.assertIn('dimension_code', h_dataframe.columns)
		self.assertIn('event_code', h_dataframe.columns)
		self.assertIn('dimension_unity_code', h_dataframe.columns)
		self.assertIn('dimension_thing_code', h_dataframe.columns)
		self.assertIn('dimension_thing', h_dataframe.columns)
		self.assertIn('dimension', h_dataframe.columns)
		self.assertIn('event', h_dataframe.columns)
		self.assertIn('dimension_unity', h_dataframe.columns)

		self.assertEqual(
			h_dataframe.iloc[0].get('dimension_thing'), 'Sensor_Inobram_T'
		)
		self.assertEqual(
			h_dataframe.iloc[0].get('dimension'), 'Point Temperature'
		)
		self.assertEqual(
			h_dataframe.iloc[0].get('event'), 'Communication State'
		)
		self.assertEqual(h_dataframe.iloc[0].get('dimension_unity'), '°C')

		self.assertEqual(
			h_dataframe.iloc[1].get('dimension_thing'), 'Sensor_Inobram_TU'
		)
		self.assertEqual(
			h_dataframe.iloc[1].get('dimension'), 'Point Humidity'
		)
		self.assertEqual(
			h_dataframe.iloc[1].get('event'), 'Communication State'
		)
		self.assertEqual(h_dataframe.iloc[1].get('dimension_unity'), '%')

	# def test_humanizeJson(self):
	# 	"""Steps:
	# 	1 - Creates a JSON object
	# 	2 - Uses humanizeJson(json) and verify results
	# 	3 - Uses humanizeJson(json, datetime=True) and verify results
	# 	"""
	# 	json_ = {
	# 		'thing_code': 13,
	# 		'ports': [{
	# 			'thing_code': 15,
	# 			'sensors': [{
	# 				'last_package': {
	# 					'header_timestamp': 1565634220016,
	# 					'dimension_value': 60,
	# 					'dimension_code': 1,
	# 					'dimension_unity_code': 1,
	# 					'dimension_thing_code': 15
	# 				}
	# 			}, {
	# 				'last_package': {
	# 					'header_timestamp': 1565634165295,
	# 					'dimension_value': 60,
	# 					'dimension_code': 3,
	# 					'dimension_unity_code': 2,
	# 					'dimension_thing_code': 16
	# 				}
	# 			}]
	# 		}]
	# 	}

	# 	res = utils.humanizeJson(json_)
	# 	self.assertIsInstance(res.get('thing_code'), str)
	# 	for port in res.get('ports'):
	# 		self.assertIsInstance(port.get('thing_code'), str)
	# 		for sensor in port.get('sensors'):
	# 			last_package = sensor.get('last_package')
	# 			self.assertIn('header_timestamp', last_package.keys())
	# 			self.assertIn('dimension_value', last_package.keys())
	# 			self.assertNotIn('dimension_code', last_package.keys())
	# 			self.assertIn('dimension', last_package.keys())
	# 			self.assertNotIn('dimension_unity_code', last_package.keys())
	# 			self.assertIn('dimension_unity', last_package.keys())
	# 			self.assertNotIn('dimension_thing_code', last_package.keys())
	# 			self.assertIn('dimension_thing', last_package.keys())

	# 			self.assertIsInstance(last_package.get('dimension'), str)
	# 			self.assertIsInstance(last_package.get('dimension_unity'), str)
	# 			self.assertIsInstance(last_package.get('dimension_thing'), str)

	# 	json_ = {
	# 		'thing_code': 13,
	# 		'ports': [{
	# 			'thing_code': 15,
	# 			'sensors': [{
	# 				'last_package': {
	# 					'header_timestamp': 1565634220016,
	# 					'dimension_value': 60,
	# 					'dimension_code': 1,
	# 					'dimension_unity_code': 1,
	# 					'dimension_thing_code': 15
	# 				}
	# 			}, {
	# 				'last_package': {
	# 					'header_timestamp': 1565634165295,
	# 					'dimension_value': 60,
	# 					'dimension_code': 3,
	# 					'dimension_unity_code': 2,
	# 					'dimension_thing_code': 16
	# 				}
	# 			}]
	# 		}]
	# 	}

	# 	res = utils.humanizeJson(json_, datetime=True)
	# 	for port in res.get('ports'):
	# 		for sensor in port.get('sensors'):
	# 			last_package = sensor.get('last_package')
	# 			self.assertNotIn('header_timestamp', last_package.keys())
	# 			self.assertIn('header_datetime', last_package.keys())

	# 			self.assertIsInstance(last_package.get('header_datetime'), str)


if __name__ == '__main__':
	unittest.main()
