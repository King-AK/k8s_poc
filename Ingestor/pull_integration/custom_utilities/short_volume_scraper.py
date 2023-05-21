import requests
import csv
import json
import os
import zipfile
from io import BytesIO


class FINRAShortScraper:

    def __init__(self):
        self.work_dir = './wd_short_scraper'

    def get_daily_short_volume_data(self, date, market):
        """
        Downloads a daily short volume TXT file from FINRA
        http://regsho.finra.org/[Market]shvol[YYYYMMDD].txt

        Available Markets:
            * CNMS: FINRA Consolidated NMS
            * FNQC: FINRA/NASDAQ TRF Chicago
            * FNRA: ADF
            * FNSQ: FINRA/NASDAQ TRF Carteret
            * FNYX: FINRA/NYSE TRF
            * FORF: ORF

        e.g.
        http://regsho.finra.org/CNMSshvol20210209.txt

        `date` must be a valid market date in `YYYYMMDD` format
        """
        available_markets = ['CNMS', 'FNQC', 'FNRA', 'FNSQ', 'FNYX', 'FORF']
        if market not in available_markets:
            raise ValueError(f"Invalid market selected. Expected one of {available_markets}")

        target_url = f"http://regsho.finra.org/{market}shvol{date}.txt"
        response = requests.get(target_url)
        if response.status_code == 200:
            lines = (line.decode('utf8') for line in response.iter_lines())
            csv_reader = csv.DictReader(lines, delimiter="|")
            data = list(csv_reader)
            return data
        raise ValueError(f"ERROR: {response.status_code}: {response.reason}")

    def download_daily_short_volume_data(self, date, market, target_folder='.'):
        data = self.get_daily_short_volume_data(date, market)
        output_file = f"{target_folder}/{market}shvol{date}.json"
        json.dump(data, open(output_file, 'w'))

    def get_monthly_short_sale_transaction_data(self, date, market, chunk_size=128):
        """
        Downloads a monthly short sale transaction TXT file from FINRA
        http://regsho.finra.org/[Market]sh[YYYYMM].txt.zip

        Available Markets:
            * FNQC: FINRA/NASDAQ TRF Chicago
            * FNSQ: FINRA/NASDAQ TRF Carteret
            * FNYX: FINRA/NYSE TRF

        e.g.
        http://regsho.finra.org/FNSQsh202012.txt.zip

        `date` must be a valid market date in `YYYYMM` format

        Note that this function returns an iterator instead of a fully fleshed out list to avoid memory issues.
        """
        available_markets = ['FNQC', 'FNSQ', 'FNYX']
        if market not in available_markets:
            raise ValueError(f"Invalid market selected. Expected one of {available_markets}")

        target_url = f"http://regsho.finra.org/{market}sh{date}.txt.zip"
        response = requests.get(target_url, stream=True)
        if response.status_code == 200:
            # Specify and create the working directory
            os.makedirs(self.work_dir, exist_ok=True)

            # Collect the ZIP file and extract into the working directory
            z = zipfile.ZipFile(BytesIO(response.content))
            z.extractall(self.work_dir)

            # Read in the TXT file data, transform into JSON
            anticipated_filename = f"{self.work_dir}/{market}sh{date}.txt"
            csv_reader = csv.DictReader(open(anticipated_filename, 'r'), delimiter="|")
            data_stream = (row for row in csv_reader)
            return data_stream

        raise ValueError(f"ERROR: {response.status_code}: {response.reason}")


if __name__ == '__main__':
    '''
    This script aims to collect and download all FINRA daily short sale volume files within a specified range
    '''
    pass
