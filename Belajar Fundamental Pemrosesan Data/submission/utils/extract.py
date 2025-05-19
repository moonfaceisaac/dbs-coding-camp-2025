import requests
from bs4 import BeautifulSoup
import csv
import time
from datetime import datetime


headers = {'User-Agent': 'Mozilla/5.0'}
items_data = []

def parse_item_block(block): #Function ngambil per tag <p> dari blok
    title_find = block.find('h3', class_='product-title')
    title = title_find.get_text(strip=True) if title_find else 'Unknown'
    price_find = block.find('span', class_='price')
    price = price_find.get_text(strip=True) if price_find else 'Price Unavailable'
    p_tags = block.find_all('p')
    rating = p_tags[0].get_text(strip=True) if len(p_tags) < 5 else (p_tags[1].get_text(strip=True) if len(p_tags) > 1 else None)
    colors = p_tags[1].get_text(strip=True) if len(p_tags) < 5 else (p_tags[2].get_text(strip=True) if len(p_tags) > 2 else None)
    size = p_tags[2].get_text(strip=True) if len(p_tags) < 5 else (p_tags[3].get_text(strip=True) if len(p_tags) > 3 else None)
    gender = p_tags[3].get_text(strip=True) if len(p_tags) < 5 else (p_tags[4].get_text(strip=True) if len(p_tags) > 4 else None)
    timestamp = datetime.now()
    return [title, price, rating, colors, size, gender, timestamp]

def scrape_items_from_site_url(pages): #Function scrape per item <div>
    site_url = "https://fashion-studio.dicoding.dev"
    for page in range(1, pages+1):
        try:
            url = site_url if page == 1 else f"{site_url}/page{page}"
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")
            item_blocks = soup.find_all('div', class_='collection-card')
            print(f"Scraping page {page}/{pages}...")

            for block in item_blocks:
                items_data.append(parse_item_block(block))
            time.sleep(1)

        except Exception as e:
            print(f"Error on page {page}: {e}")
            break

    with open('scraped_data.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Product Name', 'Price', 'Rating', 'Colors', 'Size', 'Gender', 'Timestamp'])
        for row in items_data:
            writer.writerow(row)




        
