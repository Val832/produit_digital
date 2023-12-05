import csv_excel_operations as ceo
import os 

# keep the current path
current_directory = os.getcwd()

# keep the beggining of the path
parent_directory = os.path.dirname(os.path.dirname(current_directory))

# Define file paths and constants
file_path_data = os.path.join(parent_directory, 'VBA\data.csv')
file_path_estimation= os.path.join(parent_directory, 'VBA\estimation.csv')

cell_reference = 'B1'
sheet_name = 'Traitement'


data = ceo.read_csv(file_path_data)
count = ceo.count_false_elements(data)


# Write mean value to Excel
ceo.write_to_excel(file_path_estimation, count, cell_reference, sheet_name)

