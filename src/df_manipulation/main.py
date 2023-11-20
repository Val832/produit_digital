import pandas as pd 
from df_tools import count_amenities

df_rbnb = pd.read_csv('data/listings.csv', sep = ',')

df_amenities = count_amenities(df_rbnb)

df_amenities.to_csv('data/amenities_frequency.csv', index=False, encoding="utf-8", errors='replace')
