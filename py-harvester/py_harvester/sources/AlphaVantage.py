import json
from typing import Any
from urllib.parse import urlencode
from urllib.request import urlopen


class AlphaVantageAPI:
    """
    Fluent Interface for working with the AlphaVantage API.
    """

    def __init__(self) -> None:
        self.options = {"apikey": None, "dry_run": True}
        self.alpha_vantage_query_endpoint = "https://www.alphavantage.co/query?"
        self.global_mandatory_options = ["apikey", "dry_run"]

    def add(self, key: str, value: Any):
        self.options[key] = value
        return self

    def reset(self):
        self.options = {"apikey": None, "dry_run": True}
        return self

    def list_options(self) -> None:
        print(f"Options: {self.options}")

    def confirm_mandatory_options(self) -> None:
        for option in self.global_mandatory_options:
            if self.options.get(option) is None:
                raise ValueError(f"Option '{option}' is mandatory for this query.")

    def fetch(self, params: dict) -> dict or None:
        self.confirm_mandatory_options()
        params.update(self.options)
        url = f"{self.alpha_vantage_query_endpoint}{urlencode(params)}"
        if self.options.get("dry_run") is True:
            print(f"Query URL: {url}")
            return None
        try:
            response = urlopen(url)
        except Exception as e:
            print(f"Could not process query string: {url}")
            raise e
        return json.loads(response.read())

    def query_market_time_series_intraday(self, symbol, interval='60min', outputsize='full'):
        function = 'TIME_SERIES_INTRADAY'
        params = {'symbol': symbol, 'interval': interval, 'function': function, 'datatype': 'json',
                  'outputsize': outputsize}
        return self.fetch(params)
