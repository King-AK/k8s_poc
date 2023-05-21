from tests.conftest import BasicUnitTest
import json
from marshmallow import EXCLUDE
import api.schemas as s
import api.models as m


class TestAPIModels(BasicUnitTest):

    def test_create_stock_time_series_object_w_alpha_vantage_data_single(self):
        test_data = json.load(open('tests/unit/test_data/alphavantage/given/market_time_series_daily.json', 'r'))

        # Single
        single_target_date = '2020-06-22'
        test_data_single = test_data['Time Series (Daily)'][single_target_date]
        test_data_single['symbol'] = test_data['Meta Data']['2. Symbol']
        test_data_single['datetime'] = single_target_date
        load_data = s.AlphaVantageStockTimeSeriesSchema().load(test_data_single)

        # Create object and push data into Database
        F_6_22_data = m.StockTimeSeries(**load_data)
        F_6_22_data.add_to_db()

        # TODO: assert row values in DB match expected with a query check in addition to count check -- introduce a JSON file
        validation_query = f"SELECT * FROM stock_time_series WHERE symbol='{F_6_22_data.symbol}' AND volume={F_6_22_data.volume}"
        rows = [i for i in m.db.engine.execute(validation_query)]
        self.assertEqual(1, len(rows))

        # Drop row from database
        F_6_22_data.delete_from_db()

    def test_create_stock_time_series_object_w_alpha_vantage_data_many(self):
        test_data = json.load(open('tests/unit/test_data/alphavantage/given/market_time_series_daily.json', 'r'))

        # Load AlphaVantage data -- Many
        time_series_key = 'Time Series (Daily)'
        test_data_many = s.AlphaVantageStockTimeSeriesSchema.clean_time_series_dictionary_list(test_data[time_series_key], 'F')
        load_data = s.AlphaVantageStockTimeSeriesSchema().load(test_data_many, many=True)

        # Bulk add dictionaries to database w/ classmethod function
        m.StockTimeSeries.bulk_insert(load_data)

        # SQL row count check and verify that ORM objects can be created using the table w/ the expected number of objects returned
        validation_query = "SELECT * FROM stock_time_series ORDER BY datetime ASC"
        rows = [i for i in m.db.engine.execute(validation_query)]
        self.assertEqual(100, len(rows))

        # Bulk delete rows from database w/ classmethod function
        m.StockTimeSeries.bulk_delete_symbol('F')

    def test_create_crypto_time_series_object_w_alpha_vantage_data_single(self):
        test_data = json.load(open('tests/unit/test_data/alphavantage/given/crypto_time_series_daily.json', 'r'))

        # Single
        single_target_date = '2020-06-22'
        test_data_single = test_data['Time Series (Digital Currency Daily)'][single_target_date]
        test_data_single['symbol'] = test_data['Meta Data']['2. Digital Currency Code']
        test_data_single['datetime'] = single_target_date
        load_data = s.AlphaVantageUSDCryptoTimeSeriesSchema().load(test_data_single, unknown=EXCLUDE)

        # Create object and push data into Database
        LINK_6_22_data = m.CryptoTimeSeries(**load_data)
        LINK_6_22_data.add_to_db()

        # TODO: assert row values in DB match expected with a query check in addition to count check -- introduce a JSON file
        validation_query = f"SELECT * FROM crypto_time_series WHERE symbol='{LINK_6_22_data.symbol}' AND volume={LINK_6_22_data.volume}"
        rows = [i for i in m.db.engine.execute(validation_query)]
        self.assertEqual(1, len(rows))

        # Drop row from database
        LINK_6_22_data.delete_from_db()

    def test_create_crypto_time_series_object_w_alpha_vantage_data_many(self):
        test_data = json.load(open('tests/unit/test_data/alphavantage/given/crypto_time_series_daily.json', 'r'))

        # Load AlphaVantage data -- Many
        time_series_key = 'Time Series (Digital Currency Daily)'
        test_data_many = s.AlphaVantageStockTimeSeriesSchema.clean_time_series_dictionary_list(test_data[time_series_key], 'LINK')
        load_data = s.AlphaVantageUSDCryptoTimeSeriesSchema().load(test_data_many, many=True, unknown=EXCLUDE)

        # Bulk add dictionaries to database w/ classmethod function
        m.CryptoTimeSeries.bulk_insert(load_data)

        # SQL row count check and verify that ORM objects can be created using the table w/ the expected number of objects returned
        validation_query = "SELECT * FROM crypto_time_series ORDER BY datetime ASC"
        rows = [i for i in m.db.engine.execute(validation_query)]
        self.assertEqual(613, len(rows))

        # Bulk delete rows from database w/ classmethod function
        m.CryptoTimeSeries.bulk_delete_symbol('LINK')
