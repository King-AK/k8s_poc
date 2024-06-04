import argparse
import json
import logging
import os
import sys

from kafka import KafkaProducer

from py_harvester.marshmallowSchemas.AlphaVantageSchema import AlphaVantageStockTimeSeriesSchema
from py_harvester.sources.AlphaVantage import AlphaVantageAPI


def build_logger(name: str) -> logging.Logger:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[logging.StreamHandler(sys.stdout)])
    return logging.getLogger(name)


def harvest_stock_data(producer: KafkaProducer, symbols: list, av: AlphaVantageAPI) -> None:
    # Get data for each symbol
    for symbol in symbols:
        data = av.query_market_time_series_intraday(symbol)
        time_series_key = 'Time Series (60min)'
        cleaned_data = AlphaVantageStockTimeSeriesSchema.clean_time_series_dictionary_list(data[time_series_key],
                                                                                           symbol)
        cleaned_data = AlphaVantageStockTimeSeriesSchema().load(cleaned_data, many=True)
        print(cleaned_data)

        logger.info(f"Collected [{args.data_type}] data for ${symbol}...")
        for data in cleaned_data:
            producer.send("stock-time-series", value=data)
        logger.info(f"Sent [{args.data_type}] data for ${symbol} to broker...")

        producer.flush()


if __name__ == '__main__':
    logger = build_logger("HARVESTER")

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--symbols", help="the list of symbols to get data for", type=str, required=True)
    parser.add_argument("-k", "--api_key", help="the AlphaVantage API key", type=str)
    args = parser.parse_args()

    api_key = args.api_key
    symbols = args.symbols.split(",")

    av: AlphaVantageAPI = (AlphaVantageAPI()
                           .add("apikey", api_key)
                           .add("dry_run", False))

    # Establish Kafka producer
    producer = KafkaProducer(bootstrap_servers=os.environ.get("KAFKA_BOOTSTRAP_SERVERS"),
                             value_serializer=lambda d: json.dumps(d, default=str).encode('utf-8'))

    harvest_stock_data(producer, symbols, av)
