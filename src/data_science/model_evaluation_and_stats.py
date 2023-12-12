import csv_excel_operations as ceo
import os 
import statsmodels.api as sm
import numpy as np
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


#keep seconc line 
dt = data.iloc[1:2, :].copy()


# convert
ceo.convert_df_to_float(dt)


model_pkl = 'true_model_2023.pkl'

#dt=data.head(2)
# Charger le modèle à partir du fichier pickle
with open(model_pkl, 'rb') as file:
    loaded_model = pickle.load(file)

srt_conf = loaded_model.get_prediction(dt).conf_int(alpha = .05 )
srt_pre = loaded_model.predict(dt)
srt = {'predict' : np.exp(srt_pre).iloc[0], 'born_inf' : np.exp(srt_conf)[0][0], 'born_sup' : np.exp(srt_conf)[0][1]}

# write result on estimation.csv file
ceo.write_to_excel(file_path_estimation,round(np.exp(srt_pre).iloc[0],2), 'A2', 'estimation')
ceo.write_to_excel(file_path_estimation, round(np.exp(srt_conf)[0][0],2), 'B2', 'estimation')
ceo.write_to_excel(file_path_estimation, round(np.exp(srt_conf)[0][1],2), 'C2', 'estimation')

#add count of ameneties
ceo.write_to_excel(file_path_estimation,ceo.count_true_elements(dt) , 'D2', 'estimation')
