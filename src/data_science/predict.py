# Import necessary libraries
import pickle
import statsmodels.api as sm
import pandas as pd
import os 
import numpy as np
import csv_excel_operations as ceo

# Define the file paths for the model and the dataset
model_pkl = 'true_model_2023.pkl'

# Keep the current path
current_directory = os.getcwd()

# Keep the beginning of the path
parent_directory = os.path.dirname(os.path.dirname(current_directory))

# Define file paths and constants
file_path_data = os.path.join(parent_directory, 'VBA\data.csv')
file_path_estimation = os.path.join(parent_directory, 'VBA\estimation.csv')

# Load the model from the pickle file
with open(model_pkl, 'rb') as file:
    loaded_model = pickle.load(file)


# Read the dataset from the CSV file
# Ensure the correct path to the CSV file and encoding method are specified
dt = pd.read_csv(file_path_data, sep=";", encoding='latin-1')

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

# Write results to the estimation.csv file
ceo.write_to_excel(file_path_estimation, round(np.exp(srt_pre).iloc[0], 2), 'A2', 'estimation')
ceo.write_to_excel(file_path_estimation, round(np.exp(srt_conf)[0][0], 2), 'B2', 'estimation')
ceo.write_to_excel(file_path_estimation, round(np.exp(srt_conf)[0][1], 2), 'C2', 'estimation')

# Add count of amenities
ceo.write_to_excel(file_path_estimation, ceo.count_true_elements(dt), 'D2', 'estimation')
