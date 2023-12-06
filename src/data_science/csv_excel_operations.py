import pandas as pd
import numpy as np 
import xlwings as xw
import csv


def convert_str_to_float(list_data):
    """
    Converts each string element in the input list to a floating-point number.

    Parameters:
    - list_data (list): A list containing string representations of numbers.

    Returns:
    list: A new list where each element is converted to a float.
    """
    list_data_convert = []  # Crée une nouvelle liste pour stocker les résultats convertis
    for i in range(len(list_data)):
        list_data_convert.append(float(list_data[i]))
    return list_data_convert


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
    
    
    
def count_false_elements(data_list):
    """
    Count the number of occurrences of "FAUX" in a given list.

    Parameters:
    - data_list (list): The input list containing elements to be checked.

    Returns:
    - int: The count of occurrences of "FAUX" in the list.
    """
    # Initialize a counter variable to keep track of "FAUX" occurrences
    false_count = 0

    # Iterate through each element in the list
    for element in data_list:
        # Check if the current element is equal to "FAUX"
        if element == "FAUX":
            # Increment the counter if "FAUX" is found
            false_count += 1

    # Return the final count of "FAUX" occurrences
    return false_count