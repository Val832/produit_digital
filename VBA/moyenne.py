import pandas as pd
import numpy as np 
import xlwings as xw


def meanExcel(path, sheetName):
    data = pd.read_excel(path, sheet_name=sheetName)
    return pd.DataFrame(np.mean(data, axis=0)) 
# J'ai rajouté axis=0 suite à un warning de numpy qui indique que prochainement préciser cet
# argument sera obligatoire donc mieux pour la pérennité du code 


def writeToExcel(path, moy, sheet_name):

    # On  ouvre l'application Excel sans l'afficher à l'écran (visible=False)
    with xw.App(visible=False) as app:
        # On ouvre le classeur Excel indiqué par le chemin 'path'
        workbook = app.books.open(path)
        
        # On récupère les noms des feuilles existantes dans le classeur
        sheet_names = [sheet.name for sheet in workbook.sheets]
        
        # On vérifie si la feuille cible existe
        # Si c'est le cas, on sélection cette feuille et on efface son contenu actuel
        if sheet_name in sheet_names:
            sheet = workbook.sheets[sheet_name]
            sheet.clear()
        else:
            # Si la feuille cible n'existe pas, on la crée
            sheet = workbook.sheets.add(sheet_name)

        # On écrit le df 'moy' dans la feuille cible.
        # On écrit les données à partir de la cellule A1.
        sheet.range('A1').value = moy

        # On sauvegarde le classeur.
        workbook.save()
        # On ferme le classeur.
        workbook.close()

# Tout ce qui est strictement constant et hors fonction en python est toujours en majuscule ;)
PATH = 'FormulaireAIRBNB.xlsm'
SHEET_NAME = 'Données'
moy = meanExcel(PATH, SHEET_NAME)

writeToExcel(PATH, moy, sheet_name='res')
