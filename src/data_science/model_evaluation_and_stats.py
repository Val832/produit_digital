import csv_excel_operations as ceo
import os 
import statsmodels.api as sm
import pickle

# keep the current path
current_directory = os.getcwd()

# keep the beggining of the path
parent_directory = os.path.dirname(os.path.dirname(current_directory))

# Define file paths and constants
file_path_data = os.path.join(parent_directory, 'VBA\data.csv')
file_path_estimation= os.path.join(parent_directory, 'VBA\estimation.csv')

cell_reference = 'B1'
sheet_name = 'Traitement'


data = ceo.read_csv_to_dataframe(file_path_data)

#count = ceo.count_false_elements(data)


# Write mean value to Excel
#ceo.write_to_excel(file_path_estimation, count, cell_reference, sheet_name)

model_pkl = 'best_model_2023.pkl'

dt=data.head(1)

# Charger le modèle à partir du fichier pickle
with open(model_pkl, 'rb') as file:
    loaded_model = pickle.load(file)

#srt_conf = loaded_model.get_prediction(dt).conf_int(alpha = .05 )
#srt_pre = loaded_model.predict(dt)
#srt = {'predict' : np.exp(srt_pre).iloc[0], 'born_inf' : np.exp(srt_conf)[0][0], 'born_sup' : np.exp(srt_conf)[0][1]}

#print(str)