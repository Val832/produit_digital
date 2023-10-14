
import requests 
import re
from tools import crawler

urls = [
    "https://www.cpubenchmark.net/cpu_list.php",
    "https://www.harddrivebenchmark.net/hdd_list.php",
    "https://www.videocardbenchmark.net/gpu_list.php",
    "https://www.memorybenchmark.net/ram_list.php"
]

regex = "net\/(.*?)\.php"
pattern = re.compile(rf"{regex}")

for url in urls : 

    file_name = pattern.search(url).group(1)
    html = crawler.extract_html(url)
    df = crawler.extract_table(html, table_id= 'cputable')
    df.to_csv(f"../produit_digital/data/{file_name}.csv")
    




