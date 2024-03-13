# -*- coding: utf-8 -*-

import config
import luigi
import json
import pandas as pd
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

            raw_data = json.loads(response.text)

            df = pd.json_normalize(raw_data['data'])

            selected_df = df[['cmc_rank', 'name', 'symbol', 'quote.USD.price', 'date_added']]

            renamed_df = selected_df.rename(columns = {'cmc_rank': 'Ranking', 
                                                       'name':'Coin', 
                                                       'symbol': 'Crypto ID', 
                                                       'quote.USD.price':'Price', 
                                                       'date_added':'Released'})

            renamed_df['Price'] = renamed_df['Price'].apply(lambda x: self.formatted_value(x))

            print(renamed_df)

        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)

    def output(self):
        pass

    def formatted_value(self, value):
        split_price = str(value).split(".")[1]
        if int(value) == 0 and split_price[:2] == "00":
            return str(round(value, 4)).replace(".", ",")
        else:
            return self.thousands_values(value)

    def thousands_values(self, value):
        formated_val = "{:,.2f}".format(value)
        integer, decimals = formated_val.split(".")
        integer = integer.replace(",", ".")

        return f"{integer},{decimals}"


if __name__ == '__main__':
    luigi.run()


# Run locally: python api_data_fetcher_task.py APIDataFetcherTask --local-scheduler