import pandas as pd 

from src.df_manipulation.df_tools import download_file
from config.constants import URL_AIRBNB_2023, PATH_DB_2023, PATH_CLEAN_DB_2023
from src.data_science.data_science_tools import detect_columns

# Download the database and export it to the data folder. ``
download_file(URL_AIRBNB_2023, PATH_DB_2023)

# Clean up and create a new database following the project's conventions
df_rbnb2023 = pd.read_csv(PATH_DB_2023, sep= ',')
clean_df_rbnb2023 = detect_columns(df_rbnb2023)
clean_df_rbnb2023.to_csv(PATH_CLEAN_DB_2023)
