from tests.conftest import BasicIntegrationTest
import pytest
from parameterized import parameterized
import os
from shutil import rmtree
from Harvester.pull_integration.custom_utilities.short_volume_scraper import FINRAShortScraper


@pytest.fixture(scope="class")
def _setup_scrapers(request):
    request.cls.finra_short_scraper = FINRAShortScraper()


@pytest.mark.usefixtures("_setup_scrapers", autouse=True)
class TestFINRAShortScraper(BasicIntegrationTest):
    """
    This class is used to integration test the short volume scraper utilites.
    """

    def setUp(self):
        self.maxDiff = None
        self.temp_dir = "test-tmp"
        os.makedirs(self.temp_dir, exist_ok=True)

    def tearDown(self):
        if os.path.exists(self.temp_dir):
            rmtree(self.temp_dir)

    @parameterized.expand([("CNMS"),
                           ("FNQC"),
                           ("FNRA"),
                           ("FNSQ"),
                           ("FNYX"),
                           ("FORF")
                           ])
    def test_get_short_volume_data(self, market_choice):
        date = '20210205'
        data = self.finra_short_scraper.get_daily_short_volume_data(date, market_choice)
        expected_keys = ['Date', 'Symbol', 'ShortVolume', 'ShortExemptVolume', 'TotalVolume', 'Market']
        first_row = data[0]
        self.assertListEqual(expected_keys, list(first_row.keys()))

    def test_get_short_volume_data_fails_with_invalid_market_selection(self):
        date = '20210205'
        invalid_market_choice = 'FOO'
        with self.assertRaises(ValueError):
            self.finra_short_scraper.get_daily_short_volume_data(date, invalid_market_choice)

    def test_get_short_volume_data_fails_with_invalid_date_selection(self):
        invalid_date = '20210206'
        market_choice = 'CNMS'
        with self.assertRaises(ValueError):
            self.finra_short_scraper.get_daily_short_volume_data(invalid_date, market_choice)

    def test_download_short_volume_data(self):
        date = '20210205'
        market_choice = 'CNMS'
        self.finra_short_scraper.download_daily_short_volume_data(date, market_choice, self.temp_dir)
        expected_file = f'{self.temp_dir}/CNMSshvol20210205.json'
        self.assertTrue(os.path.isfile(expected_file))
        print("hello world")

    @parameterized.expand([("FNQC"),
                           ("FNSQ"),
                           ("FNYX")
                           ])
    def test_get_short_transaction_data(self, market_choice):
        # TODO: figure out ideal clean up method for the working directory after pulling the data
        date = '202012'
        data_stream = self.finra_short_scraper.get_monthly_short_sale_transaction_data(date, market_choice)
        expected_keys = ['MarketCenter', 'Symbol', 'Date', 'Time', 'ShortType', 'Size', 'Price', 'LinkIndicator', '']
        first_row = (next(data_stream))
        self.assertListEqual(expected_keys, list(first_row.keys()))
        rmtree(self.finra_short_scraper.work_dir)
