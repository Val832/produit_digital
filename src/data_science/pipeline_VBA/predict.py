# Import necessary libraries
import pickle
import pandas as pd
import os 
import numpy as np
import csv_excel_operations as ceo
print("calcul en cours ... Merci de patienter")

# Keep the current path
current_directory = os.getcwd()

# Keep the beginning of the path
parent_directory = os.path.dirname(os.path.dirname(current_directory))
parent_directory_without_src = os.path.normpath(os.path.join(parent_directory, '..'))


# Define file paths and constants
file_path_data = os.path.join(parent_directory_without_src, 'VBA\data.csv')
file_path_estimation = os.path.join(parent_directory_without_src, 'VBA\estimation.csv')


# Define the file paths for the model and the dataset
model_pkl = os.path.join(parent_directory_without_src,'data/models/true_model_2023.pkl')



# Load the model from the pickle file
with open(model_pkl, 'rb') as file:
    loaded_model = pickle.load(file)

# Read the dataset from the CSV file
# Ensure the correct path to the CSV file and encoding method are specified
dt = pd.read_csv(file_path_data, sep=";", encoding='latin-1')

ceo.convert_df_to_float(dt)

# Perform prediction and calculate confidence intervals
srt_conf = loaded_model.get_prediction(dt).conf_int(alpha=0.05)
srt_pre = loaded_model.predict(dt)

# Prepare the results dictionary
# Ensure necessary libraries like numpy (np) are imported
srt = {
    'predict': np.exp(srt_pre).iloc[0],
    'born_inf': np.exp(srt_conf)[0][0],
    'born_sup': np.exp(srt_conf)[0][1]
}

print(srt)
# Write results to the estimation.csv file
ceo.write_to_excel(file_path_estimation, round(np.exp(srt_pre).iloc[0], 2), 'A2', 'estimation')
ceo.write_to_excel(file_path_estimation, round(np.exp(srt_conf)[0][0], 2), 'B2', 'estimation')
ceo.write_to_excel(file_path_estimation, round(np.exp(srt_conf)[0][1], 2), 'C2', 'estimation')
