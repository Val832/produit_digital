import pickle
import statsmodels.api as sm
import pandas as pd

# Define the file paths for the model and the dataset
model_pkl = 'insert model file path here'
dt_file = 'insert dataset file path here'

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

# Print the results
print(srt)