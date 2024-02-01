import os
import pandas as pd


class DataTransformer():
    """
    Carries out data cleaning processes on extracted data
    """
    generated_files = 0

    def __init__(self, dataframe: pd.DataFrame):
        self.dataframe = dataframe
        self.output_dir = 'testfiles'

    def clean_data(self) -> pd.DataFrame:
        """
        Cleans the data for analysis

        Args:
            None
        
        Returns:
            pd.DataFrame: cleaned data
        """
        df = self.dataframe.copy()
        df = df.reset_index()
    
        df['date'] = df['index']
        df['stock_price'] = df['4. close']
        
        df2 = df[['date', 'stock_price']].copy()
        df2['stock_price'] = df2['stock_price'].apply(lambda x: round(float(x), 2))
        df2['date'] = pd.to_datetime(df2['date'])

        self._save_to_csv(df2)

        return df2.copy()

    
    def _save_to_csv(self, dataframe: pd.DataFrame):
        """
        Saves data to csv file

        Args:
            dataframe: dataframe to save.
        
        Returns:
            None
        """
        self.generated_files += 1
        dataframe.to_csv(os.path.join(self.output_dir, f'sample_data_{self.generated_files}.csv'))