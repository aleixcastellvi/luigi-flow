# -*- coding: utf-8 -*-

import config
import luigi
import json
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


class APIDataFetcherTask(luigi.Task):

    def requires(self):
        pass

    def run(self):
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

        parameters = {
            'start': '1',
            'limit': '5000',
            'convert': 'USD'
        }

        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': config.API_KEY,
        }

        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            print(data)
        
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)

    def output(self):
        pass

if __name__ == '__main__':
    luigi.run()


# Run locally: python api_data_fetcher_task.py APIDataFetcherTask --local-scheduler