import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from unittest.mock import patch, Mock
from utils.extract import scrape_items_from_site_url, items_data
from datetime import datetime


class TestScraper(unittest.TestCase):

    @patch('utils.extract.open', new_callable=unittest.mock.mock_open)
    @patch('utils.extract.requests.get')  # Patch berdasarkan lokasi modul
    def test_scrape_single_page(self, mock_get, mock_open_file):
        # Mock HTML 
        mock_html = '''
        <div class="collection-card">
            <h3 class="product-title">Mock Shirt</h3>
            <span class="price">$19.99</span>
            <p>4.5 Stars</p>
            <p>Red, Blue</p>
            <p>M</p>
            <p>Unisex</p>
        </div>
        '''
        mock_response = Mock()
        mock_response.text = mock_html
        mock_get.return_value = mock_response

    

        scrape_items_from_site_url(1)

        self.assertEqual(len(items_data), 1)
        self.assertEqual(items_data[0][0], "Mock Shirt")
        self.assertEqual(items_data[0][1], "$19.99")
        self.assertEqual(items_data[0][2], "4.5 Stars")
        self.assertEqual(items_data[0][3], "Red, Blue")
        self.assertEqual(items_data[0][4], "M")
        self.assertEqual(items_data[0][5], "Unisex")
        self.assertTrue(isinstance(items_data[0][6], datetime)) 

        handle = mock_open_file()
        handle.write.assert_called()  # Mengkonfirmasi file telah dicoba untuk di written
if __name__ == '__main__':
    unittest.main()
