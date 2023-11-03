import openpyxl 
import pandas as pd 
import numpy as np

path = r'C:\Users\garan\Desktop\produit_digital\VBA\FormulaireAIRBNB.xlsm'
sheetName = 'Données'

def meanExcel(path,sheetName):
    data=pd.read_excel(path,sheet_name=sheetName)
    return(np.mean(data))

moy=meanExcel(path ,sheetName)
print(moy)
