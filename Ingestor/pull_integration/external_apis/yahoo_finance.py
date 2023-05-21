from yahoo_fin import options
import argparse
from datetime import datetime
from time import sleep
import backoff
import logging


backoff_max_tries = 15


def retry(details):
    logging.info("Backing off {wait:0.1f} seconds after {tries} tries calling function {target}".format(**details))


class YahooFinanceAPI():
    """
    TODO: get more stock information beyond options
    """
    @backoff.on_exception(backoff.expo, Exception, max_tries=backoff_max_tries,
                          on_backoff=retry, jitter=backoff.full_jitter)
    def get_options_chain(self, ticker, date):
        option_data = []
        fetch_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        raw_options_data = options.get_options_chain(ticker, date)
        for option_type in ["calls", "puts"]:
            data = raw_options_data[option_type].to_dict(orient="records")
            expiration_dt = datetime.strptime(date, '%B %d, %Y').strftime('%Y-%m-%d 16:00:00')
            for row in data:
                row['symbol'] = ticker
                row['expiration_date'] = expiration_dt
                row['option_type'] = option_type
                row['datetime'] = fetch_time
            option_data += data
        return option_data

    @backoff.on_exception(backoff.expo, Exception, max_tries=3,
                          on_backoff=retry, jitter=backoff.full_jitter)
    def get_options(self, ticker):
        """
        Pull and restructure options data to get full chains and supplement additional data
        """
        options_data = []
        expiration_dates = options.get_expiration_dates(ticker)
        for date in expiration_dates:
            options_data += self.get_options_chain(ticker, date)
            sleep(1.8)
        return options_data


if __name__ == '__main__':
    # Read in available arguments
    parser = argparse.ArgumentParser(description='''
    Pull data for a list of stocks using yahoo-fin
    ''', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-s', '--symbols', help='the symbol(s) to get Yahoo Finance information for ', type=str, required=True)
    args = parser.parse_args()

    # TODO: Define logic for using the class in a standalone fashion below
    # client = YahooFinanceAPI()
    # client.summarize(args.symbols)
