import json

from parameterized import parameterized

import py_harvester.marshmallowSchemas.AlphaVantageSchema as s
from tests.conftest import BasicUnitTest


class TestAlphaVantageSchemaEnforcement(BasicUnitTest):

    @parameterized.expand([("DAILY"),
                           ("INTRADAY_5MIN"),
                           ])
    def test_AlphaVantageTimeSeriesSchema_clean_time_series_dictionary_list(self, test_name):
        file_info = {"DAILY": {"test_data_path": 'tests/test_data/alphavantage/given/market_time_series_daily.json',
                               "time_series_key": 'Time Series (Daily)',
                               "expected_data_path": 'tests/test_data/alphavantage/expected/test_AlphaVantageTimeSeriesSchema_clean_time_series_dictionary_list.json'},  # noqa:E501
                     "INTRADAY_5MIN": {"test_data_path": 'tests/test_data/alphavantage/given/market_time_series_intraday_5min.json',
                                       "time_series_key": 'Time Series (5min)',
                                       "expected_data_path": 'tests/test_data/alphavantage/expected/test_AlphaVantageTimeSeriesSchema_clean_time_series_dictionary_list_intraday_5min.json'}}  # noqa:E501
        test_data_path = file_info[test_name]['test_data_path']
        test_data = json.load(open(test_data_path, 'r'))
        time_series_key = file_info[test_name]['time_series_key']
        test_data_many = s.AlphaVantageStockTimeSeriesSchema.clean_time_series_dictionary_list(test_data[time_series_key], 'F')

        # Assert output matches expected
        expected_data_path = file_info[test_name]['expected_data_path']
        expected_data = json.load(open(expected_data_path, 'r'))
        self.assertCountEqual(expected_data, test_data_many)

    @parameterized.expand([("DAILY", "2020-06-22", 100),
                           ("WEEKLY",  "2020-06-26", 1087),
                           ("MONTHLY",  "2020-06-30", 250),
                           ("INTRADAY_1MIN",  "2021-03-02 18:41:00", 100),
                           ("INTRADAY_5MIN",  "2021-03-02 15:15:00", 100),
                           ("INTRADAY_15MIN",  "2021-03-02 10:45:00", 100),
                           ("INTRADAY_30MIN",  "2021-03-01 07:30:00", 100),
                           ("INTRADAY_60MIN",  "2021-03-01 14:00:00", 100),
                           ])
    def test_load_AlphaVantageStockTimeSeriesSchema(self, test_name, single_target_date, expected_many_load_len):
        file_info = {"DAILY": {"path": "tests/test_data/alphavantage/given/market_time_series_daily.json",
                               "time_series_key": 'Time Series (Daily)'},
                     "WEEKLY": {"path": "tests/test_data/alphavantage/given/market_time_series_weekly.json",
                                "time_series_key": 'Weekly Time Series'},
                     "MONTHLY": {"path": "tests/test_data/alphavantage/given/market_time_series_monthly.json",
                                 "time_series_key": 'Monthly Time Series'},
                     "INTRADAY_1MIN": {"path": "tests/test_data/alphavantage/given/market_time_series_intraday_1min.json",
                                       "time_series_key": 'Time Series (1min)'},
                     "INTRADAY_5MIN": {"path": "tests/test_data/alphavantage/given/market_time_series_intraday_5min.json",
                                       "time_series_key": 'Time Series (5min)'},
                     "INTRADAY_15MIN": {"path": "tests/test_data/alphavantage/given/market_time_series_intraday_15min.json",
                                        "time_series_key": 'Time Series (15min)'},
                     "INTRADAY_30MIN": {"path": "tests/test_data/alphavantage/given/market_time_series_intraday_30min.json",
                                        "time_series_key": 'Time Series (30min)'},
                     "INTRADAY_60MIN": {"path": "tests/test_data/alphavantage/given/market_time_series_intraday_60min.json",
                                        "time_series_key": 'Time Series (60min)'}}

        path = file_info[test_name]['path']
        time_series_key = file_info[test_name]['time_series_key']

        test_data = json.load(open(path, 'r'))
        expected_keys = ['high', 'low', 'open', 'close', 'volume', 'datetime', 'symbol']

        # Single
        test_data_single = test_data[time_series_key][single_target_date]
        test_data_single['symbol'] = test_data['Meta Data']['2. Symbol']
        test_data_single['datetime'] = single_target_date
        load_data = s.AlphaVantageStockTimeSeriesSchema().load(test_data_single)
        self.assertCountEqual(expected_keys, load_data.keys())

        # Many
        test_data_many = s.AlphaVantageStockTimeSeriesSchema.clean_time_series_dictionary_list(test_data[time_series_key], 'F')
        load_data = s.AlphaVantageStockTimeSeriesSchema().load(test_data_many, many=True)
        self.assertCountEqual(expected_keys, load_data[0].keys())
        self.assertEqual(len(test_data_many), len(load_data))
        self.assertEqual(expected_many_load_len, len(load_data))
