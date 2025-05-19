import pandas as pd


class DataEmpty(Exception):
    def __init__(self, message):
        super().__init__(message)

def transform_data_all_in_one():
    df = pd.read_csv('scraped_data.csv')
    if len(df) == 0:
        raise DataEmpty('Cant operate on empty data')
    
    try:

        df = df[df['Product Name'] != 'Unknown Product']
        df = df[df['Price'] != 'Price Unavailable']

       
        df['Price'] = df['Price'].str.replace(r'[^0-9.]', '', regex=True).astype(float) * 16000

      
        df['Rating'] = df['Rating'].str.extract(r'(\d+\.\d)').astype(float)

     
        df['Colors'] = df['Colors'].str.extract(r'(\d+)').astype(int)

  
        df['Size'] = df['Size'].str.replace('Size: ', '', regex=False)

     
        df['Gender'] = df['Gender'].str.replace('Gender: ', '', regex=False)

        df = df.drop_duplicates()
        df = df.dropna()
        print(df.info())
        print(df.describe())
        print(df.head(5))

    except DataEmpty as e:
        print(f"Data requirement error has occured: {e}")
    except Exception as e:
        print(f"An error has occured: {e}")



    return df
