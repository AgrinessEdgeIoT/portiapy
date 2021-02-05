"""Integration testing for the application's summary module.
"""

import os
import unittest

from portiapy import summary


from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


class TestSummary(unittest.TestCase):
	"""Set of integration tests for all functions concerning the summary
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

	def test_summary_strategies(self):
		per_minute = summary.SummaryStrategies.PER_MINUTE
		per_hour = summary.SummaryStrategies.PER_HOUR
		per_day = summary.SummaryStrategies.PER_DAY
		per_month = summary.SummaryStrategies.PER_MONTH
		per_year = summary.SummaryStrategies.PER_YEAR
		
		self.assertEqual(per_minute.endpoint, 'perminute')
		self.assertEqual(per_hour.endpoint, 'perhour')
		self.assertEqual(per_day.endpoint, 'perday')
		self.assertEqual(per_month.endpoint, 'permonth')
		self.assertEqual(per_year.endpoint, 'peryear')

	def test_query_by_dimension(self):
		summarized_dimensions = summary.query_by_dimension(
			self.portia_config,
			1,
			[{
				'device': '2DPEQ572HEXP'
			}, {
				'device': '3WPH414SRSTZ'
			}],
			strategy=summary.SummaryStrategies.PER_DAY,
			params={
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
		    }
		)

		for i, row in summarized_dimensions.iterrows():
			self.assertEqual(row.dimension_unity_code, 1)

	def test_query_device_by_dimension(self):
		summarized_dimensions = summary.query_device_by_dimension(
			self.portia_config,
			'2DPEQ572HEXP',
			1,
			None,
			strategy=summary.SummaryStrategies.PER_DAY,
			params={
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
		    }
		)

		for i, row in summarized_dimensions.iterrows():
			self.assertEqual(row.dimension_unity_code, 1)

	def test_query_by_port_sensor(self):
		summarized_dimensions = summary.query_by_port_sensor(
			self.portia_config,
			'2DPEQ572HEXP',
			4, 
			1,
			strategy=summary.SummaryStrategies.PER_DAY,
			params={
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
		    }
		)

		for i, row in summarized_dimensions.iterrows():
			self.assertEqual(row.dimension_unity_code, 1)

	def test_query_by_port_sensor_dimension(self):
		summarized_dimensions = summary.query_by_port_sensor_dimension(
			self.portia_config,
			'2DPEQ572HEXP',
			4,
			1,
			1,
			strategy=summary.SummaryStrategies.PER_DAY,
			params={
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
		    }
		)

		for i, row in summarized_dimensions.iterrows():
			self.assertEqual(row.dimension_unity_code, 1)


if __name__ == '__main__':
	unittest.main()
