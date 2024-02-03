import unittest
import pandas as pd

from src.core.data_processing import DataTransformer

class TestDataTransformer(unittest.TestCase):

    def setUp(self):
        self.data = pd.DataFrame({
            'index': ['2023-01-01', '2023-01-02'],
            '1. open': ['100.123', '200.421'],
            '2. high': ['101.234', '203.421'],
            '3. low': ['100.100', '200.100'],
            '4. close': ['100.123', '200.456'],
            '5. volume': ['89318051', '118990164']
        })
        self.transformer = DataTransformer(self.data)
    
    def test_clean_data(self):
        cleaned_data = self.transformer.clean_data()
        # check if column names are correct
        self.assertListEqual(['date', 'stock_price'], list(cleaned_data.columns))
        # Check data types
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(cleaned_data['date']))
        self.assertTrue(pd.api.types.is_float_dtype(cleaned_data['stock_price']))
        # Check values are as expected
        self.assertEqual(cleaned_data.iloc[0]['stock_price'], 100.12)
    
if __name__ == '__main__':
    unittest.main()