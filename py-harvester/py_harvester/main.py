import argparse
import json
import logging
import os
import sys
from time import sleep
from kafka import KafkaProducer

from py_harvester.marshmallowSchemas.AlphaVantageSchema import AlphaVantageStockTimeSeriesSchema
from py_harvester.sources.AlphaVantage import AlphaVantageAPI


def build_logger(name: str, level=logging.INFO) -> logging.Logger:
    logging.basicConfig(level=level, format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[logging.StreamHandler(sys.stdout)])
    return logging.getLogger(name)


def harvest_stock_data(producer: KafkaProducer, symbols: list, av: AlphaVantageAPI) -> None:
    for symbol in symbols:
        logger.info(f"Collecting stock data for ${symbol}...")
        data = av.query_market_time_series_intraday(symbol)
        time_series_key = 'Time Series (60min)'
        cleaned_data = AlphaVantageStockTimeSeriesSchema.clean_time_series_dictionary_list(data[time_series_key],
                                                                                           symbol)
        cleaned_data = AlphaVantageStockTimeSeriesSchema().load(cleaned_data, many=True)
        logger.info(f"Collected stock data for ${symbol}...")
        logger.debug(f"Data: {cleaned_data}")
        for data in cleaned_data:
            producer.send("stock-time-series", value=data)
        logger.info(f"Sent stock data for ${symbol} to broker...")

        producer.flush()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--symbols", help="the list of symbols to get data for", type=str, required=True)
    parser.add_argument("-k", "--api_key", help="the AlphaVantage API key", type=str)
    parser.add_argument("-b", "--kafka_bootstrap_servers", help="the Kafka bootstrap servers", type=str)
    parser.add_argument("-z", "--sleep_interval", help="the sleep interval between queries in seconds", type=int, default=300)
    parser.add_argument("-l", "--log_level", help="the log level", type=str, default="INFO", choices=["DEBUG", "INFO"])
    args = parser.parse_args()

    log_level = logging.getLevelName(args.log_level)
    logger = build_logger("py_harvester", level=args.log_level)

    api_key = args.api_key
    symbols = args.symbols.split(",")

    av: AlphaVantageAPI = (AlphaVantageAPI()
                           .add("apikey", api_key)
                           .add("dry_run", False))

    # Establish Kafka producer
    producer = KafkaProducer(bootstrap_servers=args.kafka_bootstrap_servers,
                             value_serializer=lambda d: json.dumps(d, default=str).encode('utf-8'))

    while True:
        harvest_stock_data(producer, symbols, av)
        logger.info(f"Sleeping for {args.sleep_interval} seconds...")
        sleep(args.sleep_interval)
