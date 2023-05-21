import requests
import csv


class DIXScraper:

    def __init__(self):
        pass

    def download_dix_sp500_data(self):
        """
        Downloads market DIX/GEX data from
        https://squeezemetrics.com/monitor/static/DIX.csv
        """
        target_url = "https://squeezemetrics.com/monitor/static/DIX.csv"
        response = requests.get(target_url)
        if response.status_code == 200:
            lines = (line.decode('utf8') for line in response.iter_lines())
            csv_reader = csv.DictReader(lines, delimiter=",")
            data = list(csv_reader)
            for row in data:
                row['symbol'] = 'INX'
            return data
        raise ValueError(f"ERROR: {response.status_code}: {response.reason}")


if __name__ == '__main__':
    '''
    This script aims to collect DIX data
    '''
    data = DIXScraper().download_dix_data()
    print(data)
