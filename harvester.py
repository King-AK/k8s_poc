import os
from Harvester.pull_integration.external_apis.alpha_vantage import AlphaVantageAPI
from Harvester.pull_integration.external_apis.yahoo_finance import YahooFinanceAPI
from Harvester.pull_integration.custom_utilities.dix_scraper import DIXScraper
from Harvester.push_integration.db import models as m
import Harvester.schema_enforcement as s
from time import sleep
import argparse
import logging
import sys
from marshmallow import EXCLUDE
from kafka import KafkaProducer
import json


def pull_alphavantage_stock_data(ticker, time_series_key='Time Series (60min)'):
    sleep(1)
    api_key = os.environ.get("ALPHAVANTAGE_API_KEY")
    avi = AlphaVantageAPI(api_key)
    # NOTE: using full, but should use compact after initial data is pulled
    data = avi.query_market_time_series_intraday(ticker, outputsize='full')
    data = s.AlphaVantageStockTimeSeriesSchema.clean_time_series_dictionary_list(data[time_series_key], ticker)
    return s.AlphaVantageStockTimeSeriesSchema().load(data, many=True)


def pull_alphavantage_crypto_data(ticker, time_series_key='Time Series Crypto (60min)'):
    sleep(1)
    api_key = os.environ.get("ALPHAVANTAGE_API_KEY")
    avi = AlphaVantageAPI(api_key)
    # NOTE: using full, but should use compact after initial data is pulled
    data = avi.query_crypto_intraday_time_series(ticker, outputsize='full')
    data = s.AlphaVantageStockTimeSeriesSchema.clean_time_series_dictionary_list(data[time_series_key], ticker)
    return s.AlphaVantageUSDCryptoTimeSeriesIntradaySchema().load(data, many=True, unknown=EXCLUDE)


def pull_yahoo_options_data(ticker):
    yf = YahooFinanceAPI()
    data = yf.get_options(ticker)
    return s.YahooStockOptionsSchema().load(data, many=True)


def pull_dix_data(ticker='INX'):
    dix = DIXScraper()
    data = dix.download_dix_sp500_data()
    return s.DIXSchema().load(data, many=True)


if __name__ == "__main__":
    """
    Take user config from terminal
        - collect data from target source(s) in a loop
        - serialize data w/ Marshmallow
        - push to event topic
    """

    parser = argparse.ArgumentParser(description='''
    Harvest market data from an endpoint
    ''', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-t', '--tickers', help='the ticker symbol(s) to get information for', type=str,  nargs='+', required=True)
    parser.add_argument('-r', '--refresh_time', help='time in seconds to wait between data refreshes. Default: 21600', type=int, default=21600)
    parser.add_argument('-d', '--data_type', help='the type of data to collect.', default='stock', choices=['stock', 'options', 'crypto', 'dix'])
    parser.add_argument('-l', '--log_file', help='the file to write logs to', default='harvester.log')
    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.StreamHandler(sys.stdout)])
    logger = logging.getLogger(f"HARVESTER:{__name__}")

    # For now just stick with SQLAlchemy/Postgres and various ingress endpoints. Save more complex function mixes for Scala.
    ingress_endpoints = {"alpha_vantage_stocks": pull_alphavantage_stock_data, "yf_options": pull_yahoo_options_data,
                         "alpha_vantage_crypto": pull_alphavantage_crypto_data, "dix": pull_dix_data}
    data_type = {"stock_time_series": m.StockTimeSeries, "options_time_series": m.OptionsTimeSeries,
                 "crypto_time_series": m.CryptoTimeSeries, "dix_time_series": m.DIXTimeSeries}  # TODO: create a pair for data to pull

    tickers = sorted(list(set(args.tickers)))
    
    logger.info(f"Ticker List: {tickers}")
    logger.info("Kafka Bootstrap Server: {}".format(os.environ.get("KAFKA_BOOTSTRAP_SERVERS")))

    # Establish Producer
    producer = KafkaProducer(bootstrap_servers=os.environ.get("KAFKA_BOOTSTRAP_SERVERS"),
                             value_serializer=lambda d: json.dumps(d, default=str).encode('utf-8'))

    while True:
        for ticker in tickers:
            try:
                if args.data_type == 'stock':
                    # Get stock data
                    data = ingress_endpoints["alpha_vantage_stocks"](ticker)
                elif args.data_type == 'crypto':
                    # Get crypto data
                    data = ingress_endpoints["alpha_vantage_crypto"](ticker)
                elif args.data_type == 'options':
                    # Get options data
                    data = ingress_endpoints["yf_options"](ticker)
                elif args.data_type == 'dix':
                    # Get dix data
                    data = ingress_endpoints["dix"](ticker='INX')  # NOTE: fixed for now, but maybe allow user spec for specific stocks in the future
                else:
                    raise ValueError("Invalid data_type request")
                logger.info(f"Collected [{args.data_type}] data for ${ticker}...")
                producer.send(args.data_type, value=data)
                logger.info(f"Sent [{args.data_type}] data for ${ticker} to broker...")
            except Exception as e:
                logger.info(f"Failed to collect/send [{args.data_type}] data for ${ticker}...")
                logger.exception(e)
        sleep(args.refresh_time)
