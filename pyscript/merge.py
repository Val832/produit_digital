import concurrent.futures
from bs4 import BeautifulSoup
import pandas as pd
import re

from scrap import URLS, REGEX_PATTERN
from tools import Crawler

# préciser quelle bdd à enrichir en précisant l'index dans URLS
index = 1
url = URLS[index]
file_name = re.search(REGEX_PATTERN, url).group(1)

def missing_table (): 
    res = Crawler.extract_html("https://www.harddrivebenchmark.net/hdd.php?hdd=35TTFP6PCIE-256G&id=27777")
    table = Crawler.find_element(res, tag='table', element_id='test-suite-results')
    print(table)

    missing_table = {}
    for row in table.findAll('tr'):
        header = row.find('th').text
        missing_table[header] = "NA"
    
    return missing_table
    
Na_table = missing_table()

def fetch_data(url):
    res = Crawler.extract_html(url)
    if not isinstance(res, BeautifulSoup):
        print(f"Erreur : L'URL {url} n'a pas renvoyé un objet BeautifulSoup valide.")
        return {'url': url}
    
    table = Crawler.find_element(res, tag='table', element_id='test-suite-results')
    if table is None : 
        print(f"bad {url}")
    else : 
        print(f"GOOD {url}")

    try : 
        data = {}
        for row in table.findAll('tr'):
            header = row.find('th').text
            value = row.find('td').text
            data[header] = value
        return data 
    except AttributeError : 
        data = Na_table
        return data 


def merge_data(url, file_name):

    html = Crawler.extract_html(url)
    result = Crawler.find_element(html, tag='table', element_id='cputable')
    if result is None : 
        print(url)
    body = result.find('tbody')
    rows = body.find_all('tr')

    base = re.search(r'(.*net/)', url).group(1)
    urls = []

    for row in rows:
        a = row.find('a')
        if a and a.get('href'):
            urls.append(base + a.get('href'))

    for index, current_url in enumerate(urls):
        urls[index] = current_url.replace("_lookup", "")

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        all_data = list(executor.map(fetch_data, urls))

    df2 = pd.DataFrame(all_data)
    df1 = pd.read_csv(f"data/{file_name}.csv")

    df = pd.concat([df1, df2], axis=1)
    df.to_csv(f'data/{file_name}.csv')

    return df

merge_data(url, file_name)

"video_lookup"