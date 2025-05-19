from .extract import *
from .transform import *
from sqlalchemy import create_engine



def save_to_csv_final(df): #Save ke CSV
    if len(df)==0:
        raise DataEmpty('Cant operate on empty data')
    try:
        df.to_csv('scraped_data_transformed.csv', index=False)

    except Exception as e:
        print(f"An error occured:{e}")
    
    except DataEmpty as e:
        print(f"Data Requirement has occured: {e}")



def save_to_postgre_sql(df): #Save ke postgresql
    if len(df)==0:
            raise DataEmpty('Cant operate on empty data')
    try:
        username = 'mounkfedev'
        password = '070707dev'
        host = 'localhost'  
        port = '5432'       
        database = 'productdb'

        engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{database}')
        
        
        df.to_sql('products', engine, if_exists='replace', index=False)

        print("DataFrame successfully saved to PostgreSQL!")

    except Exception as e:
        print(f"An error occured:{e}")
    
    except DataEmpty as e:
        print(f"Data requirement error has occured: {e}")
    

