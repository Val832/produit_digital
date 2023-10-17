
import requests 
import re
from tools import crawler, clean_df
import pandas as pd

urls = [
    "https://www.cpubenchmark.net/cpu_list.php",
    "https://www.harddrivebenchmark.net/hdd_list.php",
    "https://www.videocardbenchmark.net/gpu_list.php",
    "https://www.memorybenchmark.net/ram_list.php",
    "https://www.memorybenchmark.net/ram_list-ddr4.php",
    "https://www.memorybenchmark.net/ram_list-ddr3.php"
]


regex = "net\/(.*?)\.php"
pattern = re.compile(rf"{regex}")

for url in urls : 

    file_name = pattern.search(url).group(1)
    html = crawler.extract_html(url)
    print(url)

    df = crawler.extract_table(html, table_id= 'cputable')
    df = clean_df.convert_str_na_to_nan(df, 'NA')
    df = clean_df.drop_na(df)

    

    result = crawler.find_element(html , tag = 'table', element_id= 'cputable' )
    result = result.find('tbody')
    result = result.find_all('tr')


    base = re.search(r'(.*net/)', url).group(1)
    urls  = []

    for i in result : 

        a = i.find('a')

        for j in a : 
            urls.append(base + a.get('href'))

    for index, current_url in enumerate(urls):
        urls[index] = current_url.replace("_lookup", "")
    print(urls)
    all_data = []

    for i in urls : 

        res = crawler.extract_html(i)
        table  = crawler.find_element(res, tag = 'table', element_id = 'test-suite-results')

        data = {}

        for row in table.findAll('tr'):
            header = row.find('th').text
            value = row.find('td').text
            data[header] = value
        all_data.append(data)

    df2 = pd.DataFrame(all_data)

    df = result = pd.concat([df, df2], axis=1)
    df.to_csv(f"../produit_digital/data/{file_name}.csv")



