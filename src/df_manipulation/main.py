import pandas as pd 
import re 

df_rbnb = pd.read_csv('data/airbnb-listings.csv', sep = ';')

#Permet de donner un aperçu de la qualité des données. 
print(df_rbnb.info())
      
