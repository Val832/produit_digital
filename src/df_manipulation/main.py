import pandas as pd 
import re 

df_rbnb = pd.read_csv('data/listings.csv', sep = ',')

#Permet de donner un aperçu de la qualité des données. 
print(df_rbnb.info())

distinct_amenities = []

for amenities in df_rbnb['amenities'] : 

    # Convertir la chaîne en une liste Python réelle
    import ast
    liste_reelle = ast.literal_eval(amenities)

    # Étape 1: Retirer les guillemets existants
    liste_sans_guillemets = [element.replace('"', '') for element in liste_reelle]

    # Étape 2: Joindre les éléments en une chaîne, séparés par ', '
    chaine = ', '.join(liste_sans_guillemets)

    # Étape 3: Ajouter des guillemets au début et à la fin
    chaine_avec_guillemets = f'"{chaine}"'
    
    # Étape 4: Convertir la chaîne en liste
    liste_finale = chaine_avec_guillemets.split(', ')
    if liste_finale[0][0] == '"':
        liste_finale[0] = liste_finale[0][1:]
    if liste_finale[-1][-1] == '"':
        liste_finale[-1] = liste_finale[-1][:-1]
    
    for ameniti in liste_finale :
        
        if ameniti not in distinct_amenities : 
            
            distinct_amenities.append(ameniti)



import ast
from collections import defaultdict

# Initialisation d'un dictionnaire pour compter les occurrences de chaque amenity
distinct_amenities = defaultdict(int)

for amenities in df_rbnb['amenities']:
    # Convertir la chaîne en liste
    liste_reelle = ast.literal_eval(amenities)

    # Retirer les guillemets et nettoyer les données
    liste_sans_guillemets = [element.replace('"', '') for element in liste_reelle]
    chaine = ', '.join(liste_sans_guillemets)
    chaine_avec_guillemets = f'"{chaine}"'
    liste_finale = chaine_avec_guillemets.split(', ')
    
    if liste_finale[0][0] == '"':
        liste_finale[0] = liste_finale[0][1:]
    if liste_finale[-1][-1] == '"':
        liste_finale[-1] = liste_finale[-1][:-1]

    # Mise à jour du compteur pour chaque amenity
    for amenity in liste_finale:
        distinct_amenities[amenity] += 1

# 1. Transformer le dictionnaire en liste de tuples et 2. Trier la liste
sorted_amenities = sorted(distinct_amenities.items(), key=lambda x: x[1], reverse=True)

# 3. Créer un DataFrame
df_amenities = pd.DataFrame(sorted_amenities, columns=['Amenity', 'Frequency'])

# 4. Enregistrer le DataFrame dans un fichier CSV
df_amenities.to_csv('data/amenities_frequency.csv', index=False, encoding="utf-8", errors='replace')





# Chemin du fichier où enregistrer la liste
"""file_path = 'utils/mod.txt'

with open(file_path, 'w', encoding='utf-8', errors='replace') as file:
    for item in distinct_amenities:
        file.write("%s\n" % item)"""
