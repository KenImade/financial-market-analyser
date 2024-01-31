import sys
import unittest
import json
import pandas as pd
from unittest.mock import patch
from pathlib import Path

root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from src.api.alpha_vantage import AlphaVantageAPI

class TestAlphaVantageAPI(unittest.TestCase):

    def setUp(self):
        self.api = AlphaVantageAPI(api_key='T8NPRZVP5SXGO4XS')
    
    @patch('requests.get')
    def test_fetch_data(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = json.loads('{"sample_key": "sample_value"}')

        response = self.api.fetch_data('TIME_SERIES_DAILY', 'IBM')
        self.assertEqual(response, {"sample_key": "sample_value"})

    def test_get_daily_stock_data(self):
        symbol = "AAPL"
        result_df = self.api.get_daily_stock_data(symbol)
        self.assertIsInstance(result_df, pd.DataFrame)
    
    def test_get_weekly_stock_data(self):
        symbol = "IBM"
        result_df = self.api.get_weekly_stock_data(symbol)
        self.assertIsInstance(result_df, pd.DataFrame)
    
    def test_get_monthly_stock_data(self):
        symbol = "IBM"
        result_df = self.api.get_monthly_stock_data(symbol)
        self.assertIsInstance(result_df, pd.DataFrame)

    def test_invalid_symbol(self):
        invalid_symbol = "INVALID"
        with self.assertRaises(ValueError) as context:
            self.api.get_daily_stock_data(invalid_symbol)
        self.assertIn("Invalid symbol please use a correct ticker symbol.", str(context.exception))



if __name__ == "__main__":
    unittest.main()