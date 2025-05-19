import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.load import *


class TestSaveFunctions(unittest.TestCase):

    def setUp(self):

        self.df = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
        self.empty_df = pd.DataFrame()
    
    def test_save_to_csv_final_success(self):
        with patch.object(self.df, 'to_csv') as mock_to_csv:
            save_to_csv_final(self.df)
            mock_to_csv.assert_called_once_with('scraped_data_transformed.csv', index=False)

    def test_save_to_csv_final_empty_df_raises(self):
        with self.assertRaises(DataEmpty):
            save_to_csv_final(self.empty_df)

    def test_save_to_csv_final_to_csv_raises_exception(self):
        with patch.object(self.df, 'to_csv', side_effect=Exception('Disk full')):
            with patch('builtins.print') as mock_print:
                save_to_csv_final(self.df)
                mock_print.assert_called_with('An error occured:Disk full')

    @patch('utils.load.create_engine')  
    def test_save_to_postgre_sql_success(self, mock_create_engine):
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine
        with patch.object(self.df, 'to_sql') as mock_to_sql:
            save_to_postgre_sql(self.df)
            mock_create_engine.assert_called_once()
            mock_to_sql.assert_called_once_with('products', mock_engine, if_exists='replace', index=False)

    def test_save_to_postgre_sql_empty_df_raises(self):
        with self.assertRaises(DataEmpty):
            save_to_postgre_sql(self.empty_df)

    @patch('utils.load.create_engine')  
    def test_save_to_postgre_sql_to_sql_raises_exception(self, mock_create_engine):
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine
        with patch.object(self.df, 'to_sql', side_effect=Exception('DB connection error')):
            with patch('builtins.print') as mock_print:
                save_to_postgre_sql(self.df)
                mock_print.assert_called_with('An error occured:DB connection error')

if __name__ == '__main__':
    unittest.main()
