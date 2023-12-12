import pickle
import statsmodels.api as sm
import pandas as pd
import os 
import numpy as np
import csv_excel_operations as ceo

# Define the file paths for the model and the dataset
model_pkl = 'true_model_2023.pkl'

current_directory = os.getcwd()
parent_directory = os.path.dirname(os.path.dirname(current_directory))
dt_file = os.path.join(parent_directory, 'VBA\data.csv')

# Load the model from the pickle file
with open(model_pkl, 'rb') as file:
    loaded_model = pickle.load(file)


# Read the dataset from the CSV file
# Ensure the correct path to the CSV file and encoding method are specified
dt = pd.read_csv(dt_file, sep=";", encoding='latin-1')

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

#write result in csv
file_path_estimation= os.path.join(parent_directory, 'VBA\estimation.csv')

ceo.write_to_excel(file_path_estimation, np.exp(srt_pre).iloc[0], 'A2', "estimation")
ceo.write_to_excel(file_path_estimation, np.exp(srt_conf)[0][0], 'B2', "estimation")
ceo.write_to_excel(file_path_estimation, np.exp(srt_conf)[0][1], 'C2', "estimation")
