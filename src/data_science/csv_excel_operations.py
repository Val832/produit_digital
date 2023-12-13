import pandas as pd
import numpy as np 
import xlwings as xw
import csv

def convert_df_to_float(dataframe):
    """
    Convertit les colonnes de type str en float en remplaçant les virgules par des points dans une DataFrame pandas.

    Parameters:
    - dataframe (pd.DataFrame): La DataFrame à convertir.

    Returns:
    - pd.DataFrame: La DataFrame convertie.
    """

    for column in dataframe.columns:
        if dataframe[column].dtype == 'O':  # Vérifie le type de la colonne (Object/str)
            dataframe[column] = dataframe[column].str.replace(',', '.', regex=False).astype(float)

    return dataframe



def read_csv_to_dataframe(path):
    """
    Reads the first two lines of a CSV file and returns them as a DataFrame.

    Parameters:
    - path (str): The path to the CSV file.

    Returns:
    pandas.DataFrame: A DataFrame containing the data from the first two rows of the CSV file.

    Note:
    This function assumes that the CSV file uses ';' as the delimiter.

    If the CSV file is empty or has only one row, the function will return a DataFrame with that row.
    """
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        # Read the first two rows
        first_two_rows = [next(csv_reader) for _ in range(2)]

    # Convert the list of lists to a DataFrame
    df = pd.DataFrame(first_two_rows)

    return df




def write_to_excel(path, value, cell, sheet_name):
    """
    Writes a value to a specified cell on a specified sheet in an Excel workbook.

    Parameters:
    - path (str): The path to the Excel workbook.
    - value (float): The value to be written to the Excel workbook.
    - cell (str): The cell reference where the value will be written (e.g., 'A1').
    - sheet_name (str): The name of the sheet where the value will be written.

    Returns:
    None

    Note:
    This function utilizes the xlwings library for interacting with Excel.
    """
    # Open the Excel workbook
    wb = xw.Book(path)
    # Select the specified sheet
    sheet = wb.sheets[sheet_name]
    # Write the value to the specified cell
    sheet.range(cell).value = value
    # Save the Excel workbook
    wb.save()
    # Close the Excel workbook
    wb.close()
    
    
    

def average_price_neighborhood(df, neighborhood):
    """
    Calculate the average price for a given neighborhood from a CSV file.

    Parameters:
    - df (dataset): 
    - neighborhood (str): The neighborhood for which to calculate the average price.

    Returns:
    - float: The average price for the specified neighborhood.
    """
    # Filter the DataFrame based on the specified neighborhood
    neighborhood_data = df[df['neighbourhood_cleansed'] == neighborhood]
    
    # Calculate the average price for the specified neighborhood
    average_price = neighborhood_data['price'].mean()
    
    return average_price