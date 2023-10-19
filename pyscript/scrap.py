"""
Scraping de données de benchmarks 

Script qui permet d'extraire les données de benchmarks de composants informatiques.
Les données de l'exctration sont disponibles dans le répertoire data. 

Fonctions:
    - extract_html: Récupère le contenu HTML.
    - extract_table: Extrait les données d'un tableau.

Auteur: [Val832]
Date de création: 17/10/2023
"""

import re
import pandas as pd
import requests
import concurrent.futures

from tools import Crawler, clean_df, Merge
 

# Liste des URL concernant les benchmarks des différents composants informatiques.
URLS = [
    {
        "url": "https://www.cpubenchmark.net/cpu_list.php",
        "url_headers": "https://www.cpubenchmark.net/cpu.php?cpu=Intel+Core+i5-3437U+%40+1.90GHz&id=1828"
    },
    {
        "url": "https://www.harddrivebenchmark.net/hdd_list.php",
        "url_headers": "https://www.harddrivebenchmark.net/hdd.php?hdd=35TTFP6PCIE-256G&id=27777"
    },
    {
        "url": "https://www.videocardbenchmark.net/gpu_list.php",
        "url_headers": "https://www.videocardbenchmark.net/gpu.php?gpu=Radeon+R7+A10-7860K&id=3447"
    },
    {
        "url": "https://www.memorybenchmark.net/ram_list.php",
        "url_headers": "https://www.memorybenchmark.net/ram.php?ram=Corsair+CM5S16GM4800A40N2+16GB&id=18343"
    },
    {
        "url": "https://www.memorybenchmark.net/ram_list-ddr4.php",
        "url_headers": "https://www.memorybenchmark.net/ram.php?ram=A-DATA+Technology+AD5U48008G-B+8GB&id=18348"
    }
]

# Expression régulière pour extraire le nom du composant à partir de l'URL.
REGEX_PATTERN = r"net\/(.*?)\.php"

for i in URLS:

    url = i['url']

    # Utilisation de l'expression régulière pour identifier le nom du composant depuis l'URL.
    match = re.search(REGEX_PATTERN, url)
    file_name = match.group(1) if match else 'unnamed'  # Nom du composant ou "unnamed" si non identifié.

    # Extraction du contenu HTML depuis l'URL.
    html_content = Crawler.extract_html(url)

    # Extraction des données depuis le tableau présent dans le contenu HTML.
    df1  = Crawler.extract_table(html_content, table_id='cputable')

    result = Crawler.find_element(html_content, tag='table', element_id='cputable')
    body = result.find('tbody')
    rows = body.find_all('tr')

    base = re.search(r'(.*net/)', url).group(1)
    urls = []

    for row in rows:
        a = row.find('a')
        if a and a.get('href'):
            urls.append(base + a.get('href'))

    for index, current_url in enumerate(urls):
        if  url == "https://www.videocardbenchmark.net/gpu_list.php": 
            urls[index] = current_url.replace("video_lookup", "gpu")
        else : 
            urls[index] = current_url.replace("_lookup", "")

    df2 = pd.DataFrame({"lien" : urls})
    df = pd.concat([df1, df2], axis=1)
    df = clean_df.convert_str_na_to_nan(df,"NA")
    df = clean_df.drop_na(df)

    # Sauvegarde des données sous forme de fichier CSV associé au composant correspondant.
    df.to_csv(f"../produit_digital/data/{file_name}.csv")
