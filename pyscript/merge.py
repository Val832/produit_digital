import concurrent.futures
from bs4 import BeautifulSoup
import pandas as pd
import re
import requests

from scrap import URLS, REGEX_PATTERN
from tools import Crawler, Merge

# préciser quelle bdd à enrichir en précisant l'index dans URLS
index = 4
headers = URLS[index]['url_headers']
file_name = re.search(REGEX_PATTERN, URLS[index]['url']).group(1)
"hello"
    
Na_table = Merge.missing_table(headers)
print(Na_table)



def merge_data(file_name):
    df1 = pd.read_csv(f"data/{file_name}.csv")
    sessions = [requests.Session() for _ in range(len(df1['lien']))]
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        all_data = list(executor.map(Merge.fetch_data, df1['lien'], [Na_table]*len(df1['lien']), sessions))
    
    df2 = pd.DataFrame(all_data)
    df = pd.concat([df1, df2], axis=1)
    df.to_csv(f'data/{file_name}2.csv')
    return df


merge_data(file_name)