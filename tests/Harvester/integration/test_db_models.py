from tests.conftest import DBIntegrationTest
import json
import Harvester.push_integration.db.models as m


class TestDBModels(DBIntegrationTest):

    def test_stock_time_series(self):
        test_data_path = "tests/Harvester/integration/test_data/test_stock_time_series_data.json"
        test_data = json.load(open(test_data_path, 'r'))
        m.StockTimeSeries.bulk_upsert(test_data, self.engine)

        # Test initial upsert
        self.assertEqual(100, self.engine.execute("SELECT count(1) FROM stock_time_series").fetchone()[0])
        # Test subsequent upsert of same data does not change row count
        m.StockTimeSeries.bulk_upsert(test_data, self.engine)
        self.assertEqual(100, self.engine.execute("SELECT count(1) FROM stock_time_series").fetchone()[0])

    def test_options_time_series(self):
        test_data_path = "tests/Harvester/integration/test_data/test_options_time_series_data.json"
        test_data = json.load(open(test_data_path, 'r'))
        m.OptionsTimeSeries.bulk_upsert(test_data, self.engine)
        # TODO: correct here
        # Test initial upsert
        self.assertEqual(599, self.engine.execute("SELECT count(1) FROM options_time_series").fetchone()[0])
        # Test subsequent upsert of same data does not change row count
        m.OptionsTimeSeries.bulk_upsert(test_data, self.engine)
        self.assertEqual(599, self.engine.execute("SELECT count(1) FROM options_time_series").fetchone()[0])

    def test_crypto_time_series(self):
        test_data_path = "tests/Harvester/integration/test_data/test_crypto_time_series_data.json"
        test_data = json.load(open(test_data_path, 'r'))
        m.CryptoTimeSeries.bulk_upsert(test_data, self.engine)

        # Test initial upsert
        self.assertEqual(613, self.engine.execute("SELECT count(1) FROM crypto_time_series").fetchone()[0])
        # Test subsequent upsert of same data does not change row count
        m.CryptoTimeSeries.bulk_upsert(test_data, self.engine)
        self.assertEqual(613, self.engine.execute("SELECT count(1) FROM crypto_time_series").fetchone()[0])

    def test_dix_time_series(self):
        test_data_path = "tests/Harvester/integration/test_data/test_dix_time_series_data.json"
        test_data = json.load(open(test_data_path, 'r'))
        m.DIXTimeSeries.bulk_upsert(test_data, self.engine)

        # Test initial upsert
        self.assertEqual(2629, self.engine.execute("SELECT count(1) FROM dix_time_series").fetchone()[0])
        # Test subsequent upsert of same data does not change row count
        m.DIXTimeSeries.bulk_upsert(test_data, self.engine)
        self.assertEqual(2629, self.engine.execute("SELECT count(1) FROM dix_time_series").fetchone()[0])
