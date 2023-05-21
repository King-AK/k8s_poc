import os
from Ingestor.push_integration.db import models as m
import Ingestor.schema_enforcement as s
import sqlalchemy as sa
import argparse
import logging
import sys
from marshmallow import EXCLUDE
from kafka import KafkaConsumer


def push_to_sqlalchemy(data, cls):
    db_uri = os.environ.get("DATABASE_URI")
    engine = sa.create_engine(db_uri)
    cls.bulk_upsert(data, engine)


if __name__ == "__main__":
    """
    Take user config from terminal
        - Read data from Kafka topic
        - deserialize data w/ Marshmallow
        - Ingest to database
    """

    parser = argparse.ArgumentParser(description='''
    Consume market data from Kafka topics
    ''', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-t', '--topic', help='the topic to pull data from.', default='stock', choices=['stock', 'options', 'crypto', 'dix'])
    parser.add_argument('-l', '--log_file', help='the file to write logs to', default='ingestor.log')
    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.StreamHandler(sys.stdout)])
    logger = logging.getLogger(f"INGESTOR:{__name__}")

    # Establish mappings for topics
    topic_model_mappings = {"stock": m.StockTimeSeries, "options": m.OptionsTimeSeries,
                            "crypto": m.CryptoTimeSeries, "dix": m.DIXTimeSeries}

    # Establish deserializers
    deserializers = {"stock": lambda d: s.StockTimeSeriesSchema().loads(d.decode('utf-8'), many=True),
                     "crypto": lambda d: s.CryptoTimeSeriesSchema().loads(d.decode('utf-8'), many=True, unknown=EXCLUDE),
                     "options": lambda d: s.YahooStockOptionsSchema().loads(d.decode('utf-8'), many=True),
                     "dix": lambda d: s.DIXSchema().loads(d.decode('utf-8'), many=True)
                     }  # TODO: check that we are using the correct deserializers here

    # Establish Consumer
    consumer = KafkaConsumer(args.topic,
                             bootstrap_servers=os.environ.get("KAFKA_BOOTSTRAP_SERVERS"),
                             value_deserializer=deserializers[args.topic])
    # TODO: figure out if there is a way to discard/ignore messages which dont pass the deserializer
    for message in consumer:
        try:
            push_to_sqlalchemy(message.value, topic_model_mappings[args.topic])
        except Exception as e:
            logger.exception(e)
