import pandas as pd

from src.df_manipulation.df_tools import download_file
from config.constants import URL_AIRBNB_2017, PATH_DB_2017, PATH_CLEAN_DB_2017
from src.data_science.data_science_tools import detect_columns

# Download the database and export it to the data folder.
download_file(URL_AIRBNB_2017, PATH_DB_2017)

# Clean up and create a new database following the project's conventions
df_rbnn2017 = pd.read_csv(PATH_DB_2017, sep= ';')
clean_df_rbnn2017 = detect_columns(df_rbnn2017)
clean_df_rbnn2017.to_csv(PATH_CLEAN_DB_2017)
