import requests
from requests.exceptions import RequestException
import pandas as pd

from typing import Dict, Any
from src.utils.config import ALPHA_VANTAGE_API_KEY

class AlphaVantageAPI:
    '''
    Creates a new API object which gets financial data from 
    the Alpha Vantage website.
    '''

    def __init__(self, api_key=ALPHA_VANTAGE_API_KEY):
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query"
    
    def fetch_data(self, function: str, symbol: str, interval: str = None, outputsize: str = 'compact') -> Dict[str, Any]:
        """
        Fetches the specified data from the Alpha Vantage website.

        Args:
            function (str): Function to get data.
            symbol (str): Name of stock wanted.
            interval (str): Interval of time of stock price to retrieve apart from daily.
                e.g., '1min', '5min', '30min', '60min'.
            outputsize (str): Specifies the amount of data that the API should return.
                'compact' returns recent data while 'full' returns a comprehensive dataset.
        
        Returns:
            Dict[str, Any]: JSON response with the requested data.
        
        Raises:
            ValueError: If a connection cannot be made or server returns an error.
        """
        try:
            params = {
                "function": function,
                "symbol": symbol,
                "apikey": self.api_key,
                "outputsize": outputsize
            }

            if interval:
                params["interval"] = interval

            response = requests.get(self.base_url, params=params)
            response.raise_for_status()

            return response.json()
        except RequestException as err:
            raise ValueError(f"An error occurred while fetching data: {err}")
    
    def get_daily_stock_data(self, symbol: str) -> pd.DataFrame:
        """
        Fetches the daily data of a stock.

        Args:
            symbol: ticker name of stock.
        
        Returns:
            pd.DataFrame: DataFrame containing stock data.
        
        Raises:
            ValueError: 1. Data not found
                        2. Error while fetching data
                        3. Invalid symbol
        """
        try:
            data = self.fetch_data('TIME_SERIES_DAILY', symbol)
            if 'Time Series (Daily)' in data:
                return pd.DataFrame(data['Time Series (Daily)']).T
            else:
                raise ValueError("Data not found in the response.")
        except RequestException as err:
            raise ValueError(f"An error occurred while fetching data: {err}")
        except ValueError:
            raise ValueError("Invalid symbol please use a correct ticker symbol.")
    
    def get_weekly_stock_data(self, symbol: str) -> pd.DataFrame:
        """
        Fetches weekly data of a stock.

        Args:
            symbol: ticker name of stock.
        
        Returns:
            pd.DataFrame: DataFrame containing stock data.
        """
        try:
            data = self.fetch_data('TIME_SERIES_WEEKLY', symbol)
            if 'Weekly Time Series' in data:
                return pd.DataFrame(data['Weekly Time Series']).T
            else:
                raise ValueError("Data not found in the response.")
        except RequestException as err:
            raise ValueError(f"An error occurred while fetching data: {err}")
        except ValueError:
            raise ValueError("Invalid symbol please use a correct ticker symbol.")

    def get_monthly_stock_data(self, symbol: str) -> pd.DataFrame:
        """
        Fetches monthly data of a stock.

        Args:
            symbol: ticker name of stock.
        
        Returns:
            pd.DataFrame: DataFrame containing stock data.
        """
        try:
            data = self.fetch_data('TIME_SERIES_MONTHLY', symbol)
            if 'Monthly Time Series' in data:
                return pd.DataFrame(data['Monthly Time Series']).T
            else:
                raise ValueError("Data not found in the response.")
        except RequestException as err:
            raise ValueError(f"An error occurred while fetching data: {err}")
        except ValueError:
            raise ValueError("Invalid symbol please use a correct ticker symbol.")
        
