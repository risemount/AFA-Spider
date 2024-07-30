import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from call_db import *

class survey_data():
    def __init__(self, data):
        self.header = data[0]
        self.unit = [""].append(data[1])
        self.status = data[2:-1]
    
def afa_scratch(savepath: str, mode: str, export: str, year: str, item: str, crop: str, city: str):

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
        data_obj = survey_data(data)
        df = pd.DataFrame(data_obj.status, columns=data_obj.header)
        if export == "multiple":
            try:
                df.to_csv(os.path.join(savepath, f"{opt.value_dict("crop")[crop]}_{opt.value_dict("year")[year]}_{opt.value_dict("city")[city]}_{opt.value_dict("item")[item]}.csv"), index = False, encoding = 'big5')
            except UnicodeEncodeError as err:
                print(f"{(year, item, crop)} got error: {err}")
        else:
            return data_obj
    else:
        return None

class DataContainer:
    def __init__(self, mode):
        self._data = []
        self.mode = mode
        self.opt = Option(options_in_db(type_=mode))
    
    def register(self, year: str, item: str, crop: str, status_data: survey_data):
        """Register a new data entry."""
        for status_entry in status_data.status:
            entry = {
                '年度': self.opt.value_dict("year")[year],
                '期作': self.opt.value_dict("item")[item],
                '作物': self.opt.value_dict("crop")[crop]
            }
            # Assuming status_entry is a list of key-value pairs or a list with consistent structure
            if "town" == self.mode[4:]:
                for idx, value in enumerate(status_entry, start=0):
                    if idx == 0:
                        cityname = value[:3]
                        townname = value[3:]
                        entry['縣市名稱'] = cityname
                        entry['鄉鎮市(區)'] = townname
                    else:
                        entry[status_data.header[idx]] = value
            elif "city" == self.mode[4:]:
                for idx, value in enumerate(status_entry, start=0):                
                    entry[status_data.header[idx]] = value
            self._data.append(entry)

    def to_dataframe(self):
        """Convert the registered data to a Pandas DataFrame."""
        return pd.DataFrame(self._data)