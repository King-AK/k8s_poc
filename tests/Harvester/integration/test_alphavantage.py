from tests.conftest import BasicIntegrationTest
import pytest
from parameterized import parameterized
from Harvester.pull_integration.external_apis.alpha_vantage import AlphaVantageAPI
from time import sleep
import os


@pytest.fixture(scope="class")
def _setup_alphavantage(request):
    api_key = os.environ.get("ALPHAVANTAGE_API_KEY")
    request.cls.avi = AlphaVantageAPI(api_key)


@pytest.fixture(scope="function")
def _sleep_alphavantage(request):
    sleep(12)


@pytest.mark.usefixtures("_setup_alphavantage", autouse=True)
@pytest.mark.usefixtures("_sleep_alphavantage", autouse=True)
class TestAlphaVantage(BasicIntegrationTest):
    """
    This class is used to integration test AlphaVantage - running these tests is NOT optimal.
    NOTE: standard API call frequency is 5 calls per minute and 500 calls per day. Really hits on the importance of the yfinance fork
    """

    def setUp(self):
        self.maxDiff = None

    def test_query_market_time_series(self):
        result_json = self.avi.query_market_time_series("F")
        expected_toplvl_keys = ["Meta Data", "Time Series (Daily)"]
        expected_meta_data_keys = ["1. Information", "2. Symbol", "3. Last Refreshed", "4. Output Size", "5. Time Zone"]
        self.assertCountEqual(expected_toplvl_keys, result_json.keys())
        self.assertCountEqual(expected_meta_data_keys, result_json["Meta Data"].keys())

    @parameterized.expand([("TIME_SERIES_DAILY", "Time Series (Daily)"), ("TIME_SERIES_DAILY_ADJUSTED", "Time Series (Daily)"),
                           ("TIME_SERIES_WEEKLY", "Weekly Time Series"), ("TIME_SERIES_WEEKLY_ADJUSTED", "Weekly Adjusted Time Series"),
                           ("TIME_SERIES_MONTHLY", "Monthly Time Series"),  ("TIME_SERIES_MONTHLY_ADJUSTED", "Monthly Adjusted Time Series")])
    def test_query_market_time_series_function_options(self, function, expected_key):
        result_json = self.avi.query_market_time_series("F", function=function)
        expected_toplvl_keys = ["Meta Data", expected_key]
        self.assertCountEqual(expected_toplvl_keys, result_json.keys())

    def test_query_market_time_series_intraday(self):
        result_json = self.avi.query_market_time_series_intraday("F")
        expected_toplvl_keys = ["Meta Data", "Time Series (5min)"]
        expected_meta_data_keys = ["1. Information", "2. Symbol", "3. Last Refreshed", "4. Interval", "5. Output Size", "6. Time Zone"]
        self.assertCountEqual(expected_toplvl_keys, result_json.keys())
        self.assertCountEqual(expected_meta_data_keys, result_json["Meta Data"].keys())

    @parameterized.expand([("1min", "Time Series (1min)"), ("5min", "Time Series (5min)"),
                           ("15min", "Time Series (15min)"), ("30min", "Time Series (30min)"),
                           ("60min", "Time Series (60min)")])
    def test_query_market_time_series_intraday_interval_options(self, interval, expected_key):
        result_json = self.avi.query_market_time_series_intraday("F", interval=interval)
        expected_toplvl_keys = ["Meta Data", expected_key]
        self.assertCountEqual(expected_toplvl_keys, result_json.keys())

    def test_query_crypto_time_series(self):
        result_json = self.avi.query_crypto_time_series("LINK")
        expected_toplvl_keys = ["Meta Data", "Time Series (Digital Currency Daily)"]
        expected_meta_data_keys = ["1. Information", "2. Digital Currency Code", "3. Digital Currency Name", "4. Market Code", "5. Market Name",
                                   "6. Last Refreshed", "7. Time Zone"]
        self.assertCountEqual(expected_toplvl_keys, result_json.keys())
        self.assertCountEqual(expected_meta_data_keys, result_json["Meta Data"].keys())

    @parameterized.expand([("DIGITAL_CURRENCY_DAILY", "Time Series (Digital Currency Daily)"),
                           ("DIGITAL_CURRENCY_WEEKLY", "Time Series (Digital Currency Weekly)"),
                           ("DIGITAL_CURRENCY_MONTHLY", "Time Series (Digital Currency Monthly)")])
    def test_query_crypto_time_series_function_options(self, function, expected_key):
        result_json = self.avi.query_crypto_time_series("LINK", function=function)
        expected_toplvl_keys = ["Meta Data", expected_key]
        self.assertCountEqual(expected_toplvl_keys, result_json.keys())

    def test_query_company_overview(self):
        result_json = self.avi.query_company_overview('F')
        expected_toplvl_keys = ['Symbol', 'AssetType', 'Name', 'Description', 'Exchange', 'Currency', 'Country', 'Sector', 'Industry', 'Address',
                                'FullTimeEmployees', 'FiscalYearEnd', 'LatestQuarter', 'MarketCapitalization', 'EBITDA', 'PERatio', 'PEGRatio', 'BookValue',
                                'DividendPerShare', 'DividendYield', 'EPS', 'RevenuePerShareTTM', 'ProfitMargin', 'OperatingMarginTTM', 'ReturnOnAssetsTTM',
                                'ReturnOnEquityTTM', 'RevenueTTM', 'GrossProfitTTM', 'DilutedEPSTTM', 'QuarterlyEarningsGrowthYOY', 'QuarterlyRevenueGrowthYOY',
                                'AnalystTargetPrice', 'TrailingPE', 'ForwardPE', 'PriceToSalesRatioTTM', 'PriceToBookRatio', 'EVToRevenue', 'EVToEBITDA',
                                'Beta', '52WeekHigh', '52WeekLow', '50DayMovingAverage', '200DayMovingAverage', 'SharesOutstanding', 'SharesFloat',
                                'SharesShort', 'SharesShortPriorMonth', 'ShortRatio', 'ShortPercentOutstanding', 'ShortPercentFloat', 'PercentInsiders',
                                'PercentInstitutions', 'ForwardAnnualDividendRate', 'ForwardAnnualDividendYield', 'PayoutRatio', 'DividendDate',
                                'ExDividendDate', 'LastSplitFactor', 'LastSplitDate']
        self.assertCountEqual(expected_toplvl_keys, result_json.keys())

    def test_query_income_statement(self):
        result_json = self.avi.query_income_statement('F')
        expected_toplvl_keys = ['symbol', 'annualReports', 'quarterlyReports']
        self.assertCountEqual(expected_toplvl_keys, result_json.keys())

    def test_query_balance_sheet(self):
        result_json = self.avi.query_balance_sheet('F')
        expected_toplvl_keys = ['symbol', 'annualReports', 'quarterlyReports']
        self.assertCountEqual(expected_toplvl_keys, result_json.keys())

    def test_query_cash_flow(self):
        result_json = self.avi.query_cash_flow('F')
        expected_toplvl_keys = ['symbol', 'annualReports', 'quarterlyReports']
        self.assertCountEqual(expected_toplvl_keys, result_json.keys())

    def test_query_vwap(self):
        result_json = self.avi.query_vwap('F')
        expected_toplvl_keys = ['Meta Data', 'Technical Analysis: VWAP']
        self.assertCountEqual(expected_toplvl_keys, result_json.keys())

    def test_query_rsi(self):
        result_json = self.avi.query_rsi('F')
        expected_toplvl_keys = ['Meta Data', 'Technical Analysis: RSI']
        self.assertCountEqual(expected_toplvl_keys, result_json.keys())

    def test_query_cpi(self):
        result_json = self.avi.query_cpi()
        expected_toplvl_keys = ['name', 'interval', 'unit', 'data']
        self.assertCountEqual(expected_toplvl_keys, result_json.keys())
