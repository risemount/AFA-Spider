import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from call_db import *



def afa_scratch(savepath: str, mode: str, year: str, item: str, crop: str, city: str):

    opt = Option(options_in_db(type_=mode))

    # URLs From the website
    urls = {
        'croptown': "https://agr.afa.gov.tw/afa/pgcroptown.jsp", ## 鄉鎮作物查詢 (一般作物查詢)
        'cropcity': "https://agr.afa.gov.tw/afa/pgcropcity.jsp", ## 縣市作物查詢 (一般作物查詢)
        'ricetown': "https://agr.afa.gov.tw/afa/pgricetown.jsp", ## 鄉鎮稻作查詢 (稻作查詢)
        'ricecity': "https://agr.afa.gov.tw/afa/pgricecity.jsp" ## 縣市稻作查詢 (稻作查詢)
    }

    # Request data
    payload = {
        'accountingyear': year,
        'item': item, # Season
        'corn001': '',
        'input803': '',
        'crop': crop, # Crop
        'city': city, # All location
        'btnSend': '送　出'
    }

    try:
        # POST request
        response = requests.post(urls[mode], data = payload)

        # Check the responses
        response.raise_for_status()  # Raises an HTTPError for bad responses (4XX, 5XX)
        print('Success')  # Outputs the response text directly

    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Oops: Something Else", err)
        # Parse the HTML
    soup = BeautifulSoup(response.text, 'lxml')

    # Find the table
    div = soup.find('div', class_='DivRestTbl')

    rows = div.find('table', class_= "TDFont")

    # Extract rows
    rows = rows.find_all('tr')
    # Process each row to extract column data
    data = []
    for row in rows:
        cols = [ele.text.strip() for ele in row.find_all('td')]
        if cols:  # Avoid empty lists from empty rows
            cols = [col.replace(",", "") for col in cols if "�" not in col]
            data.append(cols)

    # Create a DataFrame with the extracted data
    # First row of data contains the headers
    if not ['查無資料！！'] in data:
        df = pd.DataFrame(data[1:], columns=data[0])
        
        try:
            df.to_csv(os.path.join(savepath, f"{opt.value_dict("crop")[crop]}_{opt.value_dict("year")[year]}_{opt.value_dict("city")[city]}_{opt.value_dict("item")[item]}.csv"), index = False, encoding = 'big5')
        except UnicodeEncodeError as err:
            print(f"{(year, item, crop)} got error: {err}")

    return 0
