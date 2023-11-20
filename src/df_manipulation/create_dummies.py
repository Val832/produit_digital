import pandas as pd 
from df_tools import count_amenities, create_column_from_match

# Read df
df_rbnb = pd.read_csv('data/rbnb.csv', sep = ',') 

# Create frequency table for amenities column
df_frequency = count_amenities(df_rbnb)
df_frequency.to_csv('data/amenities_frequency.csv', index=False, encoding="utf-8", errors='replace')

# Create a dictionary where each key is the name of an amenity. 
df_frequency = df_frequency[:500]
dictionnaire = {nom: nom for nom in df_frequency['Amenity']}

# Use the create_column_from_match function to add new columns to the df_rbnb DataFrame.
df_new_rbnb = create_column_from_match(df_rbnb, 'amenities', words_dictionnary=dictionnaire)
df_new_rbnb.to_csv('data/rbnb_with_dummies.csv')