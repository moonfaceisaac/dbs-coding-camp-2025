import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.transform import *


class TestTransformDataAllInOne(unittest.TestCase):

    @patch('pandas.read_csv')
    def test_raises_DataEmpty_for_empty_dataframe(self, mock_read_csv):
        mock_read_csv.return_value = pd.DataFrame()
        with self.assertRaises(DataEmpty):
            transform_data_all_in_one()

    @patch('pandas.read_csv')
    def test_basic_transformation(self, mock_read_csv):
        # Setup mock dataframe
        mock_read_csv.return_value = pd.DataFrame({
            'Product Name': ['Product A', 'Unknown Product', 'Product B'],
            'Price': ['$10.00', 'Price Unavailable', '$20.00'],
            'Rating': ['4.5 stars', '3.0 stars', '5.0 stars'],
            'Colors': ['3 colors', '2 colors', '5 colors'],
            'Size': ['Size: M', 'Size: L', 'Size: S'],
            'Gender': ['Gender: Male', 'Gender: Female', 'Gender: Unisex'],
            'Timestamp': [
            '2025-05-18 10:00:00',
            '2025-05-18 11:00:00',
            '2025-05-18 12:00:00'
        ]
        })

        result_df = transform_data_all_in_one()

        # Check apakah invalid value memang telah dihapus
        self.assertNotIn('Unknown Product', result_df['Product Name'].values)
        self.assertNotIn('Price Unavailable', result_df['Price'].astype(str).values)

        # Check konversi price ke IDR
        self.assertAlmostEqual(result_df.loc[result_df['Product Name']=='Product A', 'Price'].values[0], 160000)
        self.assertAlmostEqual(result_df.loc[result_df['Product Name']=='Product B', 'Price'].values[0], 320000)

        # Check kolom rating float
        self.assertTrue(pd.api.types.is_float_dtype(result_df['Rating']))

        # Check kolom color tipe data int
        self.assertTrue(pd.api.types.is_integer_dtype(result_df['Colors']))

        # Check pembersihan size
        self.assertTrue(all(size in ['M', 'S'] for size in result_df['Size']))

        # Check pembersihan gender
        self.assertTrue(all(g in ['Male', 'Unisex'] for g in result_df['Gender']))

    @patch('pandas.read_csv')
    def test_exception_handling(self, mock_read_csv):
        # Buat read_Csv mengembalikan datafram yang akan menimbulkan error (kolom price dan timestamp tidak ada)
        mock_read_csv.return_value = pd.DataFrame({
            'Product Name': ['Product A'],
            'Rating': ['4.5 stars'],
            'Colors': ['3 colors'],
            'Size': ['Size: M'],
            'Gender': ['Gender: Male']
        })

        with patch('builtins.print') as mock_print:
            result_df = transform_data_all_in_one()
            printed_args = [call.args[0] for call in mock_print.call_args_list]
            error_msgs = [msg for msg in printed_args if 'An error has occured:' in msg]
            self.assertTrue(any(error_msgs))


if __name__ == '__main__':
    unittest.main()
