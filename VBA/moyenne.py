import pandas as pd
import numpy as np 
import xlwings as xw
import csv

def convertStrToFloat(list_data):
    for value in range(len(list_data)):
        list_data[value]=float(list_data[value])
    return(list_data)



def mean(list_data):
    somme = 0
    for value in range(len(list_data)):
        somme+=list_data[value]
    return (somme / len(list_data))

# read csv and keep the result in a list 
def readExcel(path):
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            a=row
            line_count += 1
    return(a)


def writeToExcel(path, moy, cell, sheet_name):
    # Ouvrir le classeur Excel
    wb = xw.Book(path)
    # Sélectionner la feuille spécifiée
    sheet = wb.sheets[sheet_name]
    # Écrire la moyenne dans la cellule spécifiée
    sheet.range(cell).value = moy
    # Enregistrez le classeur Excel
    wb.save()
    # Fermez le classeur Excel
    wb.close()

    
def convertir_virgule(chaine):
    # Remplace la virgule par un point et convertit en nombre à virgule flottante
    try:
        resultat = float(chaine.replace(',', '.'))
        return resultat
    except ValueError:
        print("Erreur : La chaîne n'est pas au bon format.")
        return None
    

def convertir_virgule_chaine(nombre):
    # Convertit le nombre en chaîne avec une virgule comme séparateur décimal
    try:
        resultat = "{:.1f}".format(nombre).replace('.', ',')
        return resultat
    except ValueError:
        print("Erreur : La valeur n'est pas au bon format.")
        return None



PATH = r'C:\Users\garan\Desktop\produit_digital\VBA\data.csv'
SHEET_NAME='data'
CELL='A3'

DATA = readExcel(PATH)
print(DATA)

DATA = convertStrToFloat(DATA)
MOY = str(mean(DATA))
writeToExcel(PATH, MOY, CELL, SHEET_NAME)


#def convertir_virgule(chaine):
#   resultat = float(chaine.replace(',', '.'))
#   return resultat

# Exemple d'utilisation
#valeur_chaine = 2,2
#resultat_conversion = convertir_virgule(valeur_chaine)
#print(resultat_conversion)