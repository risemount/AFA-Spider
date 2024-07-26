import requests
import pandas as pd
from bs4 import BeautifulSoup
import sqlite3


def update_options(url: str, attr_: str) -> list:
    """
    Extract the options from url with respect to the selection(attr)
    """
    pgcond_get = requests.get(url)
    ### Clean the selections to data frame
    pgcond_soup = BeautifulSoup(pgcond_get.text, 'lxml') # As soup format
    pgcond_select = pgcond_soup.find("select", attrs = {'name': attr_}) # The chosen seleted name

    # Listing all options
    pgcond_options = pgcond_select.find_all("option") # Update the crop options
    
    updated_data = [] # Container to the value and label in options
    for option in pgcond_options:
        value = option['value']
        label = option.text.split('.')[1] if '.' in option.text else option.text
        updated_data.append({'value': value, 'label': label})

    return updated_data

def create_option_db():
        # Connecting to the database
    conn = sqlite3.connect("./web_options.db")
    cur = conn.cursor()

    # Define the CREATE TABLE statement
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT NOT NULL,
        type TEXT NOT NULL,
        attr TEXT NOT NULL,
        value TEXT NOT NULL,
        label TEXT NOT NULL,
        UNIQUE(url, attr, value)
    )
    '''

    # Execute the CREATE TABLE statement
    cur.execute(create_table_sql)
    
    # Close the database
    conn.close()

def update_database():
    # URLs From the website
    urls = {
        'croptown': "https://agr.afa.gov.tw/afa/pgcroptown_cond.jsp", ## 鄉鎮作物查詢 (一般作物查詢)
        'cropcity': "https://agr.afa.gov.tw/afa/pgcropcity_cond.jsp", ## 縣市作物查詢 (一般作物查詢)
        'ricetown': "https://agr.afa.gov.tw/afa/pgricetown_cond.jsp", ## 鄉鎮稻作查詢 (稻作查詢)
        'ricecity': "https://agr.afa.gov.tw/afa/pgricecity_cond.jsp" ## 縣市稻作查詢 (稻作查詢)
    }

    # The Selection titles
    attrs = {
        'year': "accountingyear", # 年度
        'season': 'item', # 期作別
        'crop': 'crop', # 作物代號
        'city': 'city' # 縣市代號
    }
    conn = sqlite3.connect("./web_options.db")
    cur = conn.cursor()

    for i in urls.keys():
        for j in attrs.keys():
            updated = update_options(url = urls[i], attr_ = attrs[j])
            df = pd.DataFrame(updated, dtype = str)
            # Insert data into the database
            for index, row in df.iterrows():
                cur.execute('''
                    INSERT OR REPLACE INTO data (url, type, attr, value, label) VALUES (?, ?, ?, ?, ?)
                ''', (urls[i], i, attrs[j], row['value'], row['label']))
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()