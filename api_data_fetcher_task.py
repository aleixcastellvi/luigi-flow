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
            'limit': config.LIMIT_VALUES,
            'convert': config.CURRENCY
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

        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)

        df = pd.json_normalize(raw_data['data'])

        selected_df = df[['name', 'symbol', 'quote.USD.price', 'date_added']]

        renamed_df = selected_df.rename(columns = {
            'name': 'coin', 
            'symbol': 'id', 
            'quote.USD.price': 'price', 
            'date_added': 'released'})
        
        # The cost value is sorted from highest to lowest
        crypto_df = renamed_df.sort_values(by=['price'], ascending=False)

        # New column to define a coin ranking from highest to lowest cost value
        crypto_df['rank'] = range(1, len(crypto_df) + 1)

        # New format to display the price of each coin
        crypto_df['price'] = crypto_df['price'].apply(lambda x: self.formatted_price(x))

        # New format to display the release date of each coin
        crypto_df['released'] = pd.to_datetime(crypto_df['released'])
        crypto_df['released'] = crypto_df['released'].dt.strftime('%d-%m-%Y')

        # Reorganization of the columns
        rank_column = crypto_df.columns[-1]
        other_columns = crypto_df.columns[:-1]
        order_columns = [rank_column] + list(other_columns)

        top_crypto_df = crypto_df[order_columns]

        # Generate CSV file in the specified directory
        top_crypto_df.to_csv(config.OUTPUT_DIR, index=False)

    def output(self):
        return luigi.LocalTarget(config.OUTPUT_DIR)

    def formatted_price(self, value):
        """
        This function formats the given price value.

        Args:
            value (float or int): The price value to be formatted.

        Returns:
            str: The formatted price.
        """
        split_price = str(value).split(".")[1]
        if int(value) == 0 and split_price[:2] == "00":
            return str(round(value, 4)).replace(".", ",")
        else:
            return self.thousands_values(value)

    def thousands_values(self, value):
        """
        Formats a numerical value with thousands separator.

        Args:
            value (float or int): The numerical value to be formatted.

        Returns:
            str: The formatted value with thousands separator.
        """
        formated_val = "{:,.2f}".format(value)
        integer, decimals = formated_val.split(".")
        integer = integer.replace(",", ".")

        return f"{integer},{decimals}"


if __name__ == '__main__':
    luigi.run()


# Run locally: python api_data_fetcher_task.py APIDataFetcherTask --local-scheduler