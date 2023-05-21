from tests.conftest import BasicIntegrationTest
import pytest
from parameterized import parameterized
from Harvester.pull_integration.external_apis.yahoo_finance import YahooFinanceAPI


@pytest.fixture(scope="class")
def _setup_yahoofinance(request):
    request.cls.yf = YahooFinanceAPI()


@pytest.mark.usefixtures("_setup_yahoofinance", autouse=True)
class TestYahooFinance(BasicIntegrationTest):
    """
    This class is used to integration test YahooFinance (yahoo-fin)
    """

    def setUp(self):
        self.maxDiff = None

    def test_get_options(self):
        result_json = self.yf.get_options("F")
        expected_keys = ['Contract Name', 'Last Trade Date', 'Strike', 'Last Price', 'Bid', 'Ask', 'Change',
                         '% Change', 'Volume', 'Open Interest', 'Implied Volatility', 'symbol', 'expiration_date', 'option_type', 'datetime']
        for row in result_json:
            self.assertCountEqual(expected_keys, list(row.keys()))
