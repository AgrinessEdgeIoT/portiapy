"""Unit tests of PortiaPy's utils module.

Test Classes: TestHumanization
"""

import unittest

import pandas as pd

from portiapy import utils


class TestHumanization(unittest.TestCase):
	"""Set of unit tests for all functions concerning humanization of a data
	structure's contents.

	Tests: test_humanize, test_humanizeJson
	"""
	def test_humanize(self):
		"""Steps:
		1 - Creates a data frame
		2 - Uses humanize(df) and verify results
		3 - Uses humanize(df, datetime=True) and verify results
		"""
		df = pd.DataFrame(
			[[1565634220016, 60, 1, 1, 15], [1565634165295, 60, 3, 2, 16]],
			columns=['header_timestamp', 'dimension_value', 'dimension_code',
					 'dimension_unity_code', 'dimension_thing_code']
		)

		res = utils.humanize(df)
		self.assertIn('header_timestamp', res.columns)
		self.assertIn('dimension_value', res.columns)
		self.assertNotIn('dimension_code', res.columns)
		self.assertIn('dimension', res.columns)
		self.assertNotIn('dimension_unity_code', res.columns)
		self.assertIn('dimension_unity', res.columns)
		self.assertNotIn('dimension_thing_code', res.columns)
		self.assertIn('dimension_thing', res.columns)

		for idx, row in res.iterrows():
			self.assertEqual(row.get('header_timestamp'),
							 df.loc[idx].get('header_timestamp'))
			self.assertIsInstance(row.get('dimension'), str)
			self.assertIsInstance(row.get('dimension_unity'), str)
			self.assertIsInstance(row.get('dimension_thing'), str)

		df = pd.DataFrame(
			[[1565634220016, 60, 1, 1, 15], [1565634165295, 60, 3, 2, 16]],
			columns=['header_timestamp', 'dimension_value', 'dimension_code',
					 'dimension_unity_code', 'dimension_thing_code']
		)

		res = utils.humanize(df, datetime=True)
		self.assertNotIn('header_timestamp', res.columns)
		self.assertIn('header_datetime', res.columns)

		for idx, row in res.iterrows():
			self.assertIsInstance(row.get('header_datetime'), str)

	def test_humanizeJson(self):
		"""Steps:
		1 - Creates a JSON object
		2 - Uses humanizeJson(json) and verify results
		3 - Uses humanizeJson(json, datetime=True) and verify results
		"""
		json_ = {
			'thing_code': 13,
			'ports': [{
				'thing_code': 15,
				'sensors': [{
					'last_package': {
						'header_timestamp': 1565634220016,
						'dimension_value': 60,
						'dimension_code': 1,
						'dimension_unity_code': 1,
						'dimension_thing_code': 15
					}
				}, {
					'last_package': {
						'header_timestamp': 1565634165295,
						'dimension_value': 60,
						'dimension_code': 3,
						'dimension_unity_code': 2,
						'dimension_thing_code': 16
					}
				}]
			}]
		}

		res = utils.humanizeJson(json_)
		self.assertIsInstance(res.get('thing_code'), str)
		for port in res.get('ports'):
			self.assertIsInstance(port.get('thing_code'), str)
			for sensor in port.get('sensors'):
				last_package = sensor.get('last_package')
				self.assertIn('header_timestamp', last_package.keys())
				self.assertIn('dimension_value', last_package.keys())
				self.assertNotIn('dimension_code', last_package.keys())
				self.assertIn('dimension', last_package.keys())
				self.assertNotIn('dimension_unity_code', last_package.keys())
				self.assertIn('dimension_unity', last_package.keys())
				self.assertNotIn('dimension_thing_code', last_package.keys())
				self.assertIn('dimension_thing', last_package.keys())

				self.assertIsInstance(last_package.get('dimension'), str)
				self.assertIsInstance(last_package.get('dimension_unity'), str)
				self.assertIsInstance(last_package.get('dimension_thing'), str)

		json_ = {
			'thing_code': 13,
			'ports': [{
				'thing_code': 15,
				'sensors': [{
					'last_package': {
						'header_timestamp': 1565634220016,
						'dimension_value': 60,
						'dimension_code': 1,
						'dimension_unity_code': 1,
						'dimension_thing_code': 15
					}
				}, {
					'last_package': {
						'header_timestamp': 1565634165295,
						'dimension_value': 60,
						'dimension_code': 3,
						'dimension_unity_code': 2,
						'dimension_thing_code': 16
					}
				}]
			}]
		}

		res = utils.humanizeJson(json_, datetime=True)
		for port in res.get('ports'):
			for sensor in port.get('sensors'):
				last_package = sensor.get('last_package')
				self.assertNotIn('header_timestamp', last_package.keys())
				self.assertIn('header_datetime', last_package.keys())

				self.assertIsInstance(last_package.get('header_datetime'), str)


if __name__ == '__main__':
	unittest.main()
