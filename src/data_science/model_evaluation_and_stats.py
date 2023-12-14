# Import necessary libraries
import csv_excel_operations as ceo
import os
import statsmodels.api as sm
import numpy as np
import pickle
import pandas as pd

# Keep the current path
current_directory = os.getcwd()

# Keep the beginning of the path
parent_directory = os.path.dirname(os.path.dirname(current_directory))

# Define file paths and constants
file_path_data = os.path.join(parent_directory, 'VBA\data.csv')
file_path_estimation = os.path.join(parent_directory, 'VBA\estimation.csv')

# Read data from CSV to DataFrame
data = ceo.read_csv_to_dataframe(file_path_data)

# Keep the second line of the data
dt = data.iloc[1:2, :].copy()

# Convert the DataFrame to float
ceo.convert_df_to_float(dt)

# Load the pre-trained model from a pickle file
model_pkl = 'true_model_2023.pkl'
with open(model_pkl, 'rb') as file:
    loaded_model = pickle.load(file)

# Get predictions and confidence intervals
srt_conf = loaded_model.get_prediction(dt).conf_int(alpha=0.05)
srt_pre = loaded_model.predict(dt)
srt = {'predict': np.exp(srt_pre).iloc[0], 'born_inf': np.exp(srt_conf)[0][0], 'born_sup': np.exp(srt_conf)[0][1]}

# Write results to the estimation.csv file
ceo.write_to_excel(file_path_estimation, round(np.exp(srt_pre).iloc[0], 2), 'A2', 'estimation')
ceo.write_to_excel(file_path_estimation, round(np.exp(srt_conf)[0][0], 2), 'B2', 'estimation')
ceo.write_to_excel(file_path_estimation, round(np.exp(srt_conf)[0][1], 2), 'C2', 'estimation')

# Add count of amenities
ceo.write_to_excel(file_path_estimation, ceo.count_true_elements(dt), 'D2', 'estimation')
