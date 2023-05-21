import os
from kafka import KafkaConsumer
from Harvester.push_integration.db import models as m
import Harvester.schema_enforcement as s
import sqlalchemy as sa
from time import sleep
import argparse
import logging
from marshmallow import EXCLUDE


def consume_kafka_message():
    pass


def push_to_sqlalchemy(data, cls):
    db_uri = os.environ.get("DATABASE_URI")
    engine = sa.create_engine(db_uri)
    cls.bulk_upsert(data, engine)


if __name__ == "__main__":
    """
    Take user config from terminal
        - collect data from target source(s) in a loop
        - serialize data w/ Marshmallow
        - push to target endpoints
    TODO:
        - create volume for log??
    """

    parser = argparse.ArgumentParser(description='''
    Harvest market data from an endpoint
    ''', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-t', '--tickers', help='the ticker symbol(s) to get information for', type=str,  nargs='+', required=True)
    parser.add_argument('-r', '--refresh_time', help='time in seconds to wait between data refreshes. Default: 21600', type=int, default=21600)
    parser.add_argument('-d', '--data_type', help='the type of data to collect.', default='stock', choices=['stock', 'options', 'crypto', 'dix'])
    parser.add_argument('-l', '--log_file', help='the file to write logs to', default='harvester.log')
    # TODO: add ingress and egress args
    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(filename=args.log_file, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    # TODO: pull messages from kafka topic, post to SQLDB
