from tests.conftest import BasicIntegrationTest
import pytest
from Harvester.pull_integration.custom_utilities.dix_scraper import DIXScraper


@pytest.fixture(scope="class")
def _setup_scrapers(request):
    request.cls.dix_scraper = DIXScraper()


@pytest.mark.usefixtures("_setup_scrapers", autouse=True)
class TestDIXScraper(BasicIntegrationTest):
    """
    This class is used to integration test the DIX scraper utilites.
    """

    def test_download_dix_data(self):
        data = DIXScraper().download_dix_sp500_data()
        self.assertCountEqual(['date', 'symbol', 'price', 'dix', 'gex'], data[0].keys())
        self.assertEqual('INX', data[0]['symbol'])
