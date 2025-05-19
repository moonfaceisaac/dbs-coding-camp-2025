
from utils.extract import *
from utils.load import *
from utils.transform import *


def main():
    scrape_items_from_site_url(50) #Scraping
    print('Scraping Completed')
    df = transform_data_all_in_one() #Transformation
    print('Transformation Completed')
    save_to_csv_final(df)
    print('Saving to CSV Completed') #Save ke .CSV
    save_to_postgre_sql(df)
    print('Saving to postgre Completed') #Save ke postgresql



if __name__ == "__main__":
    main()