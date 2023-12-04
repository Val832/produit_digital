#import csv_excel_operation
# from 
import csv_excel_operations as ceo
import os 

current_directory = os.getcwd()
# Remonter de deux niveaux dans la hiérarchie du chemin
parent_directory = os.path.dirname(os.path.dirname(current_directory))

# Define file paths and constants
file_path_data = os.path.join(parent_directory, 'VBA\data.csv')
file_path_estimation= os.path.join(parent_directory, 'VBA\estimation.csv')

cell_reference = 'A1'
sheet_name = 'estimation'


data = ceo.read_csv(file_path_data)

count = ceo.count_false_elements(data)


# Write mean value to Excel
ceo.write_to_excel(file_path_estimation, count, cell_reference, sheet_name)

