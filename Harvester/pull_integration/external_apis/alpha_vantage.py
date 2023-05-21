'''
Interface with the AlphaVantage API.
Pull JSON data (TODO: optionally directly save direct JSON copies for Spark streaming at some point in future - though may be better for a different dataset)
Wrangle JSON data using Marshmallow, push into the Postgres database.
'''
from urllib.parse import urlencode
from urllib.request import urlopen
import json
import argparse


class AlphaVantageAPI():
    """
    Establish a connection to the AlphaVantage API

    TODO: set up some API query baseline and make this more modular for future endpoints. Import from some base class for marshalling
    """

    def __init__(self, api_key):
        self.api_query_header = "https://www.alphavantage.co/query?"
        self.api_key = api_key

    def query_market_time_series_intraday(self, symbol, interval='60min', outputsize='full'):
        """
            Establish a connection to the AlphaVantage API and query for intraday market data of a particular stock based on its symbol.

            interval: May be one of ('1min', '5min', '15min', '30min', '60min')
            outputsize: either 'compact' or 'full'
        """
        query_params = {'symbol': symbol, 'apikey': self.api_key, 'interval': interval, 'function': 'TIME_SERIES_INTRADAY',
                        'datatype': 'json', 'outputsize': outputsize}
        query_url = f"{self.api_query_header}{urlencode(query_params)}"

        try:
            response = urlopen(query_url).read().decode('utf8')
        except Exception as e:
            print(f"Could not process query string: {query_url}")
            raise e
        return json.loads(response)

    def query_market_time_series(self, symbol, function='TIME_SERIES_DAILY', outputsize='compact'):
        """
            Establish a connection to the AlphaVantage API and query for market data of a particular stock based on its symbol.

            `function`: May be one of (`TIME_SERIES_DAILY`, `TIME_SERIES_DAILY_ADJUSTED`, `TIME_SERIES_WEEKLY`, `TIME_SERIES_WEEKLY_ADJUSTED`,
                                       `TIME_SERIES_MONTHLY`, `TIME_SERIES_MONTHLY_ADJUSTED` )

            `outputsize`: either `compact` or `full`
        """
        query_params = {'symbol': symbol, 'apikey': self.api_key, 'function': function,
                        'datatype': 'json', 'outputsize': outputsize}
        query_url = f"{self.api_query_header}{urlencode(query_params)}"
        try:
            response = urlopen(query_url).read().decode('utf8')
        except Exception as e:
            print(f"Could not process query string: {query_url}")
            raise e
        return json.loads(response)

    def query_crypto_intraday_time_series(self, symbol, function='CRYPTO_INTRADAY', market='USD', interval='60min', outputsize='full'):
        """
            Establish a connection to the AlphaVantage API and query for market data of a particular stock based on its symbol.

            `function`: May be one of (`CRYPTO_INTRADAY`)

            `market`: any currency exchange rate provided by AlphaVantage. Defaults to `USD`
        """
        query_params = {'symbol': symbol, 'apikey': self.api_key, 'function': function, 'outputsize': outputsize,
                        'datatype': 'json', 'market': market, 'interval': interval}
        query_url = f"{self.api_query_header}{urlencode(query_params)}"
        try:
            response = urlopen(query_url).read().decode('utf8')
        except Exception as e:
            print(f"Could not process query string: {query_url}")
            raise e
        return json.loads(response)

    def query_crypto_time_series(self, symbol, function='DIGITAL_CURRENCY_DAILY', market='USD'):
        """
            Establish a connection to the AlphaVantage API and query for market data of a particular stock based on its symbol.

            `function`: May be one of (`DIGITAL_CURRENCY_DAILY`, `DIGITAL_CURRENCY_WEEKLY`, `DIGITAL_CURRENCY_MONTHLY`)

            `market`: any currency exchange rate provided by AlphaVantage. Defaults to `USD`
        """
        query_params = {'symbol': symbol, 'apikey': self.api_key, 'function': function,
                        'datatype': 'json', 'market': market}
        query_url = f"{self.api_query_header}{urlencode(query_params)}"
        try:
            response = urlopen(query_url).read().decode('utf8')
        except Exception as e:
            print(f"Could not process query string: {query_url}")
            raise e
        return json.loads(response)

    def query_fundamental_data(self, symbol, function):
        """
            Establish a connection to the AlphaVantage API and query for Company Overview data of a particular stock based on its symbol.
        """
        query_params = {'symbol': symbol, 'apikey': self.api_key, 'function': function}
        query_url = f"{self.api_query_header}{urlencode(query_params)}"
        try:
            response = urlopen(query_url).read().decode('utf8')
        except Exception as e:
            print(f"Could not process query string: {query_url}")
            raise e
        return json.loads(response)

    def query_company_overview(self, symbol):
        """
            Establish a connection to the AlphaVantage API and query for Company Overview data of a particular stock based on its symbol.
        """
        return self.query_fundamental_data(symbol, 'OVERVIEW')

    def query_income_statement(self, symbol):
        """
            Establish a connection to the AlphaVantage API and query for Income Statement data of a particular stock based on its symbol.
        """
        return self.query_fundamental_data(symbol, 'INCOME_STATEMENT')

    def query_balance_sheet(self, symbol):
        """
            Establish a connection to the AlphaVantage API and query for Income Statement data of a particular stock based on its symbol.
        """
        return self.query_fundamental_data(symbol, 'BALANCE_SHEET')

    def query_cash_flow(self, symbol):
        """
            Establish a connection to the AlphaVantage API and query for Income Statement data of a particular stock based on its symbol.
        """
        return self.query_fundamental_data(symbol, 'CASH_FLOW')

    def query_vwap(self, symbol, interval='60min'):
        """
            Establish a connection to the AlphaVantage API and query for intraday vwap data of a particular stock based on its symbol.

            interval: May be one of ('1min', '5min', '15min', '30min', '60min')
            outputsize: either 'compact' or 'full'
        """
        query_params = {'symbol': symbol, 'apikey': self.api_key, 'interval': interval, 'function': 'VWAP',
                        'datatype': 'json'}
        query_url = f"{self.api_query_header}{urlencode(query_params)}"

        try:
            response = urlopen(query_url).read().decode('utf8')
        except Exception as e:
            print(f"Could not process query string: {query_url}")
            raise e
        return json.loads(response)

    def query_rsi(self, symbol, interval='60min', time_period='420', series_type='low'):
        """
            Establish a connection to the AlphaVantage API and query for rsi data of a particular stock based on its symbol.

            interval: May be one of ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly')
            time_period: xxx
            series_type: xxx
            outputsize: either 'compact' or 'full'
        """
        query_params = {'symbol': symbol, 'apikey': self.api_key, 'interval': interval, 'function': 'RSI',
                        'datatype': 'json', 'time_period': time_period, 'series_type': series_type}
        query_url = f"{self.api_query_header}{urlencode(query_params)}"

        try:
            response = urlopen(query_url).read().decode('utf8')
        except Exception as e:
            print(f"Could not process query string: {query_url}")
            raise e
        return json.loads(response)

    def query_cpi(self, interval='monthly'):
        """
            Establish a connection to the AlphaVantage API and query for cpi data.

            interval: May be one of ('monthly', 'semiannual')
            time_period: xxx
            series_type: xxx
            outputsize: either 'compact' or 'full'
        """
        query_params = {'apikey': self.api_key, 'interval': interval, 'function': 'CPI',
                        'datatype': 'json'}
        query_url = f"{self.api_query_header}{urlencode(query_params)}"

        try:
            response = urlopen(query_url).read().decode('utf8')
        except Exception as e:
            print(f"Could not process query string: {query_url}")
            raise e
        return json.loads(response)

    '''TODO:
    * Unemployment
    * Nonfarm payroll
    * Durables
    * Retail Sales
    * Federal Funds Rate
    * Treasury Yield
    '''


if __name__ == '__main__':
    """ TODO: flesh out main to read in a list of tickers and dump json files to specified output directory
        Should be useful for future applications.
    """
    parser = argparse.ArgumentParser(description='''
    Pull data for a list of stocks with AlphaVantage...
    ''', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-s', '--symbol', help='the symbol(s) to get Yahoo Finance information for', type=str, required=True)
    parser.add_argument('-k', '--api_key', help='AlphaVantage API key', type=str, required=True)
    args = parser.parse_args()

    # TODO: Define more complex logic for using the class in a standalone fashion below.
    client = AlphaVantageAPI(api_key=args.api_key)
    client.query_market_time_series(args.symbol)
