"""
Sraping de données de benchmarks 

Fournit des outils pour extraire et traiter les benchmarks de composants informatiques.

Fonctions:
    - extract_html: Récupère le contenu HTML.
    - extract_table: Extrait les données d'un tableau.

Auteur: [Val832]
Date de création: {creation_date}
Dernière mise à jour: {last_update}
Version: {version}
""".format(creation_date="DATE_CREATION_AUTO", last_update="DATE_MISE_A_JOUR_AUTO", version="VERSION_AUTO")


import re
from tools import crawler

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
    html_content = crawler.extract_html(url)

    # Extraction des données depuis le tableau présent dans le contenu HTML.
    dataframe = crawler.extract_table(html_content, table_id='cputable')

    # Sauvegarde des données sous forme de fichier CSV associé au composant correspondant.
    dataframe.to_csv(f"../produit_digital/data/{file_name}.csv")