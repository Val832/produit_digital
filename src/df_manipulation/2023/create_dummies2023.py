import pandas as pd 

from src.df_manipulation.df_tools import count_amenities_2023, create_column_from_match
from config.constants import *

df_rbnb = pd.read_csv(PATH_CLEAN_DB_2023)

# Create frequency table for amenities column
df_frequency = count_amenities_2023(df_rbnb)
df_frequency.to_csv('data/airbnb2023/airbnb2023_frequency.csv', index=False, encoding="utf-8", errors='replace')

# Create a dictionary where each key is the name of an amenity. 
df_frequency = df_frequency[:500]
dictionnaire = {nom: nom for nom in df_frequency['Amenity']}

#Use the create_column_from_match function to add new columns to the df_rbnb DataFrame.
df_new_rbnb = create_column_from_match(df_rbnb, 'amenities', words_dictionnary=dictionnaire)
df_new_rbnb.to_csv('data/airbnb2023/airbnb2023_dummies.csv')