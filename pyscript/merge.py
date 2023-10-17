import re
import concurrent.futures

import pandas as pd

from scrap import URLS, REGEX_PATTERN
from tools import crawler

# préciser quelle bdd à enrichir en précisant l'index dans URLS
index = 2
url = URLS[index]
file_name = re.search(REGEX_PATTERN, url).group(1)

def fetch_data(url):
    res = crawler.extract_html(url)
    table = crawler.find_element(res, tag='table', element_id='test-suite-results')

    data = {}
    for row in table.findAll('tr'):
        header = row.find('th').text
        value = row.find('td').text
        data[header] = value

    return data


def merge_data(url, file_name):
    html = crawler.extract_html(url)
    result = crawler.find_element(html, tag='table', element_id='cputable')
    result = result.find('tbody')
    result = result.find_all('tr')

    base = re.search(r'(.*net/)', url).group(1)
    urls = []

    for i in result:
        a = i.find('a')
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




print(merge_data(url, file_name))



