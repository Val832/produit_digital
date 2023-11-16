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
    for i in range(len(list_data)):
        list_data[i] = float(list_data[i])
    return list_data


def calculate_mean(list_data):
    """
    Calculates the mean (average) of a list of numeric values.

    Parameters:
    - list_data (list): A list containing numeric values.

    Returns:
    float or str: The mean of the input list, or a message indicating that the list is empty.
    """
    if len(list_data) == 0:
        return "List is empty."

    total_sum = sum(list_data)
    return total_sum / len(list_data)


def read_csv(path):
    """
    Reads a CSV file and returns the last row as a list.

    Parameters:
    - path (str): The path to the CSV file.

    Returns:
    list: A list containing the data from the last row of the CSV file.

    Note:
    This function assumes that the CSV file uses ';' as the delimiter.

    If the CSV file is empty, the function will return an empty list.
    """
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            # Assuming the CSV file has multiple rows, 'last_row' will contain the last row
            last_row = row
    return last_row


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



# Define file paths and constants
file_path = 'data.csv'

sheet_name = 'data'
cell_reference = 'A3'

# Read data from CSV
data_from_csv = read_csv(file_path)
print("Data from CSV:", data_from_csv)

# Convert string data to float
data_as_float = convert_str_to_float(data_from_csv)

# Calculate mean and convert to string
mean_value = calculate_mean(data_as_float)
mean_as_str = str(mean_value)
print("Mean:", mean_as_str)

# Write mean value to Excel
write_to_excel(file_path, mean_as_str, cell_reference, sheet_name)
