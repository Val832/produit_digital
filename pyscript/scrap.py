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

from tools import Crawler

# Liste des URL concernant les benchmarks des différents composants informatiques.
URLS = [
    "https://www.cpubenchmark.net/cpu_list.php",
    "https://www.harddrivebenchmark.net/hdd_list.php",
    "https://www.videocardbenchmark.net/gpu_list.php",
    "https://www.memorybenchmark.net/ram_list.php",
    "https://www.memorybenchmark.net/ram_list-ddr4.php",
    "https://www.memorybenchmark.net/ram_list-ddr3.php"
]

# Expression régulière pour extraire le nom du composant à partir de l'URL.
REGEX_PATTERN = r"net\/(.*?)\.php"

for url in URLS:

    # Utilisation de l'expression régulière pour identifier le nom du composant depuis l'URL.
    match = re.search(REGEX_PATTERN, url)
    file_name = match.group(1) if match else 'unnamed'  # Nom du composant ou "unnamed" si non identifié.

    # Extraction du contenu HTML depuis l'URL.
    html_content = Crawler.extract_html(url)

    # Extraction des données depuis le tableau présent dans le contenu HTML.
    dataframe = Crawler.extract_table(html_content, table_id='cputable')

    # Sauvegarde des données sous forme de fichier CSV associé au composant correspondant.
    dataframe.to_csv(f"../produit_digital/data/{file_name}.csv")
